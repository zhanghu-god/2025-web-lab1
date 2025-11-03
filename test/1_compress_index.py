"""
比较压缩后的索引在存储空间上与原索引的区别
此脚本用于测试和比较不同索引存储方式的空间效率:
1. 顺序存储
2. 按块存储
3. 前端编码存储
"""
import os
from config import DICTIONARY_ORIN, BLOCK_SIZE, DICTIONARY_BLOCKING, DICTIONARY_FrontCoding

def get_file_size(file_path):
    """获取文件大小"""
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    return 0


def format_size(file_path):
    """将字节大小格式化为更易读的格式"""
    size_bytes = get_file_size(file_path)
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

if __name__ == "__main__":
    print(f"顺序存储的词典大小:\t\t\t\t\t" + format_size(DICTIONARY_ORIN))
    print(f"按块存储的词典大小(block_size = {BLOCK_SIZE}):\t" + format_size(DICTIONARY_BLOCKING))
    print(f"前端编码存储的词典大小(block_size = {BLOCK_SIZE}):" + format_size(DICTIONARY_FrontCoding))