"""
选择不同的跳表指针步长，并分析其对存储性能/检索效率的影响
"""
import sys
import statistics
pro_dir = r"H:\web\lab1\2025-web-lab1"  # 根据实际情况修改路径
sys.path.append(pro_dir)

import time

from config import *
from index.parse_xml import stemmer, stop_words, normalize_text
from query.load import *
from query.search import bool_search

text = "(app and ap) and (op and p) or (go and back) and (close and home)"
SKIP_STEP = [5,10, 15, 20, 25, 30, 40, 50]
COUNT = 500

for i in range(len(SKIP_STEP)):
    time_1 = []
    PATH = fr"{BASE_PATH}\inverted_index\skip_step_{SKIP_STEP[i]}\inverted_index.pkl"
    id_name = load_pickle(ID_NAME)
    inverted_index = load_pickle(PATH)
    dictionary = Trie.decompress_from_blocking(load_pickle(DICTIONARY_BLOCKING))
    for j in range(COUNT):
        start_time = time.perf_counter()
        search_result = bool_search(text, dictionary, inverted_index, id_name)
        end_time = time.perf_counter()
        time_1.append(end_time - start_time)
    print("跳表指针步长为：",SKIP_STEP[i],"\n","索引检索耗时：",statistics.median(time_1))
    # print("索引检索结果：", search_result)

dictionary, inverted_index, id_name = load() #默认跳表指针步长为sqrt(n)
time_1 = []
for j in range(COUNT):
    start_time = time.perf_counter()
    search_result = bool_search(text, dictionary, inverted_index, id_name)
    end_time = time.perf_counter()
    time_1.append(end_time - start_time)
print("跳表指针步长为：sqrt(n)","\n","索引检索耗时：", statistics.median(time_1))
# print("索引检索结果：", search_result)
