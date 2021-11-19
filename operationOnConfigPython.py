import json

JSON_CONFIG="TestsConfig/Configuration.json"

with open(JSON_CONFIG) as f:
    json_dict = json.load(f)

def getEndpoints(idTest):  
    return json_dict["Tests"][idTest]["endpoints"]

def getSuccesEndpoint(idTest):
    result=[]
    for x in json_dict["Tests"][idTest]["endpoints"]:
        if not x.get("error"):
            result.append(x)
    return result

def getErrorEndpoint(idTest):
    result=[]
    for x in json_dict["Tests"][idTest]["endpoints"]:
        if x.get("error"):
            result.append(x)
    return result

def getProtocoleApp(idTest, idMod):
    return getConf("protocolApp",idTest,"http")

def getProtocoleRDB(idTest):
    return getConf("protocolRDB",idTest,"http")

def getConfMod(name,idTest,idMod):
    if  name in json_dict["Tests"][int(idTest)]["module"][int(idMod)]:
        if not json_dict["Tests"][int(idTest)]["module"][int(idMod)][name]:
            return None
        else:
            return json_dict["Tests"][int(idTest)]["module"][int(idMod)][name]
    else:
        return None


def getConf(name,idTest,defaultVal, idMod=None):
    if idMod!=None:
        result=getConfMod(name,idTest, idMod)
        if result!=None:
            return result
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

def listToString(valueList):
    result=""
    for i in valueList:
        result=f'{result} {i}'
    return result

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



def getTestDelay(idTest):
    return listToString(getConf("delay",idTest,[0]))

def getRDBHost(idTest):
    return getConf("server_rdb_default",idTest,"0.0.0.0")

def getTestProportion(idTest):
    return listToString(getConf("proportions",idTest,[50]))

def getModeLen(idTest):
    return len(json_dict["Tests"][int(idTest)]['module'])

def getAppHost(idTest, idMod):
    return getConf("server_app_default",idTest,"0.0.0.0",idMod)

def getAppPort(idTest, idMod):
    return json_dict["Tests"][int(idTest)]['module'][int(idMod)]['port']

def getThCount(idTest, idMod):
    return getConf("hostRDB",idTest,"100",idMod)

def getRDBHost(idTest, idMod):
    return getConf("server_rdb_default",idTest,"0.0.0.0",idMod)

def getslave():
    return json_dict["slave"]

def getApplicationName():
    return getConf("application_name",idTest,"Non Name",idMod)