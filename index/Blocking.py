from config import BLOCK_SIZE

class Blocking:
    def __init__(self,blocks,long_string):
        self.blocks = blocks
        self.long_string = long_string
    #用块存储进行搜索
    def search(self, word):
        low, high = 0, len(self.blocks) - 1
        #块外进行二分查找确定所在的块
        target_block = []
        while low <= high:
            mid = (low + high) // 2
            posting_ptr, pos = self.blocks[mid]
            word_len = ord(self.long_string[pos])
            pos += 1
            mid_word = self.long_string[pos:pos + word_len]
            if mid_word == word:
                return posting_ptr[0]
            elif mid_word > word:
                high = mid - 1
            else:
                #如果mid_word < word，要判断是在块内，还是后面的块
                posting_ptr_next, pos_next = self.blocks[mid + 1]
                word_len_next = ord(self.long_string[pos_next])
                pos_next += 1
                mid_next_word = self.long_string[pos_next:pos_next + word_len_next]
                if mid_next_word < word:
                    low = mid + 1
                else:
                    target_block = self.blocks[mid]
                    break
        # 块内进行线性搜索
        posting_ptr, pos = target_block
        for i in range(len(posting_ptr)):
            word_len = ord(self.long_string[pos])
            pos += 1
            word_i = self.long_string[pos:pos + word_len]
            # 如果当前块内找到该单词，则返回该单词的倒排表索引
            if word_i == word:
                return posting_ptr[i]
            pos += word_len
            # 如果当前块内没有该单词，则跳出循环
            if word_i > word:
                return -1
        return -1

#前端编码存储,两个部分放到一起
class FrontCoding:
    def __init__(self,blocks,long_string):
        self.blocks = blocks
        self.long_string = long_string