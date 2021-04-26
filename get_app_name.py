import re
import sys
import os
import json

FULL_NAME=sys.argv[1]

result=FULL_NAME.split("_")
result=result[len(result)-1][:-4]

f = open("tmp.txt", "a")
f.write(result)
f.close()

JSON_RAPORT_PATH=sys.argv[2]

with open(JSON_RAPORT_PATH, 'r', encoding='utf-8' ) as x:
    json_dict = json.load(x)

json_dict["Application_name"]=result
json_dict["Jmeter_raport_path"]=sys.argv[3]

with open(JSON_RAPORT_PATH, "w", encoding='utf-8') as x:    
    json.dump(json_dict, x, ensure_ascii=False, indent=4)



