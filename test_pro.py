import json



# with open("assistant_config.ini",'w') as fp:
#   json.dump(init_list,fp,ensure_ascii=False)
#
# with open("assistant_config.ini",'r') as fp:
#   data=json.load(fp)
#   print(data)


list_replace={}
item=["a","b","c"]

list_replace[item[0]]={"string":item[2],"used":item[2]}

print(list_replace)
