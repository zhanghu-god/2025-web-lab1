import math

from index.parse_xml import *


def bool_evaluator(text):
    #小写
    text=text.lower()
    # 去掉特殊符号（保留单词和空格,和括号）
    text = html.unescape(text)  # 转回 <p>Our purpose:</p>
    text = re.sub(r"<.*?>", "", text)  # 去掉 <p> 和 </p>
    text = re.sub(r"[^a-z\s()]", " ",  text) #把除了字母和空白符号的其他符号换成空格
    # 分词
    tokens = word_tokenize(text)#分词
    clean_tokens = []
    for word in tokens:
        if word not in stop_words:
            clean_tokens.append(stemmer.stem(word))
        elif word=='or' or word=='and' or word=='not'and clean_tokens[-1] not in ['or','and','not'] :#暂时每个运算都得带上括号
            clean_tokens.append(word)
    return clean_tokens
def _build_syntax_tree(tokens):
        # """构建抽象语法树 (使用Shunting-yard算法)"""
        output = []
        stack = []
        
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # 弹出左括号
            elif token in {'and', 'or'}:
                while stack and stack[-1] in {'and', 'or', 'not'}:#必须有这个才能获得正确的计算顺序
                    output.append(stack.pop())
                stack.append(token)
            elif token == 'not':
                stack.append(token)
            else:  # 词项
                output.append({
                    'type': 'term',
                    # 'parent': None,
                    'value': [token]
                    })
        
        # 弹出剩余运算符
        while stack:
            output.append(stack.pop())
        
        # 构建树结构
        tree_stack = []
        for elem in output:
            if isinstance(elem, dict):  # 词项
                # if tree_stack==[] or  (len(tree_stack)>2 and (tree_stack[-1]['type']!='term' or tree_stack[-2]['type']!='term')) or len(tree_stack)<2:
                #     tree_stack.append(elem)
                # else:
                #     tree_stack[-1]['value'].append(elem['value'][0])###########改动1
                tree_stack.append(elem)
            elif elem == 'not':
                operand = tree_stack.pop()
                tree_stack.append({
                    'type': 'operator',
                    # 'parent': None,
                    'operator': 'not',
                    'operand': operand
                })
            else:  # and/or
                right = tree_stack.pop()
                left = tree_stack.pop()
                tree_stack.append({
                    'type': 'operator',
                    # 'parent': None,
                    'operator': elem,
                    'left': left,
                    'right': right
                })
                # left.parent = tree_stack[-1]
                # right.parent = tree_stack[-1]
        
        return tree_stack[0] if tree_stack else None
    

def search_word(word,dictionary, inverted_index):#word是输入的单个查询单词，这里只返回了倒排表内的id
    posting_index = dictionary.search(word)
    if posting_index != -1:
        file_ids = list(inverted_index[posting_index][0].keys())
    else:
        file_ids = []
    # print(word,":",file_ids,"\n")
    return file_ids

# 跳表指针对应的search_word函数，直接返回一个倒排表字典
def search_word_skip(word,dictionary, inverted_index):
    posting_index = dictionary.search(word)
    return inverted_index[posting_index]

# 倒排表：1.id[位置]，2.跳表指针




        


def AND(arr1, arr2):
    return list(set(arr1) & set(arr2))

def AND_SKIP(inverted_index_1,inverted_index_2):#使用跳表指针的优化合并，参数改为两个倒排表。
    temp_1 = list(inverted_index_1[0].keys())
    temp_2 = list(inverted_index_2[0].keys())
    temp_skip_1 = list(inverted_index_1[1].values())
    temp_skip_2 = list(inverted_index_2[1].values())
    length_1 = len(temp_1)
    length_2 = len(temp_2)
    results_ids = []

    i = 0
    j = 0
    while 1:
        if temp_1[i] < temp_2[j]:
            if temp_1[i] in temp_skip_1:
                for temp_id in temp_skip_1:
                    if temp_id < temp_2[j]:
                        i = temp_1.index(temp_id)+1
                    elif temp_id == temp_2[j]:
                        results_ids.append(temp_id)
                        i = temp_1.index(temp_id)+1
                        j += 1
                    else:
                        break
            else:
                i += 1 
        elif temp_2[j] < temp_1[i]:
            if temp_2[j] in temp_skip_2:
                for temp_id in temp_skip_2:
                    if temp_id < temp_1[i]:
                        j = temp_2.index(temp_id)+1
                    elif temp_id == temp_1[i]:
                        results_ids.append(temp_id)
                        j = temp_2.index(temp_id)+1
                        i += 1
                    else:
                        break
            else:
                j += 1
        elif temp_1[i] == temp_2[j]:
            results_ids.append(temp_1[i])
            i += 1
            j += 1
        if i >= length_1-1 or j >= length_2-1:
            break
    return results_ids



def OR(arr1, arr2):
    return list(set(arr1) | set(arr2))

def NOT(arr1, arr2):#返回arr1中有arr2中没有的元素
    return list(set(arr1) - set(arr2))

def recursive_search(tree, dictionary, inverted_index, id_name_list):
    # """递归计算布尔表达式语法树"""
    if tree['type'] == 'term':
        return search_word(tree['value'][0], dictionary, inverted_index)
    elif tree['type'] == 'operator':
        if tree['operator'] == 'and':
            left_result = recursive_search(tree['left'], dictionary, inverted_index, id_name_list)
            right_result = recursive_search(tree['right'], dictionary, inverted_index, id_name_list)
            return AND(left_result, right_result)
        elif tree['operator'] == 'or':
            left_result = recursive_search(tree['left'], dictionary, inverted_index, id_name_list)
            right_result = recursive_search(tree['right'], dictionary, inverted_index, id_name_list)
            return OR(left_result, right_result)
        elif tree['operator'] == 'not':
            operand_result = recursive_search(tree['operand'], dictionary, inverted_index, id_name_list)
            return NOT(id_name_list, operand_result)

def recursive_search_skip(tree, dictionary, inverted_index, id_name_list):
    # """递归计算布尔表达式语法树"""
    if tree['type'] == 'term':
        return search_word_skip(tree['value'][0], dictionary, inverted_index)
    elif tree['type'] == 'operator':
        if tree['operator'] == 'and':
            if tree['left']['type'] == 'term' and tree['right']['type'] == 'term':
                left_result = recursive_search_skip(tree['left'], dictionary, inverted_index, id_name_list)
                right_result = recursive_search_skip(tree['right'], dictionary, inverted_index, id_name_list)     
                return AND_SKIP(left_result, right_result)
            else:     
                left_result = recursive_search_skip(tree['left'], dictionary, inverted_index, id_name_list)
                right_result = recursive_search_skip(tree['right'], dictionary, inverted_index, id_name_list)
                return AND(left_result, right_result)
        elif tree['operator'] == 'or':
            left_result = recursive_search_skip(tree['left'], dictionary, inverted_index, id_name_list)
            right_result = recursive_search_skip(tree['right'], dictionary, inverted_index, id_name_list)
            return OR(left_result, right_result)
        elif tree['operator'] == 'not':
            operand_result = recursive_search_skip(tree['operand'], dictionary, inverted_index, id_name_list)
            return NOT(id_name_list, operand_result)




def bool_search(text, dictionary, inverted_index, id_name):#text是输入的查询文本
    tokens = bool_evaluator(text)
    tree = _build_syntax_tree(tokens)
    id_name_list = list(id_name.keys())
    return recursive_search(tree, dictionary, inverted_index, id_name_list)


def bool_search_skip(text, dictionary, inverted_index, id_name):#text是输入的查询文本
    tokens = bool_evaluator(text)
    tree = _build_syntax_tree(tokens)
    id_name_list = list(id_name.keys())
    return recursive_search_skip(tree, dictionary, inverted_index, id_name_list)



####TF-IDF
def count_words(doc,id,id_name):#计算文档总的含词数
    count = 0
    for word in doc[id_name[id]]:
        count += 1
    return count

    
#计算词频
def compute_tf(text,dictionary, inverted_index,id_name,doc,id):
    #tf是相对于每一篇文档而言的，即该单词在该文档中出现的次数/该文档的长度
    #doc为所代表文档集合的正排表
    #这里计算了一个词在一个文档（id）中的词频
    #返回一个字典，只不过只有一个键值对
    position_index = dictionary.search(text)
    tf_text={}
    if id not in inverted_index[position_index][0]:
        tf_text[id] = 0
        return tf_text
    else:
            text_len = len(inverted_index[position_index][0][id])
            id_len = count_words(doc,id,id_name)
            tf_text[id] = float(text_len)/float(id_len)
            # tf_text[id] = float(text_len)
    return tf_text

def cosine_similarity(vec1, vec2):
    #"""计算两个向量的余弦相似度"""
    # 点积
    dot_product = sum(float(a) * float(b) for a, b in zip(vec1, vec2))

    # print(dot_product,"\n")
    
    # 向量模长
    magnitude1 = math.sqrt(sum(float(a)**2 for a in vec1))
    magnitude2 = math.sqrt(sum(float(a)**2 for a in vec2))
    
    # print(magnitude1,"\n")
    # print(magnitude2,"\n")

    # print(dot_product / (magnitude1 * magnitude2),"\n")
    # 避免除零错误
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)



# 计算逆文档频率
def compute_idf(doc,text,dictionary,inverted_index):#doc代表一个文档集合,这里只计算一个单词的逆文档频率
    text_idf = 0
    N = len(doc)
    ids_text = search_word(text,dictionary, inverted_index)
    df = len(ids_text)
    if df == 0:
        return 0.0
    text_idf = math.log10(float(N) / float(df))
    return text_idf

# 计算TF-IDF
def compute_tf_idf(text,id,doc,dictionary,inverted_index,id_name):#单词text，文档id
    tf_idf = 0
    text_idf = compute_idf(doc,text,dictionary,inverted_index)
    tf_text = compute_tf(text,dictionary, inverted_index,id_name,doc,id)
    tf_idf = tf_text[id] * text_idf#每个文档对应的tf-idf,
    return tf_idf

# 计算输入文本当中词的tf
def compute_texts_tf(texts):
    count = {}
    for word in texts:
        # if word not in count:
        #    # count.update({word: 1})
        #     #count[word]=1 #可以直接赋值，会自动生成新的键值对，update则会合并新旧字典（重复直接覆盖）
        # else:
        #     count[word] += 1
        count[word] = count.get(word, 0) + 1
    len_texts = len(texts)
    word_tf = {}
    for word in count:
        # temp = float(count[word])/float(len_texts)
        # temp = float(count[word])
        temp = float(count[word])*0.5+float(count[word])/float(len_texts)
        word_tf[word] = temp
    return word_tf

    


#注意这里需要bool的最终搜索结果来确定需要参与计算的文档长度
#对一定的文档集合进行检索

def TF_IDF_search(texts_original,ids,dictionary, inverted_index,id_name,doc):
    # 对输入的文本进行预处理,即分词和规范化
    texts = normalize_text(texts_original)

    word_texts_tf = compute_texts_tf(texts)

    if not ids:  # 如果输入的文本为空，则返回空字典
        return print("No results found.")

    tf_idf = 0
    vec = {}
    vec_search = []
    for id in ids:
        vec[id]=[]
        for text in texts:
            tf_idf=compute_tf_idf(text,id,doc,dictionary, inverted_index,id_name)
            vec[id].append(tf_idf)
    for text in texts:
        idf_search = compute_idf(doc,text,dictionary, inverted_index)
        #三种情况都可以
        ##有点问题，需要计算重复的词
        # tf_search = float(1)/float(len(texts))#即搜索词在搜索文本中的词频
        # tf_search = float(1)
        # tf_search = 0.5*float(1) + 0.5*float(1)/float(len(text))
        tf_search = word_texts_tf[text]
        vec_search.append(idf_search*tf_search)
    results = {}
    for id in ids:
        sim = cosine_similarity(vec[id],vec_search)
        # print(vec[id],"\n")
        # print(vec_search,"\n")
        # print(sim,"\n")
        results[id]=sim
    # 按相似度降序排序（从高到低）
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    # 输出排序结果
    for rank, (doc_id, score) in enumerate(sorted_results, 1):
        if rank > 100:
            break
        print(f"Rank {rank}: Document {doc_id} (Score: {score:.16f})")

    # ​​results.items()​​
    # 将字典 results转换为可迭代的 (doc_id, score)元组列表，例如：
    # [('doc3', 0.9746), ('doc1', 0.9144), ('doc2', 0.6710)]
    # ​​key=lambda x: x[1]​​
    # 指定排序依据为元组的第二个元素（即相似度分数 score）。
    # ​​reverse=True​​
    # 按降序排列（从高到低），使得最相关的文档排在前面。



# 直接对一个文档或一句文本进行TF-IDF搜索，只能说明文档相似性，感觉最终还是需要一个确定的文档集。
# 但是如何获得该文档集呢？
# 感觉还是得布尔搜索，只不过全是and而已
# 如果不用布尔搜索，则需要？
# 究竟需要在多大的文档集当中检索？感觉可以表示成布尔表达式
# 这里指的一串句子，不需要输入布尔表达式

def TF_IDF_search_not_bool(texts_original,dictionary, inverted_index,id_name,doc):
    # 对输入的文本进行预处理,即分词和规范化
    texts_origin = normalize_text(texts_original)
    #更改为布尔检索模式
    texts = ""
    i=0
    len_texts = len(texts_origin)
    for text in texts_origin:
        texts += text
        i+=1
        if i<len_texts:
            texts+= " or " ##这里需要的是and还是or
    print(texts)
    ids = bool_search(texts,dictionary, inverted_index, id_name)
    print(ids)
    TF_IDF_search(texts_original,ids,dictionary, inverted_index,id_name,doc)











#####################下面是可以处理短语的部分############
def evaluator(text):
    #小写
    text=text.lower()
    # 去掉特殊符号（保留单词和空格,和括号）
    text = html.unescape(text)  # 转回 <p>Our purpose:</p>
    text = re.sub(r"<.*?>", "", text)  # 去掉 <p> 和 </p>
    text = re.sub(r"[^a-z\s()]", " ",  text) #把除了字母和空白符号的其他符号换成空格
    # 分词
    tokens = word_tokenize(text)#分词
    clean_tokens = []
    for word in tokens:
        clean_tokens.append(stemmer.stem(word))#词干化
    return clean_tokens

def search_phrase(text,dictionary, inverted_index):
    tokens = evaluator(text)
    ids = []
    count = 0 #计数，计算短语中单词的个数
    for word in tokens:
        ids_text = search_word(word,dictionary, inverted_index) #问题1：无法使用跳表指针，只有都是倒排表才能用
        if ids_text == []:
            print("没有找到该短语")
            return []
        elif count == 0:
            ids = ids_text
            count += 1
        else:
            count += 1
            ids = AND(ids,ids_text)
    #汇总了同时含有短语所有单词的文档
    result_ids = []
    position_index = []
    for word in tokens:
        position_index.append(dictionary.search(word))
    for id in ids:
        print("id:",id,"\n")
        for position in inverted_index[position_index[0]][0][id]:
            print("position:",position,"\n")
            flag = 0
            for i in range(1,count,1):#注意这里不包含右边界
                if(position+i not in inverted_index[position_index[i]][0][id]):
                    # print("closer对应的文档位置",inverted_index[position_index[i-1]][0][id],"\n")
                    # print("to对应的文档位置",inverted_index[position_index[i]][0][id],"\n")
                    break
                else:
                    flag += 1
            # print("flag：",flag,"\n")
            if flag == count-1:
                # print("flag：",flag,"\n")
                # print("id:",id,"\n")
                result_ids.append(id)
                break
    # print("text:",text,"\n")
    # print("tokens:",tokens,"\n")
    # print("position_index:",position_index,"\n")
    # print("ids:",ids,"\n")
    # print("position:",position,"\n")
    # print("flag:",flag,"\n")
    # print("count:",count,"\n")
    # print("短语搜索结果：",result_ids)
    return  result_ids




