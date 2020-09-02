import json
from unicodedata import normalize

punctuation="，、？：！（）"
print(set(punctuation))
# processed = normalize("NFKC", s)
# print(s,processed,sep="\n")

# print(b'\\u4E00'<=",".encode("unicode-escape")<=b'\\u9FA5')

# print(b'\\u9FA5'.decode("unicode-escape"))

# aaa="，"
# print(s.encode("unicode-escape"))
# print(processed.encode("unicode-escape"))
