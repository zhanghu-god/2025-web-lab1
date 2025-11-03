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
        from Blocking import Blocking
        # 提取所有词项及其倒排表位置索引
        words, posting_indexes = [], []
        self.extract_words(self.root, "", words, posting_indexes)
        # 拼接所有词项成一个长字符串
        long_string = ""
        blocks = []  #最终返回的blocking结构
        offset = 0  # 当前块在 long_string 中的起始位置
        # 按 block_size 分块
        for start in range(0, len(words), block_size):
            # 当前块内的词项和对应 posting index
            block_words = words[start:start + block_size]
            block_postings = posting_indexes[start:start + block_size]
            # 将块内所有词项拼接成：长度(1B)+词项
            encoded_block = ""
            for w in block_words:
                encoded_block += chr(len(w)) + w

            # 记录块信息（倒排表指针列表 + 当前块在字符串中的起始偏移）
            blocks.append((block_postings, offset))

            # 更新整体字符串与偏移
            long_string += encoded_block
            offset += len(encoded_block)

        return Blocking(blocks, long_string)
    @staticmethod
    def decompress_from_blocking(blocking):
        trie = Trie()
        for posting_ptr, start_index in blocking.blocks:
            pos = start_index  # 当前块内的读取位置
            for posting_index in posting_ptr:
                # 读取长度字节
                word_len = ord(blocking.long_string[pos])
                pos += 1
                # 读取实际词项
                word = blocking.long_string[pos:pos + word_len]
                pos += word_len
                # 插入到 Trie
                trie.insert(word, posting_index)
        return trie
    #blocking
    #获取两个字符串的公共前缀
    @staticmethod
    def get_lcp(a: str, b: str) -> str:
        i = 0
        m = min(len(a), len(b))
        while i < m and a[i] == b[i]:
            i += 1
        return a[:i]
    #将Trie树转化为前段编码存储
    def convert_to_front_coding(self, block_size):
        from Blocking import FrontCoding
        words, posting_indexes = [], []
        self.extract_words(self.root, "", words, posting_indexes)

        blocks, long_string = [], ""
        offset = 0

        for start in range(0, len(words), block_size):
            block_words = list(words[start:start+block_size])
            block_postings = list(posting_indexes[start:start+block_size])

            # 计算块内 LCP
            lcp = block_words[0]
            for word in block_words[1:]:
                lcp = self.get_lcp(lcp, word)
                if not lcp:
                    break

            # 写入：lcp长度 + 第一个单词
            encoded = chr(len(lcp)) + block_words[0]

            # 写入剩下单词每个后缀
            for word in block_words[1:]:
                suffix = word[len(lcp):]
                encoded += chr(len(suffix)) + suffix

            blocks.append((block_postings, offset))
            offset += len(encoded)
            long_string += encoded

        return FrontCoding(blocks, long_string)

    @staticmethod
    def decompress_from_front_coding(front_coding):
        trie = Trie()
        for posting_ptr, start_index in front_coding.blocks:
            pos = start_index

            # 读取 LCP 长度
            lcp_len = ord(front_coding.long_string[pos])
            pos += 1

            # 读取第一个完整单词
            first_word = ""
            # 一直读取，直到后续遇到“长度字节”（ASCII < 65 ）
            while pos < len(front_coding.long_string) and ord(front_coding.long_string[pos]) >= 65:
                first_word += front_coding.long_string[pos]
                pos += 1

            trie.insert(first_word, posting_ptr[0])
            lcp = first_word[:lcp_len]

            # 读取剩余单词
            for posting_index in posting_ptr[1:]:
                if pos >= len(front_coding.long_string):
                    break
                suffix_len = ord(front_coding.long_string[pos])
                pos += 1
                suffix = front_coding.long_string[pos:pos + suffix_len]
                pos += suffix_len
                word = lcp + suffix
                trie.insert(word, posting_index)
        return trie

