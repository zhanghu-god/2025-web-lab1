import os
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
