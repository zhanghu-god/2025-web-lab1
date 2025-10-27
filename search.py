import math

from Trie import Trie
from config import DATA_DIR
from parse_xml import *
from store import store_list, store_blocking


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
                # while stack and stack[-1] in {'and', 'or', 'not'}:
                #     output.append(stack.pop())
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
                if tree_stack==[] or tree_stack[-1]['type']!='term':
                    tree_stack.append(elem)
                else:
                    tree_stack[-1]['value'].append(elem['value'][0])###########改动1
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
    

def search_word(word,dictionary, inverted_index):#word是输入的单个查询单词
    posting_index = dictionary.search(word)
    if posting_index != -1:
        file_ids = list(inverted_index[posting_index][0].keys())
        print(word,":",file_ids,"\n")
    else:
        file_ids = []
    return file_ids

#####################改动3
def search_words(words,dictionary, inverted_index):#word是输入的单个查询单词
    count = 0
    for word in words:
        temp = search_word(word,dictionary, inverted_index)
        if(word==words[0]):
            file_ids = temp
        else:
            file_ids = AND(file_ids,temp)
        count += 1
    #汇总了同时含有短语所有单词的文档
    results_ids = []
    for id in file_ids:
        for position in words[0][id]:
            flag = 0
            for i in range(1,count-1,1):
                if(position+i not in words[i][id]):
                    break
                else:
                    flag += 1
            if flag == count-1:
                results_ids.append(id)
                break
    return  results_ids
        


def AND(arr1, arr2):
    return list(set(arr1) & set(arr2))

def OR(arr1, arr2):
    return list(set(arr1) | set(arr2))

def NOT(arr1, arr2):#返回arr1中有arr2中没有的元素
    return list(set(arr1) - set(arr2))

def recursive_search(tree, dictionary, inverted_index, id_name_list):
    # """递归计算布尔表达式语法树"""
    if tree['type'] == 'term':
        if tree['value'][1]!=None:####################改动2
            return search_words(tree['value'], dictionary, inverted_index)
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



def bool_search(text, dictionary, inverted_index, id_name):#text是输入的查询文本
    tokens = bool_evaluator(text)
    tree = _build_syntax_tree(tokens)
    id_name_list = list(id_name.keys())
    return recursive_search(tree, dictionary, inverted_index, id_name_list)


    



