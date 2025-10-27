import os
import xml.etree.ElementTree as ET

from config import DATA_DIR
from parse_xml import parse_group_file, normalize_text

file_type="Event"
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