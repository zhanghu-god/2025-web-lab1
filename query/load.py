import json
import pickle

from Trie import Trie
from config import *
from report.structure import inverted_index


def load_pickle(path):
    with open(path, "rb") as f:
        return pickle.load(f)
def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def load():
    id_name = load_pickle(ID_NAME)
    inverted_index = load_pickle(INVERTED_INDEX)
    dictionary = Trie.decompress_from_blocking(load_pickle(DICTIONARY_BLOCKING))
    return dictionary, inverted_index, id_name