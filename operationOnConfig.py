import argparse
import json
import datetime

JSON_CONFIG="TestsConfig/Configuration.json"

parser = argparse.ArgumentParser(description='Get config')


parser.add_argument('-getTestDelay',  nargs='?')
parser.add_argument('-getRDBHost',  nargs='?')
parser.add_argument('-getTestProportion',  nargs='?')
parser.add_argument('-ifTestIsActive',  nargs='?')
parser.add_argument('-getCountOfAllTest',  nargs='?')
parser.add_argument('-approximateTime',  nargs='?')
parser.add_argument('-getTestsLen',  nargs='?')

argsP=parser.parse_args().__dict__

filtered = {k: v for k, v in argsP.items() if v is not None}
argsP.clear()
argsP.update(filtered)

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

def getTestsLen():
    return len(json_dict['Tests'])

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


def ifTestIsActive(idTest):
    if 'active' in json_dict['Tests'][int(idTest)]:
        try:
            if to_bool(json_dict['Tests'][int(idTest)]['active']):
                return "1"
            else:
                return "0"
        except:
            return "0"
    else:
        return "1"

def listToString(valueList):
    result=""
    for i in valueList:
        result=f'{result} {i}'
    return result

def getConf(name,idTest,defaultVal):
    if  name in json_dict["Tests"][int(idTest)]:
        if not json_dict["Tests"][int(idTest)][name]:
            return getConfTest(name,defaultVal)
        else:
            return json_dict["Tests"][int(idTest)][name]
    else:
        return getConfTest(name,defaultVal)

def getConfTest(name,defaultVal):
    if  name in json_dict:
        if not json_dict[name]:
            return defaultVal
        else:   
            return json_dict[name]
    else:
        return defaultVal

def getTestDelay(idTest):
    return listToString(getConf("delay",idTest,[0]))

def getRDBHost(idTest):
    return getConf("server_rdb_default",idTest,"0.0.0.0")

def getTestProportion(idTest):
    return listToString(getConf("proportions",idTest,[50]))

def getResult(argsP):
    for key, val in argsP.items():
        result = {
        'getRDBHost': lambda x: getRDBHost(x),
        'getTestDelay': lambda x: getTestDelay(x),
        'getTestProportion': lambda x: getTestProportion(x),
        'ifTestIsActive': lambda x: ifTestIsActive(x),
        'getTestsLen': lambda x: getTestsLen(),
        'getCountOfAllTest': lambda x: getAllRun()['allRun'],
        'approximateTime': lambda x: str(datetime.timedelta(seconds=getAllRun()["testTime"])),
        }[key](val)
    return result

result=str(getResult(argsP))


from sys import exit
exit(result)