import math

from Trie import Trie
from config import DATA_DIR
from parse_xml import *
from store import store_list, store_blocking, store_front_coding


def split_index(inverted_index_pre):
    dictionary = Trie()   #用trie树存储词典
    inverted_index = []   #倒排表每一个表项也是一个列表，有postings和skip_pointers
        # postings_dict,    包含文档ID和位置信息的字典
        # skip_pointers     跳表指针字典
    for token, data in inverted_index_pre.items():
        #根据token和位置索引构建trie树的节点
        dictionary.insert(token, len(inverted_index))
        inverted_index.append(data)
    return dictionary, inverted_index

def gen_inverted_index(documents):
    doc_id = 0 #文档ID
    id_name = {}  # 文档-ID映射
    inverted_index_pre = {} #初步处理
    # 里面由token和data组成

    #倒排表中填充每个token的postings,文档ID-位置信息
    for doc_name, tokens in documents.items():
        position = 0  # 记录token在文档中的位置
        for token in tokens:
            if token not in inverted_index_pre:
                #构建token的posting字典
                inverted_index_pre[token] = []
                postings = {}
                positions = [position]
                postings[doc_id] = positions #文档ID-位置信息
                inverted_index_pre[token].append(postings)
                #实质上形成 inverted_index_pre[token][postings] = [ {doc_id: [position]} ]
            elif doc_id in inverted_index_pre[token][0]:
                #已有doc_id，添加位置信息
                inverted_index_pre[token][0][doc_id].append(position)
            else:
                #已有token，但无doc_id，添加doc_id和位置信息
                positions = [position]
                inverted_index_pre[token][0][doc_id] = positions
            position += 1
        id_name[doc_id] = doc_name
        doc_id += 1
    # 填充skip pointers
    # 这里的data就代表了postings_dict（0）和skip_pointers（1）
    for token, data in inverted_index_pre.items():
        postings_dict = data[0]
        #doc_id转换成列表便于用位置索引
        doc_ids = list(postings_dict.keys())
        n = len(doc_ids)
        skip_pointers = {}
        if n > 3:
            #跳表指针步长是根号n
            skip_step = int(math.sqrt(n))
            for i in range(0, n, skip_step):
                if i + skip_step < n:
                    from_doc = doc_ids[i]
                    to_doc = doc_ids[i + skip_step]
                    skip_pointers[from_doc] = to_doc
        data.append(skip_pointers)
    # 按字母排序
    inverted_index_pre = dict(sorted(inverted_index_pre.items()))
    dictionary, inverted_index = split_index(inverted_index_pre)
    return dictionary, inverted_index, id_name


def compress_inverted_index(documents):#压缩倒排表,位置-GAP
    doc_id = 0 #文档ID
    id_name = {}  # 文档-ID映射
    inverted_index_pre = {} #初步处理
    # 里面由token和data组成

    #倒排表中填充每个token的postings,文档ID-位置信息
    for doc_name, tokens in documents.items():
        position = 0  # 记录token在文档中的位置
        for token in tokens:
            if token not in inverted_index_pre:
                #构建token的posting字典
                inverted_index_pre[token] = []
                postings = {}
                positions = [position]
                postings[doc_id] = positions #文档ID-位置信息
                inverted_index_pre[token].append(postings)
                #实质上形成 inverted_index_pre[token][postings] = [ {doc_id: [position]} ]
            elif doc_id in inverted_index_pre[token][0]:
                #已有doc_id，添加位置信息
                gap = position - inverted_index_pre[token][0][doc_id][-1]
                 #即求间隔
                inverted_index_pre[token][0][doc_id].append(gap)
            else:
                #已有token，但无doc_id，添加doc_id和位置信息
                positions = [position]
                inverted_index_pre[token][0][doc_id] = positions
            position += 1
        id_name[doc_id] = doc_name
        doc_id += 1
    # 填充skip pointers
    # 这里的data就代表了postings_dict（0）和skip_pointers（1）
    for token, data in inverted_index_pre.items():
        postings_dict = data[0]
        #doc_id转换成列表便于用位置索引
        doc_ids = list(postings_dict.keys())
        n = len(doc_ids)
        skip_pointers = {}
        if n > 3:
            #跳表指针步长是根号n
            skip_step = int(math.sqrt(n))
            for i in range(0, n, skip_step):
                if i + skip_step < n:
                    from_doc = doc_ids[i]
                    to_doc = doc_ids[i + skip_step]
                    skip_pointers[from_doc] = to_doc
        data.append(skip_pointers)
    # 按字母排序
    inverted_index_pre = dict(sorted(inverted_index_pre.items()))
    dictionary, inverted_index = split_index(inverted_index_pre)
    return dictionary, inverted_index, id_name

if __name__ == "__main__":
    #找到正确的数据目录
    file_type="Event"
    folder = os.path.join(DATA_DIR, file_type)
    #解析全部文件生成正排表(文档name-tokens)
    documents = parse_all(folder)
    #生成倒排表同时保存文档id-name映射
    dictionary, inverted_index, id_name= gen_inverted_index(documents)
    #保存倒排表
    #未压缩直接存储
    store_list(dictionary, inverted_index, id_name)
    store_blocking(dictionary)
    store_front_coding(dictionary)
    # # 打印文档数量
    # print(f"共处理 {len(documents)} 篇文档")
    # # 看看第一个文档的 tokens
    # first_doc = next(iter(documents.items()))
    # print("示例文档:", first_doc[0])
    # print("分词结果:", first_doc[1])  # 打印前50个 token

