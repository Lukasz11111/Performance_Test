import sys
import json
PATH_CONF=sys.argv[1]

with open(PATH_CONF) as f:
    json_dict = json.load(f)

def f():
    return json_dict["server_rdb"]
   
sys.exit(f())
