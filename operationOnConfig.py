import argparse
import json
JSON_CONFIG="TestsConfig/Configuration.json"

parser = argparse.ArgumentParser(description='Get config')


parser.add_argument('-getCountOfAllTest',  nargs='?')
parser.add_argument('-approximateTime',  nargs='?')
parser.add_argument('-TotalJmeter',  nargs='?')

args=parser.parse_args().__dict__

filtered = {k: v for k, v in args.items() if v is not None}
args.clear()
args.update(filtered)

with open(JSON_CONFIG) as f:
    json_dict = json.load(f)


def to_bool(value):
    valid = {'true': True, 't': True, '1': True, 1: True,
             'false': False, 'f': False, '0': False,0 : False,
             }   
    if isinstance(value, bool):
        return value
    lower_value = str(value).lower()
    if lower_value in valid:
        return valid[lower_value]
    else:
        raise ValueError('invalid literal for boolean: "%s"' % value)


# for key, value in args.items():
#     json_dict[key]=value

def getTestTime(idTest,idmod):
    if "test_time" in json_dict['Tests'][idTest]['module'][idmod]:
        if int(json_dict['Tests'][idTest]['module'][idmod]["test_time"]) > 0:
            return json_dict['Tests'][idTest]['module'][idmod]["test_time"]
    if "test_time" in json_dict['Tests'][idTest]:
        if int(json_dict['Tests'][idTest]['test_time']) > 0:
            return json_dict['Tests'][idTest]['test_time']
    if "test_time" in json_dict:
        if int(json_dict['test_time']) > 0:
            return json_dict['test_time']
    return '10'
    

def getAllRun():
    runs={"allRun":0,"testTime":0}
    for index, val in enumerate(json_dict['Tests']):
        if to_bool(val['active']):
            proportionSize=len(val['proportions'])
            allOnMode=returnLenOfActiveMod(val['module'])
            singletestTime=0
            key=index
            for index, val in enumerate(val['module']):
                if ifModIsActiv(val):
                    singletestTime+=proportionSize*(int(getTestTime(key,index))+5)
            runs["testTime"]=runs["testTime"]+singletestTime
            if proportionSize > 0 and allOnMode > 0:
                runs["allRun"]=runs["allRun"]+(proportionSize*allOnMode)
    return runs

def ifModIsActiv(mod):
    if 'active' in mod:
        if not to_bool(mod['active']):
            return False
        else:
            return True
    return True

def returnLenOfActiveMod(mods):
    activeMod=0
    for index, val in enumerate(mods):
        if 'active' in val:
            if not to_bool(val['active']):
                pass
            else:
                activeMod+=1
        else:
            activeMod+=1
    return activeMod


# print(getAllRun())

import datetime

# with open(JSON_RAPORT_PATH, "w", encoding='utf-8') as x:    
#     json.dump(json_dict, x, ensure_ascii=False, indent=4)

for key in args:
    result = {
    'getCountOfAllTest': getAllRun()['allRun'],
    'approximateTime': str(datetime.timedelta(seconds=getAllRun()["testTime"])),
    }[key]

import sys

sys.exit(result)