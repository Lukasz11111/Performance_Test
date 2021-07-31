import sys
import json
PATH_CONF=sys.argv[1]

RDB_MOD=sys.argv[2]

with open(PATH_CONF) as f:
    json_dict = json.load(f)

def f(x):
    return {
        '0': get_mod("0"),
        '5': get_mod("5"),
        '10': get_mod("10"),
        '15': get_mod("15"),
        '20': get_mod("20"),
        '25': get_mod("25"),
        '30': get_mod("30"),
        '35': get_mod("35"),
        '40': get_mod("40"),
        '45': get_mod("45"),
        '50': get_mod("50"),
        '55': get_mod("55"),
        '60': get_mod("60"),
        '65': get_mod("65"),
        '70': get_mod("70"),
        '75': get_mod("75"),
        '80': get_mod("80"),
        '85': get_mod("85"),
        '90': get_mod("90"),
        '95': get_mod("95"),
        '100': get_mod("100")
    }[x]

def to_bool(value):
    valid = {'true': True, 't': True, '1': True, 
             'false': False, 'f': False, '0': False
             }
    return valid[value.lower()]

def get_mod(number):
    try:
        if to_bool(json_dict["proportions"][number]):
            return "1"
        else:
            return "0"
    except:
        return "0"
   
        
sys.exit(f(RDB_MOD))


