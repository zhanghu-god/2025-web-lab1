# # 添加 parse_xml.py 所在目录到 Python 路径
# pro_dir = r"H:\web\lab1\2025-web-lab1"  # 根据实际情况修改路径
# sys.path.append(pro_dir)

from gen_inverted_index import *
from query.load import load
from query.search import *

docs = parse_all(os.path.join(DATA_DIR, "Event"))
docs1 = load_pickle(DOCUMENTS)
if(docs == docs1):
    print("词典相同")

# dictionary, inverted_index, id_name = gen_inverted_index(docs)
# dictionary, inverted_index, id_name = compress_inverted_index(docs)
dictionary, inverted_index, id_name = load()
# store_list(dictionary, inverted_index, id_name)

# text = "back and go"

# search_result = bool_search(text, dictionary, inverted_index, id_name)

# ##布尔搜索还有问题


# print(search_result,"\n")

# ##目前还没有短语检测机制，快弄

# TF_IDF_search(text, search_result, dictionary, inverted_index, id_name, docs)

# text = "app or ap or pa or go or back"
# search_result = bool_search(text, dictionary, inverted_index, id_name)
# print(search_result,"\n")

# text = "app ap pa go back"

while True:
    text = input("请输入查询：")
    if text == "###":
        break
    search_result = bool_search(text, dictionary, inverted_index, id_name)
    print(search_result,"\n")
    TF_IDF_search_not_bool(text, dictionary, inverted_index, id_name, docs)

# text = "ap and pa"
# search_result = bool_search(text, dictionary, inverted_index, id_name)
# print(search_result,"\n")

# TF_IDF_search_not_bool(text, dictionary, inverted_index, id_name, docs)

