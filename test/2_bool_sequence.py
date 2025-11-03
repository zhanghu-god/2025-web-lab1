"""
分析同一个布尔表达式的不同处理顺序对时间开支的影响
"""
import sys

pro_dir = r"H:\web\lab1\2025-web-lab1"  # 根据实际情况修改路径
sys.path.append(pro_dir)

import time
from gen_inverted_index import *
from query.search import *
from query.load import *


# text_1 = "(app or ap) and (not pa) and (go or back)"
# text_2 = "(go or back) and (not pa) and (app or ap)"
text_1 = "go and back and app"
text_2 = "app and go and back"


docs = load_pickle(DOCUMENTS)
dictionary, inverted_index, id_name = load()

start = time.perf_counter()
search_result_1 = bool_search(text_1, dictionary, inverted_index, id_name)
time_1 = time.perf_counter() - start

start = time.perf_counter()
search_result_1_skip = bool_search_skip(text_1, dictionary, inverted_index, id_name)
time_1_skip = time.perf_counter() - start

start = time.perf_counter()
search_result_2 = bool_search(text_2, dictionary, inverted_index, id_name)
time_2 = time.perf_counter() - start

start = time.perf_counter()
search_result_2_skip = bool_search_skip(text_2, dictionary, inverted_index, id_name)
time_2_skip = time.perf_counter() - start

print("bool_search:","\n")
print(text_1, ":", time_1)
print("bool_search_result_1:",search_result_1,"\n")
print(text_2, ":", time_2)
print("bool_search_result_2:",search_result_2,"\n")
print("bool_search_skip:","\n")
print(text_1, ":", time_1_skip)
print("bool_search_skip_result_1:",search_result_1_skip,"\n")
print(text_2, ":", time_2_skip)
print("bool_search_skip_result_2:",search_result_2_skip,"\n")

