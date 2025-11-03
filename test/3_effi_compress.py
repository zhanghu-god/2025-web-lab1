"""
比较索引压缩前后在检索效率上的差异
"""
from query.load import load

if __name__ == '__main__':
    # 加载索引,未压缩
    dictionary, inverted_index, id_name = load()