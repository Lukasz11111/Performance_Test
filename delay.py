import sys
import json
PATH_CONF=sys.argv[1]

with open(PATH_CONF) as f:
    json_dict = json.load(f)

def f():
    if "delay" in json_dict:
        if not (json_dict['delay'] is None):
            return json_dict["delay"]
    return "0"
    
sys.exit(f())
