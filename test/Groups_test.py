import html
import re
import sys
import os

# 添加 parse_xml.py 所在目录到 Python 路径
pro_dir = r"H:\web\lab1\project"  # 根据实际情况修改路径
sys.path.append(pro_dir)

from parse_xml import*
from config import *
from gen_inverted_index import *
from search import *
from nltk import word_tokenize

docs = parse_all(os.path.join(DATA_DIR, "Groups"))
# dictionary, inverted_index, id_name = gen_inverted_index(docs)
dictionary, inverted_index, id_name = compress_inverted_index(docs)
store_list(dictionary, inverted_index, id_name)

text = "app pa"
search_result = bool_search(text, dictionary, inverted_index, id_name)
print(search_result)