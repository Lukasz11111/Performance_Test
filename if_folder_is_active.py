import sys
import json
PATH_CONF=sys.argv[1]

with open(PATH_CONF) as f:
    json_dict = json.load(f)

def to_bool(value):
    valid = {'true': True, 't': True, '1': True, 
             'false': False, 'f': False, '0': False
             }
    return valid[value.lower()]

def f():
    try:
        if to_bool(json_dict["active"]):
            return "1"
        else:
            return "0"
    except:
        return "0"
   
sys.exit(f())
