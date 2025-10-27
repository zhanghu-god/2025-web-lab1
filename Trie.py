class TrieNode:
    def __init__(self):
        self.children = {} # 子节点
        self.is_end_of_word = False  # 标记是否是一个单词的结尾
        self.posting_index = -1 #对应的倒排表位置索引

class Trie:
    def __init__(self):
        self.root = TrieNode() #初始化根节点，没有对应的字符
        self.count = 0 #记录插入的单词数量

    #插入一个单词
    def insert(self, word, posting_index):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.posting_index = posting_index
        self.count += 1

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children :
                return -1
            node = node.children[char]
        return node.posting_index if node.is_end_of_word else -1  # 返回倒排表的索引位置

    #递归遍历Trie树，提取字符以及倒排表索引
    # node：当前遍历的Trie节点（初始调用时通常传入根节点 self.root）。
    # prefix：从根节点到当前节点的路径构成的字符串（初始为空字符串 ""）。
    # words：用于保存所有完整单词的列表（​​按引用传递​​，递归过程中填充结果）。
    # posting_indexes：用于保存所有单词对应的倒排表索引的列表（与words一一对应）。
    def extract_words(self, node, prefix, words, posting_indexes):
        if node.is_end_of_word:
            words.append(prefix)
            posting_indexes.append(node.posting_index)  # 记录倒排表索引
        for char, child in node.children.items():#char是当前节点的键，child是当前节点的值，字典键值对
            self.extract_words(child, prefix + char, words, posting_indexes)

    '''以下是几种将字典压缩和解压的方式'''
    #顺序存储
    def convert_to_list(self):
        words = []
        posting_indexes = []
        self.extract_words(self.root, "", words, posting_indexes)
        return words, posting_indexes
    @staticmethod
    def decompress_from_list(words, posting_indexes):
        trie = Trie()
        for i, word in enumerate(words):
            trie.insert(word, posting_indexes[i])
        return trie

    #将Trie树转化成按块存储的形式
    def convert_to_blocking(self, block_size):
        # 提取所有词项及其倒排表位置索引
        words = []
        posting_indexes = []
        self.extract_words(self.root, "", words, posting_indexes)
        # 拼接所有词项成一个长字符串
        long_string = ""
        blocks = []  #最终返回的blocking结构
        index = 0   #long_string里的索引,从0开始
        posting_ptr = [] #块内倒排表索引的列表
        cnt = 0
        for i, word in enumerate(words):
            posting_ptr.append(posting_indexes[i])
            long_string += chr(len(word)) + word  # 词项的长度+词项本身（用一个字节表示长度）
            #每满一个块，保存该块的内容
            if cnt == block_size - 1:
                blocks.append((posting_ptr, index))
                posting_ptr = [] #重新初始化倒排表指针列表
                index = len(long_string) #更新当前词项在long_string中的起始位置
                cnt = 0
            else:
                cnt += 1
        # 最后将剩余的posting_ptr添加到block中
        if posting_ptr:
            blocks.append((posting_ptr, index))
        return blocks, long_string
    #从blocking结构中解压出Trie树
    @staticmethod
    def decompress_from_blocking(blocks, long_string):
        trie = Trie()
        for block in blocks:
            posting_ptr, start_index = block
            for i, posting_index in enumerate(posting_ptr):
                #获取词项在long_string中的起始位置和长度
                # word_start = start_index + sum([ord(long_string[j]) + 1 for j in range(i)])
                j = 0  
                for k in range(i):  # 获取词项在long_string中的起始位置
                    word_start = start_index + ord(long_string[j]) + 1
                    j += ord(long_string[j]) + 1

                # 通过长度获取每个词项
                # 这里的for是递归这算的应该，j=i代表之前i-1个计算结果的和
                word_length = ord(long_string[word_start])  # 获取词项的长度
                word = long_string[word_start + 1: word_start + word_length + 1]  # 提取词项
                #在Trie树中插入词项，并将倒排表索引赋值给对应的节点
                trie.insert(word, posting_index)
        return trie
