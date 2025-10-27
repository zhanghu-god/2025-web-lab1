import json
import pickle

from config import *

def store_pickle(file,path):
    with open(path, "wb") as f:
        pickle.dump(file, f)
def store_json(file,path):
    with open(path, "w") as f:
        json.dump(file, f, ensure_ascii=False, indent=2)

def store_id_name(id_name):
    store_pickle(id_name, ID_NAME)
    store_json(id_name, ID_NAME_JSON)

def store_inverted_index(inverted_index):
    store_pickle(inverted_index, INVERTED_INDEX)
    store_json(inverted_index, INVERTED_INDEX_JSON)

'''下面是三个索引存储方式'''
#未压缩直接顺序存储
def store_list(dictionary, inverted_index, id_name):
    store_inverted_index(inverted_index)
    store_id_name(id_name)
    words, posting_indexes = dictionary.convert_to_list()
    print(len(words))
    store_pickle((words, posting_indexes), DICTIONARY_ORIN)
    store_json((words, posting_indexes), DICTIONARY_ORIN_JSON)

#按块存储
def store_blocking(dictionary):
    # store_inverted_index(inverted_index)
    # store_id_name(id_name)
    blocks, long_string = dictionary.convert_to_blocking(BLOCK_SIZE)
    store_pickle((blocks, long_string), DICTIONARY_BLOCKING)
    store_json((blocks, long_string), DICTIONARY_BLOCKING_JSON)
