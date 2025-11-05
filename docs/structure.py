"""
文档内容：
Group:
    共计：783
    有description : 776
Event:
    共计：93512
    有description : 90825
    description有内容：89711
    字典词数(去掉停用词,单纯去掉特殊字符)：207840
    字典词数(去掉停用词,把特殊字符换成空格)：115999
Member:
    共计：82770
RSVPs:
    共计：65128
总计：242193

短语搜索用例：text = "closer to"
测试代码：
# text = "closer to"
# search_result = search_phrase(text, dictionary, inverted_index)
# print("短语搜索：",search_result,"\n")


布尔搜索用例：text = "ap and pa"    text = "go and back"
测试代码：
# text = "back and go"
# search_result = bool_search(text, dictionary, inverted_index, id_name)
# print("search",search_result,"\n")
# search_result_sorted = sorted(search_result)
# search_result_skip = bool_search_skip(text, dictionary, inverted_index, id_name) #跳表指针搜索
# print("search_skip",search_result_skip,"\n")
# if search_result_sorted == search_result_skip:
#     print("skip_search_success")
# else:
#     print("skip_search_fail")


TF-IDF 测试代码
# while True:
#     text = input("请输入查询：")
#     if text == "###":
#         break
#     search_result = bool_search(text, dictionary, inverted_index, id_name)
#     print(search_result,"\n")
#     TF_IDF_search_not_bool(text, dictionary, inverted_index, id_name, docs)



"""#倒排表的结构示例
inverted_index_pre = {
    "meetup": [
        {   #postings，文档ID-位置信息
            0 : [5, 23, 87],
            1 : [1],
            3 : [12, 43],
            5 : [7],
            8 : [9]
        },
        {   #skip_pointers,跳表指针
            0 : 3,
            3 : 8
        }
    ],
    "word":[
        {   #posting，文档ID-位置信息
            0: [5, 23, 87],
            1: [1],
            3: [12, 43],
            5: [7],
            8: [9]
        },
        {   #skip_pointer,跳表指针
            0 : 3,
            3 : 8
        }
    ]
    #...
}
'''倒排表最终结构，词典用trie树存储'''
inverted_index = [
    [
        {   #postings，文档ID-位置信息
            0 : [5, 23, 87],
            1 : [1],
            3 : [12, 43],
            5 : [7],
            8 : [9]
        },
        {   #skip_pointers,跳表指针
            0 : 3,
            3 : 8
        }
    ],
    [
        {   #posting，文档ID-位置信息
            0: [5, 23, 87],
            1: [1],
            3: [12, 43],
            5: [7],
            8: [9]
        },
        {   #skip_pointer,跳表指针
            0 : 3,
            3 : 8
        }
    ]
    #...
]

"""词典按块存储的结构"""
dictionary_blocking = [
    (
        [3,6,133,269],
        0   #第0个word的索引
    ),
    (
        [2,4,7,9],
        16  #第4个word的索引
    ),
    #...
]
long_string = "...7systile9syzygetic8syzygial6syzygy11szaibelyite8szczecin..."

"""词典前端编码结构"""
# 前缀长度 + 第一个单词 + 各个(后缀长度 + 后缀)
long_string = "7automata1e2ic3ion"

'''
数据目录结构
lab1/                               # 数据目录
├── Data/                           # 原始XML数据
│   ├── Group/
│   ├── Event/
│   ├── RSVPs/
│   └── Member/
└── Store/                          # 构建的索引文件
    ├── dictionary/                 # 词典
    │    ├── block_size_10          # 块大小为10的按块存储
    │    ├── block_size_25          # 块大小为25的按块存储
    │    ├── ...
    │    └── dictionary_orin.pkl    # 未压缩顺序存储
    ├── inverted_index/             # 倒排记录表
    │    ├── sqrt/                  # 跳表步长为sqrt(n)
    │    ├── skip_step_10/          # 设置跳表步长为10
    │    ├── skip_step_20/          # 设置跳表步长为20
    │    ├── ...
    │    └── inverted_index_pre.pkl # 原始倒排表,包含词典.
    └── id_name/                    # id-name映射
    
    
2025-web-lab1/ 
├── docs/                           # 文档文件夹 
│   ├── picture/                    # 报告中使用的图片 
│   ├── Lab1_report.md              # 实验报告主文件 
│   └── structure.py                # 结构示例以及统计数据
│
├── index/                          # 索引构建相关模块 
│   ├── Blocking.py                 # 按块存储类
│   ├── Trie.py                     # Trie树数据结构 
│   ├── parse_xml.py                # XML文档解析与文本规范化处理 
│   └── store.py                    # 倒排索引存储相关功能 
│
├── query/                          # 查询相关模块 
│   ├── load.py                     # 加载倒排索引和相关数据结构 
│   └── search.py                   # 实现布尔检索和向量空间模型检索 
│
├── test/                           # 测试相关模块 
│   ├── 1_compress_index.py         # 测试压缩后的索引在存储空间上与原索引的区别
│   ├── 2_bool_sequence.py          # 测试布尔表达式的不同处理顺序对时间开支的影响
│   ├── 3_effi_compress.py          # 测试索引压缩前后在检索效率上的差异
│   └── 4_diff_skip.py              # 测试不同跳表指针步长对索引效率的影响
│
├── gen_inverted_index.py           # 倒排索引生成主程序 
└── Groups_test.py                  # 查询主程序, 包含各类查询的样例
'''