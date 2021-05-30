import sys
import json
PATH_CONF=sys.argv[1]
# moduły 1=rdb and apm, 2=apm, 3=none, 4=rdb
RDB_MOD=sys.argv[2]


with open(PATH_CONF) as f:
    json_dict = json.load(f)
# json_dict["module"]["rdb_and_apm"]["is_on"]:



def f(x):
    return {
        '1': get_mod("rdb_and_apm"),
        '2': get_mod("apm"),
        '3': get_mod("none"),
        '4': get_mod("rdb")
    }[x]

def to_bool(value):
    valid = {'true': True, 't': True, '1': True,
             'false': False, 'f': False, '0': False,
             }
    return valid[value.lower()]

def get_mod(mod):
    if to_bool(json_dict["module"][mod]["is_on"]):
        if json_dict["module"][mod]["port"].strip():
                return json_dict["module"][mod]["host"]+":"+json_dict["module"][mod]["port"]
        else:
            return json_dict["module"][mod]["host"]+":"
    return '0'
        

sys.exit(f(RDB_MOD))



