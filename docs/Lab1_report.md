### 1.文档解析与规范化处理

**实现文件为 parse_xml.py**
总体采用NTLK库对文档进行解析和规范化处理

1. 获取文档对应字段（这里是description字段），函数：parse_group_file(filepath)
2. 规范化处理，函数：normalize_text(text)，最终返回一个规范的分词列表clean_tokens，处理步骤如下：
    1. 小写
    2. 去除特殊符号
    3. 分词
    4. 去除停用词&词干化
3. 为了方便短语处理，额外构建了一个不排除停用词的处理函数：normalize_text_full(text)，处理步骤如下：
    1. 小写
    1. 去除特殊符号
    1. 分词
    1. 词干化
### 2.倒排表的构建

**实现文件为 gen_inverted_index.py,Trie.py**
分为正排表构建，词典构建和倒排表构建等步骤

* 正排表结构:  

  ```python
  docs = {
      file1:[word1, word2, ...],
      file2:[word3, word4, ...],
      ...
  }
  ```

* 倒排表构建以及查询时词典的结构都主要是 Trie 树，其结构如下：
  
  <svg width="800" height="450" version="1.1" xmlns="http://www.w3.org/2000/svg">
  	<ellipse stroke="black" stroke-width="1" fill="none" cx="371.5" cy="69.5" rx="30" ry="30"/>
  	<ellipse stroke="black" stroke-width="1" fill="none" cx="249.5" cy="155.5" rx="30" ry="30"/>
  	<text x="245.5" y="161.5" font-family="Times New Roman" font-size="20">t</text>
  	<ellipse stroke="black" stroke-width="1" fill="none" cx="377.5" cy="207.5" rx="30" ry="30"/>
  	<text x="371.5" y="213.5" font-family="Times New Roman" font-size="20">a</text>
  	<ellipse stroke="black" stroke-width="1" fill="none" cx="512.5" cy="155.5" rx="30" ry="30"/>
  	<text x="509.5" y="161.5" font-family="Times New Roman" font-size="20">i</text>
  	<ellipse stroke="black" stroke-width="1" fill="none" cx="154.5" cy="266.5" rx="30" ry="30"/>
  	<text x="148.5" y="272.5" font-family="Times New Roman" font-size="20">o</text>
  	<ellipse stroke="black" stroke-width="1" fill="none" cx="287.5" cy="281.5" rx="30" ry="30"/>
  	<text x="282.5" y="287.5" font-family="Times New Roman" font-size="20">e</text>
  	<ellipse stroke="black" stroke-width="1" fill="none" cx="200.5" cy="362.5" rx="30" ry="30"/>
  	<text x="194.5" y="368.5" font-family="Times New Roman" font-size="20">a</text>
  	<ellipse stroke="black" stroke-width="1" fill="none" cx="287.5" cy="393.5" rx="30" ry="30"/>
  	<text x="281.5" y="399.5" font-family="Times New Roman" font-size="20">d</text>
  	<ellipse stroke="black" stroke-width="1" fill="none" cx="377.5" cy="362.5" rx="30" ry="30"/>
  	<text x="370.5" y="368.5" font-family="Times New Roman" font-size="20">n</text>
  	<ellipse stroke="black" stroke-width="1" fill="none" cx="559.5" cy="266.5" rx="30" ry="30"/>
  	<text x="552.5" y="272.5" font-family="Times New Roman" font-size="20">n</text>
  	<ellipse stroke="black" stroke-width="1" fill="none" cx="491.5" cy="362.5" rx="30" ry="30"/>
  	<text x="484.5" y="368.5" font-family="Times New Roman" font-size="20">n</text>
  	<polygon stroke="black" stroke-width="1" points="346.98,86.785 274.02,138.215"/>
  	<polygon fill="black" stroke-width="1" points="274.02,138.215 283.44,137.693 277.678,129.519"/>
  	<polygon stroke="black" stroke-width="1" points="372.803,99.472 376.197,177.528"/>
  	<polygon fill="black" stroke-width="1" points="376.197,177.528 380.845,169.319 370.854,169.753"/>
  	<polygon stroke="black" stroke-width="1" points="397.112,85.121 486.888,139.879"/>
  	<polygon fill="black" stroke-width="1" points="486.888,139.879 482.662,131.444 477.455,139.981"/>
  	<polygon stroke="black" stroke-width="1" points="229.993,178.292 174.007,243.708"/>
  	<polygon fill="black" stroke-width="1" points="174.007,243.708 183.007,240.881 175.41,234.379"/>
  	<polygon stroke="black" stroke-width="1" points="258.162,184.222 278.838,252.778"/>
  	<polygon fill="black" stroke-width="1" points="278.838,252.778 281.315,243.675 271.741,246.562"/>
  	<polygon stroke="black" stroke-width="1" points="265.543,301.943 222.457,342.057"/>
  	<polygon fill="black" stroke-width="1" points="222.457,342.057 231.719,340.266 224.905,332.947"/>
  	<polygon stroke="black" stroke-width="1" points="287.5,311.5 287.5,363.5"/>
  	<polygon fill="black" stroke-width="1" points="287.5,363.5 292.5,355.5 282.5,355.5"/>
  	<polygon stroke="black" stroke-width="1" points="309.799,301.569 355.201,342.431"/>
  	<polygon fill="black" stroke-width="1" points="355.201,342.431 352.6,333.363 345.91,340.796"/>
  	<polygon stroke="black" stroke-width="1" points="542.159,290.981 508.841,338.019"/>
  	<polygon fill="black" stroke-width="1" points="508.841,338.019 517.545,334.381 509.385,328.601"/>
  	<polygon stroke="black" stroke-width="1" points="524.197,183.126 547.803,238.874"/>
  	<polygon fill="black" stroke-width="1" points="547.803,238.874 549.288,229.558 540.079,233.457"/>
  </svg>
  
* 倒排表结构: 
```python
'''倒排表最终结构，词典被分开用trie树存储'''
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
    #...
]
```
1. 构建正排表，函数：parse_all(folder)，结果返回一个字典，处理步骤如下：
   1. 遍历文件夹下的所有文件获取规范化处理的各个字段
   2. 构建正排表，将字段值作为value，文件名作为key

     > 注意这里同样有函数parse_all_full(folder)来获取不排除停用词的正排表
2. 构建倒排表，函数：gen_inverted_index(documents)，结果返回一个字典，处理步骤如下：
   1. 通过正排表来获取文档名和字段信息
   2. 遍历每个字段，将每个词存入倒排表中，记录词出现的位置：field_id:[positions]，同时补全id_name的内容。（即倒排表当中存储的时文件id，实际文件名需要后续通过id_name提取）
   3. 遍历倒排表，设置跳表指针，有固定长度指针，也有sqrt(n)长度指针 
3. 还另外设置了函数：compress_inverted_index(documents)来构建压缩倒排表，这里的压缩指的是把词项在文档当中的位置信息改为了两次出现的间隔。
   * 具体操作与gen_inverted_index(documents)一致，只在存入位置信息时做了修改，改为了存储间隔。
4. 通过split_index(inverted_index_pre)函数将初步生成的结果分成两个部分，即词典和倒排表。（inverted_index_pre当中仍然通过token进行索引，通过该函数可以实现拆分，使得字典当中存储的是token以及其对应的倒排索引，而倒排表当中存储的是则完全是倒排索引所对应的词项位置信息）

### 3.倒排表的扩展与优化 [todo3]

#### 1.在倒排表中加入词项的位置信息，以应对短语检索需求。

> 词项的位置信息在上一步构建倒排表中已经添加。具体实现也已经介绍过。

#### 2.任选两种课程中介绍过的索引压缩方法加以实现，如按块存储、前端编码等，并比较压缩后的索引在存储空间上与原索引的区别。

- 实现了按块存储、前端编码两种索引压缩方法, 存储结构如下:

  > 查询时词典主要采用 Trie 树结构, 对于 Trie 树的压缩和解压函数写在了 Trie 类里

  1. 顺序存储

     > 词典列表和倒排索引(词项对应的倒排表的索引下标)的列表

     ```py
     [word1, word2, ...]
     [pos1, pos2, ...]
     ```

  2. 按块存储

     > 两个部分:
     >
     > 1. 块的信息(存储倒排索引以及对应块在长字符串中的索引), 
     > 2. 长字符串(每个词项由词项长度分割)

     ```python
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
     ```

  3. 前端编码

     > 两个部分:
     >
     > 1. 块的信息, 
     > 2. 长字符串(每个词项由词项长度分割)

     `````python
     """词典前端编码结构"""
     dictionary_fronting = dictionary_blocking  #块的信息和按块存储结构一样
     # 前缀长度 + 第一个单词 + 各个(后缀长度 + 后缀)
     long_string = "7automata1e2ic3ion"
     `````

- 压缩后的索引在存储空间上与原索引的区别测试如下:

  <img src="picture/test_1.png" style="zoom: 50%;" />

- 通过输出结果可以看到按块存储压缩后节约了将近 $10\%$的空间，而前段编码的压缩方式又在前段编码的基础上节约了大约$15\%-20\%$ 的空间。

  > 同时可以发现块大小的增加对于空间节约方面收益不多, 而对于检索效率可能产生较大影响.

### 4.多种形式的信息检索

**实现文件为 search.py**

#### 1.布尔检索

#### 2.向量空间模型