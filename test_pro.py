import json
from unicodedata import normalize

s="我的，w 我,你"

# processed = normalize("NFKC", s)
# print(s,processed,sep="\n")

print(b'\\u4E00'<=",".encode("unicode-escape")<=b'\\u9FA5')

# print(b'\\u9FA5'.decode("unicode-escape"))

# aaa="，"
# print(aaa.encode("unicode-escape"))
