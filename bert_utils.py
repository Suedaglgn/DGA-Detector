import transformers
from transformers import BertTokenizer


def load_pretrained(path):
    """
    A method that loads tokenizer model using vocab.txt
    :param path: path of vocabulary file
    :return: tokenizer model
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
    :param model: tokenizer model
    :return: tokenized value
    """
    return " ".join(model.tokenize(string.lower()))


def tokenize_list(data_list, model):
    """
    Method that tokenizes a list
    :param data_list: list of string
    :param model: tokenizer model
    :return: tokenized list
    """
    return [tokenize_value(item, model) for item, i in zip(data_list, range(len(data_list)))]


def predict_list(value, model):
    """
    A method that predict the result of input value
    :param value: list of string
    :param model: classification model
    :return: prediction result of list
    """
    print("Model prediction...")
    return [model.predict(item) for item in value]


def predict_value(value, model):
    """
    Method that predict DGA probability
    :param value: string
    :param model: classification model
    :return: result of probability
    """
    return model.predict(value)
