import sys
import json
PATH_CONF=sys.argv[1]

with open(PATH_CONF) as f:
    json_dict = json.load(f)

def f():
    if "raport_name" in json_config:
        if not (json_config['raport_name'] is None):
            return json_dict["delay"]
    return "0"
    
sys.exit(f())
