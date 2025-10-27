import os
import xml.etree.ElementTree as ET

import sys

# 添加 parse_xml.py 所在目录到 Python 路径
pro_dir = r"H:\web\lab1\project"  # 根据实际情况修改路径
sys.path.append(pro_dir)

from config import DATA_DIR
from parse_xml import parse_group_file, normalize_text

file_type="Groups"
folder = os.path.join(DATA_DIR, file_type)
cnt=0
for filename in os.listdir(folder):
    filepath = os.path.join(folder, filename)
    text = parse_group_file(filepath)
    tokens = normalize_text(text)
    if not tokens:
        continue
    cnt+=1
print(cnt)