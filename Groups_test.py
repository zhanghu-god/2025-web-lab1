# # 添加 parse_xml.py 所在目录到 Python 路径
# pro_dir = r"H:\web\lab1\2025-web-lab1"  # 根据实际情况修改路径
# sys.path.append(pro_dir)

from gen_inverted_index import *
from query.search import *
from query.load import *

## 生成索引数据
# docs = parse_all(os.path.join(DATA_DIR, "Groups"))
# dictionary, inverted_index, id_name = gen_inverted_index(docs)
# dictionary, inverted_index, id_name = compress_inverted_index(docs)
# store_list(dictionary, inverted_index, id_name)

## load加载索引数据
docs = load_pickle(DOCUMENTS)
dictionary, inverted_index, id_name = load()


## TF-IDF 搜索,不需要输入布尔表达式，直接输入句子就行
while True:
    text = input("请输入查询：")
    if text == "###":
        break
    search_result = bool_search(text, dictionary, inverted_index, id_name)
    print(search_result,"\n")
    TF_IDF_search_not_bool(text, dictionary, inverted_index, id_name, docs)




## 布尔查询，不含跳表指针版本
# text = "(app or ap) and (not pa) or go or back" #例1，注意这里not括号不能省
# text = "app or ap or pa or go or back" #例2
# text = "ap and pa"    #例3
# search_result = bool_search(text, dictionary, inverted_index, id_name)
# print(search_result,"\n")

## 布尔查询，跳表指针版本
# text = "(app or ap) and (not pa) or go or back"
# text = "app or ap or pa or go or back"
# text = "ap and pa"
# search_result = bool_search_skip(text, dictionary, inverted_index, id_name)
# print(search_result,"\n")

## 短语查询
# text =  "closer to"
# search_result = search_phrase(text, dictionary, inverted_index, id_name)
# print(search_result,"\n")


