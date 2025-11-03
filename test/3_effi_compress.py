"""
比较索引压缩前后在检索效率上的差异
"""
import html
import re

import time
from nltk import word_tokenize

from config import DICTIONARY_BLOCKING
from index.parse_xml import stemmer, stop_words, normalize_text
from query.load import load, load_pickle
from query.search import bool_search

if __name__ == '__main__':
    # 加载索引,未压缩
    dictionary, inverted_index, id_name = load()
    # 加载索引,按块存储
    dictionary_blocking = load_pickle(DICTIONARY_BLOCKING)
    # 三次布尔查询
    text = "This is a 100% hands-on workshop that will focus on glamour, implied nude, and provocative posing. It is open to photographers at all levels.  You will be working in a commercial studio, using a full range of high-end studio gear and experienced professional models.  Individual training and assistance will be available throughout the event.  Due to the nature of this shoot, seating is very limited.  Here are some highlights:&lt;br /&gt;&lt;br /&gt;•  high contrast lighting&lt;br /&gt;•  prone and proactive posing&lt;br /&gt;•  implied nude posing&lt;br /&gt;•  very special (1 time only) glamour ballerina using point shoes&lt;br /&gt;•   (see samples the models and sets)    &lt;a href=&quot;http://www.pbase.com/beauarts/june07&quot; target=&quot;_blank&quot;&gt;(click here)&lt;/a&gt;&lt;br /&gt;&lt;br /&gt;Time:  Sunday, June 7th 10AM – 2PM (#)&lt;br /&gt;Place: Jerry Bedrick Studios, 122 Western Avenue, Suite A311-A312, Lowell, MA 01850&lt;br /&gt;Contact:  Jerry Bedrick   -    jerry@jerrybedrick.com     -    781.771.3101&lt;br /&gt;Cost:   $55 (##) &lt;br /&gt;&lt;br /&gt;(#)    There will be a free pre-shoot workshop on studio basics from 9AM-10AM&lt;br /&gt;(##) $55 prepaid, $65 at the door.&lt;br /&gt;"
    #处理文本,生成tokens
    clean_tokens = normalize_text(text)

    start_time = time.perf_counter()
    for j in range(500):
        for i in range(len(clean_tokens)):
            # search_result = bool_search(text[i], dictionary, inverted_index, id_name)
            dictionary.search(clean_tokens[i])
    end_time = time.perf_counter()
    time1 = end_time - start_time
    start_time = time.perf_counter()
    for j in range(500):
        for i in range(len(clean_tokens)):
            # search_result = bool_search(text[i], dictionary_blocking, inverted_index, id_name)
            dictionary_blocking.search(clean_tokens[i])
    end_time = time.perf_counter()
    time2 = end_time - start_time
    print("未压缩索引检索耗时：", time1)
    print("按块存储索引检索耗时：", time2)
