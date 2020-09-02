import json
from unicodedata import normalize
import variable

# for k,v in variable.part.items():
#     proc=normalize("NFKC", k)
#     if proc != v:
#         print(k,k.encode("unicode-escape"),":",v,v.encode("unicode-escape"))

# print(variable.radicals.__len__())
variable.radicals.update(variable.supplement)
print(variable.radicals)
# print(variable.radicals.__len__())

# print("⻔".encode("unicode-escape"))
# print("⻔".encode("unicode-escape"))