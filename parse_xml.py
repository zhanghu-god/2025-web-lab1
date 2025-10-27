import os
import re
import html
import xml.etree.ElementTree as ET

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# 停用词 & 词干化工具
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def parse_group_file(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    description = root.find("description")
    if description is not None and description.text:
        return description.text
    return ""

def normalize_text(text):
    #小写
    text=text.lower()
    # 去掉特殊符号（保留单词和空格）
    text = html.unescape(text)  # 转回 <p>Our purpose:</p>
    text = re.sub(r"<.*?>", "", text)  # 去掉 <p> 和 </p>
    text = re.sub(r"[^a-z\s]", " ", text) #把除了字母和空白符号的其他符号换成空格
    # 分词
    tokens = word_tokenize(text)
    # 去停用词 & 词干化
    clean_tokens = [
        stemmer.stem(word) for word in tokens
        if word not in stop_words
    ]
    return clean_tokens

def parse_all(folder):
    docs = {}
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        try:
            text = parse_group_file(filepath)
            tokens = normalize_text(text)
            if not tokens:
                continue
            docs[filename] = tokens
        except Exception as e:
            print(f"解析 {filename} 出错: {e}")
    return docs