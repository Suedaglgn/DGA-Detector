import transformers
from transformers import BertTokenizer


def load_pretrained(path):
    """
    A method that loads tokenizer model using vocab.txt
    :return:
    """
    print("BERT model loading...")
    return transformers.BertTokenizer(
        vocab_file=path,
        clean_text=True,
        handle_chinese_chars=False,
        strip_accents=False,
        lowercase=True
    )


def tokenize_value(string, model:BertTokenizer):
    """
    Method that tokenizes input string and return
    :param string: Input data for tokenizing
    :return:
    """
    return " ".join(model.tokenize(string.lower()))


def tokenize_list(data_list, model):
    return [tokenize_value(item, model) for item, i in zip(data_list, range(len(data_list)))]


def predict_list(value, model):
    """
    A method that predict the result of input value
    :param value:
    :return:
    """
    print("Model prediction...")
    return [model.predict(item) for item in value]


def predict_value(value, model):
    return model.predict(value)
