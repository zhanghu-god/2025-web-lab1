import html
import re

from nltk import word_tokenize

from parse_xml import normalize_text, stemmer, stop_words
#来自PastEvent 10389592.xml的description
text ="This is a 100% hands-on workshop that will focus on glamour, implied nude, and provocative posing. It is open to photographers at all levels.  You will be working in a commercial studio, using a full range of high-end studio gear and experienced professional models.  Individual training and assistance will be available throughout the event.  Due to the nature of this shoot, seating is very limited.  Here are some highlights:&lt;br /&gt;&lt;br /&gt;•  high contrast lighting&lt;br /&gt;•  prone and proactive posing&lt;br /&gt;•  implied nude posing&lt;br /&gt;•  very special (1 time only) glamour ballerina using point shoes&lt;br /&gt;•   (see samples the models and sets)    &lt;a href=&quot;http://www.pbase.com/beauarts/june07&quot; target=&quot;_blank&quot;&gt;(click here)&lt;/a&gt;&lt;br /&gt;&lt;br /&gt;Time:  Sunday, June 7th 10AM – 2PM (#)&lt;br /&gt;Place: Jerry Bedrick Studios, 122 Western Avenue, Suite A311-A312, Lowell, MA 01850&lt;br /&gt;Contact:  Jerry Bedrick   -    jerry@jerrybedrick.com     -    781.771.3101&lt;br /&gt;Cost:   $55 (##) &lt;br /&gt;&lt;br /&gt;(#)    There will be a free pre-shoot workshop on studio basics from 9AM-10AM&lt;br /&gt;(##) $55 prepaid, $65 at the door.&lt;br /&gt;"

#小写
text=text.lower()
print(text)
# 去掉特殊符号（保留单词和空格）
text = html.unescape(text)  # 转回 <p>Our purpose:</p>
print(text)
text = re.sub(r"<.*?>", "", text)  # 去掉 <p> 和 </p>
print(text)
text = re.sub(r"[^a-z\s]", " ", text)
print(text)
# 分词
tokens = word_tokenize(text)
print(tokens)
# 去停用词 & 词干化
clean_tokens = [
    stemmer.stem(word) for word in tokens
    if word not in stop_words
]
print(clean_tokens)