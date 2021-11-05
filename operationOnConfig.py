import argparse
import json
JSON_CONFIG="TestsConfig/Configuration.json"

# parser = argparse.ArgumentParser(description='Process some integers.')


# parser.add_argument('-Recordings',  nargs='?')
# parser.add_argument('-Trace_Span',  nargs='?')
# parser.add_argument('-TotalJmeter',  nargs='?')

# args=parser.parse_args().__dict__

# filtered = {k: v for k, v in args.items() if v is not None}
# args.clear()
# args.update(filtered)


with open(JSON_CONFIG) as f:
    json_dict = json.load(f)


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
    runs={"allRun":0}
    for idx, val in json_dict['Tests']:
        proportionSize=len(val['proportions'])
        allMode=len(val['module'])
        singletestTime=0
        for value,key in val['module']:
            singletestTime=getTestTime(c,key)
        if proportionSize > 0 and allMode > 0:
            runs["allRun"]=runs["allRun"]+(proportionSize*allMode)
    return runs




# print(getAllRun())
print(getTestTime(0,0))




# with open(JSON_RAPORT_PATH, "w", encoding='utf-8') as x:    
#     json.dump(json_dict, x, ensure_ascii=False, indent=4)