import os
import time
import fasttext
import pandas as pd
import tldextract
from flask import Flask, jsonify, request, send_file, render_template
from bert_utils import tokenize_list, tokenize_value, predict_list, predict_value, load_pretrained

# model threshold
THRESHOLD = 0.5

# load bert model via corpus
bert = load_pretrained(path="model/vocab.txt")
# load fasttext model
model = fasttext.load_model(path="model/supervised_model_with_BERT_v07")
app = Flask(__name__)
# directory path for uploaded files
app.config["UPLOAD_FOLDER"] = "uploads/"
dir_upload = os.path.join(os.getcwd(), "uploads")
os.makedirs(dir_upload, exist_ok=True)
dir_result = os.path.join(os.getcwd(), "results")
os.makedirs(dir_result, exist_ok=True)
# current white list path
curr_white_list = "White_list.txt"


@app.route("/")
def main():
    """
    Main page
    """
    return render_template('index.html')


@app.route('/detect', methods=["POST"])
def detect():
    """
    A method that detects domain as dga or not
    :return: model result as dga label and model confidence
    """
    whitelist = []
    global message
    f = open("white_list/White_list.txt", 'r')
    for i in f.readlines():
        whitelist.append(i.replace('\n', ''))
    question = str(request.get_json()["domain"])
    domain = tldextract.extract(question).domain
    suffix = tldextract.extract(question).suffix.split(".")[0]
    extract = domain
    if suffix:
        extract = domain + "." + suffix
    domain_ = ".".join(extract.split(".")[-2:])
    if domain_ in whitelist:
        message = "DGA: False, " + domain_ + " is in whitelist"
        return jsonify({"status": "success"}), 200
    # preprocess the domain
    question = tokenize_value(question, model=bert)
    # predict the domain
    pred = predict_value(question, model=model)
    # set label according to condition
    result = True if pred[0][0] == "__label__1" and pred[1][0] > THRESHOLD else False
    f.close()
    message = domain_ + " | " + "DGA: " + str(result) + ", Probability: " + '{:.4f}'.format(pred[1][0])
    return jsonify({"status": "success"}), 200


@app.route('/bulk', methods=["POST"])
def bulk():
    """
    A method that detects bulk domain as dga or not from given file
    :return: model result as dga label and model confidence
    """
    whitelist = []
    f = open("white_list/White_list.txt", 'r')
    for i in f.readlines():
        whitelist.append(i.replace('\n', ''))

    try:
        suspicious = []
        if 'file' not in request.files:
            return jsonify({"status": "error", "reason": "file not found"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "reason": "file not found"}), 400
        if file and file.filename.split(".")[-1] in ["xlsx", "csv"]:
            try:
                file.save(app.config['UPLOAD_FOLDER'] + file.filename)
                path = app.config['UPLOAD_FOLDER'] + file.filename
                df = pd.read_csv(path, names=["domain"])
                set_log_list = list(set(df["domain"]))
                for item in set_log_list:
                    extract = tldextract.extract(item).domain + "." + tldextract.extract(item).suffix.split(".")[0]
                    domain_ = ".".join(extract.split(".")[-2:])
                    # if not domain is in whitelist, mark it as suspicious
                    if not domain_ in whitelist:
                        suspicious.append(item)
                        # tokenize and predict the suspicious domain
                question = tokenize_list(suspicious, model=bert)
                pred_list = predict_list(question, model=model)
                columns = ["domain", "label", "confidence"]
                new_df = pd.DataFrame(columns=columns)
                for i in range(len(pred_list)):
                    all_logs_with_cond = df[df["domain"] == suspicious[i]]
                    for j in range(len(all_logs_with_cond)):
                        if pred_list[i][0][0] == "__label__1":
                            dga_status = "DGA"
                        else:
                            dga_status = "legit"
                        out = list(all_logs_with_cond.iloc[j]) + [dga_status] + [round(pred_list[i][1][0], 4)]
                        out = pd.Series(out, index=columns)
                        new_df = new_df.append(out, ignore_index=True)
                fname = "results/" + "classified_" + "".join(file.filename.split(".")[:-1]) + ".xlsx"
                pd.DataFrame(new_df).to_excel(fname, index=False, engine='openpyxl')
                return send_file(fname, as_attachment=True)
            except Exception as e:
                return jsonify({"status": "error", "reason": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "reason": str(e)}), 400


@app.route('/whitelist/list', methods=["GET"])
def whitelist_list():
    """
    A method that shows all whitelists
    :return: whitelists in whitelist directory
    """
    return jsonify(os.listdir("white_list/"))


@app.route('/configuration', methods=["POST", "GET"])
def configuration():
    """
    A method that get and set current whitelist
    :return: current whitelist
    """
    try:
        global curr_white_list
        if request.method == 'GET':
            return jsonify(curr_white_list)
        if request.method == 'POST':
            old_model = curr_white_list
            model_id = str(request.get_json()["model"])
            curr_white_list = model_id
            return jsonify({"old_list": old_model, "current_list": model_id})

    except Exception as e:
        return jsonify({"status": "error", "reason": str(e)}), 400


@app.route('/whitelist/content/<name>', methods=["GET"])
def whitelist_content(name):
    """
    A method that get content of whitelist
    :param name: name of desired whitelist
    :return: content of whitelist
    """
    try:
        f = open(f"white_list/{name}", "r")
        return jsonify([line.replace('\n', '') for line in f.readlines()])
    except Exception as e:
        return jsonify({"status": "error", "reason": str(e)}), 400


@app.route('/upload_whitelist', methods=["POST"])
def set_whitelist():
    """
    A method that set whitelist from given file
    :return: new whitelist content in new tab
    """
    try:
        wlist = pd.read_csv("white_list/White_list.txt", names=["domain"])
        # read given whitelist
        if 'file' not in request.files:
            return jsonify({"status": "error", "reason": "no field"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "reason": "no name"}), 400
        file.save(app.config['UPLOAD_FOLDER'] + file.filename)
        file_dir = app.config['UPLOAD_FOLDER'] + file.filename
        nlist = pd.read_csv(file_dir, names=["domain"])
        # concat old list and given list and drop dublicates
        new = pd.concat([wlist, nlist], axis=0, ignore_index=True)
        new.drop_duplicates()
        # export new whitelist as txt
        wlist_name = f"White_list_{str(int(time.time()))}.txt"
        new.to_csv(f"white_list/{wlist_name}", index=False, header=False)
        return render_template("whitelist.html", name=wlist_name)
    except Exception as e:
        return jsonify({"status": "error", "reason": str(e)}), 400


@app.route("/result/<method>", methods=["GET"])
def result(method):
    """
    Result pages
    """
    if method == "predict":
        return render_template("result_index.html", result=message)
    if method == "whitelist":
        return render_template("whitelist.html", name=curr_white_list)
    if method == "list_wlist":
        return render_template("list_of_wlist.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
