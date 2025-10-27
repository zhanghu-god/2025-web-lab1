import sys
import os

# 添加 parse_xml.py 所在目录到 Python 路径
pro_dir = r"H:\web\lab1\project"  # 根据实际情况修改路径
sys.path.append(pro_dir)

from config import *


'''查看文档的数量'''
os.chdir(DATA_DIR)
cwd=os.getcwd()
count=0
for fold in os.listdir(cwd):
    cnt = len(os.listdir(os.path.join(cwd, fold)))
    print(fold + ':' + str(cnt))
    count+=cnt
print("ALL:"+str(count))
