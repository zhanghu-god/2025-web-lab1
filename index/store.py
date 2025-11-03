import json
import os
import pickle

from config import *

def store_pickle(file,path):
    # 创建目录（如果不存在）
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(file, f)
def store_json(file,path):
    # 创建目录（如果不存在）
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(file, f, ensure_ascii=False, indent=2)

def store_id_name(id_name):
    store_pickle(id_name, ID_NAME)
    store_json(id_name, ID_NAME_JSON)

def store_inverted_index(inverted_index):
    if(TEST):
        store_pickle(inverted_index, INVERTED_INDEX_TEST)
        store_json(inverted_index, INVERTED_INDEX_TEST_JSON)
    else:
        store_pickle(inverted_index, INVERTED_INDEX)
        store_json(inverted_index, INVERTED_INDEX_JSON)

'''下面是三个索引存储方式'''
#未压缩直接顺序存储
def store_list(dictionary, inverted_index, id_name):
    store_inverted_index(inverted_index)
    store_id_name(id_name)
    words, posting_indexes = dictionary.convert_to_list()
    store_pickle((words, posting_indexes), DICTIONARY_ORIN)
    store_json((words, posting_indexes), DICTIONARY_ORIN_JSON)

#按块存储
def store_blocking(dictionary):
    # store_inverted_index(inverted_index)
    # store_id_name(id_name)
    blocking = dictionary.convert_to_blocking(BLOCK_SIZE)
    store_pickle(blocking, DICTIONARY_BLOCKING)
    #store_json(blocking, DICTIONARY_BLOCKING_JSON)
#前端编码存储
def store_front_coding(dictionary):
    # store_inverted_index(inverted_index)
    # store_id_name(id_name)
    front_coding = dictionary.convert_to_front_coding(BLOCK_SIZE)
    store_pickle(front_coding, DICTIONARY_FrontCoding)
    #store_json(front_coding, DICTIONARY_FrontCoding_JSON)