import json
import os

JSON_CONFIG=os.getenv('JSON_CONFIG')

with open(JSON_CONFIG) as f:
    json_dict = json.load(f)

def getEndpoints(idTest, idMod=0):  
    return getRdbConf("server_app_default",idTest,[],"endpoints",idMod)

def getSuccesEndpoint(idTest,idMod):
    result=[]
    for x in getRdbConf("server_app_default",idTest,[],"endpoints",idMod):
        if not x.get("error"):
            result.append(x)
    return result


def getErrorEndpoint(idTest,idMod):
    result=[]
    for x in getRdbConf("server_app_default",idTest,[],"endpoints",idMod):
        if x.get("error"):
            result.append(x)
    return result

def getProtocoleApp(idTest, idMod):
    return getRdbConf("server_app_default",idTest,"http","protocol",idMod)

def ifRaportGen(idTest,idMod):
    return getConf("raportOn",idTest,"False")


def getRdbConfMod(name,idTest,idMod, nameConf):
    if  name in json_dict["Tests"][int(idTest)]["module"][int(idMod)]:
        if nameConf in json_dict["Tests"][int(idTest)]["module"][int(idMod)][name]:
            if not json_dict["Tests"][int(idTest)]["module"][int(idMod)][name][nameConf]:
                return None
            else:
                return json_dict["Tests"][int(idTest)]["module"][int(idMod)][name][nameConf]
    return None

def getRdbConf(name,idTest,defaultVal,nameConf, idMod=None):
    
    if idMod!=None:
        result=getRdbConfMod(name,idTest,idMod,nameConf)
        if result!=None:
            return result
    if  name in json_dict["Tests"][int(idTest)]:
        if  nameConf in json_dict["Tests"][int(idTest)][name]:
            if not json_dict["Tests"][int(idTest)][name][nameConf]:
                return getRdbConfTest(name,defaultVal)
            else:
                return json_dict["Tests"][int(idTest)][name][nameConf]
        else:
            return getRdbConfTest(name,defaultVal,nameConf)
    return getRdbConfTest(name,defaultVal,nameConf)

def getRdbConfTest(name,defaultVal,nameConf):
    if  name in json_dict:
        if  nameConf in json_dict[name]:
            if not json_dict[name][nameConf]:
                return defaultVal
            else:   
                return json_dict[name][nameConf]       
    return defaultVal


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
        return False


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
        idTest=index

        if to_bool(val['active']):
            allOnMode=returnLenOfActiveMod(val['module'])
            singletestTime=0
            for index, val in enumerate(val['module']):
                idMod=index
                if ifModIsActiv(val):
                    proportionSize=getLenProportion(idTest, idMod)
                    delaySize=getLenDelay(idTest, idMod)
                    singletestTime+=delaySize*proportionSize*(int(getTestTime(idTest,index))+65)
            runs["testTime"]=runs["testTime"]+singletestTime
            if proportionSize > 0 and allOnMode > 0:
                runs["allRun"]=runs["allRun"]+(delaySize*proportionSize*allOnMode)
    return runs


def getLenProportion(idTest, idMod):
    return len(getConf("proportions",idTest,[0],idMod))

def getLenDelay(idTest, idMod):
    return len(getConf("delay",idTest,[0],idMod))

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


def retValueOrEnv(result, envName):
    if not result:
        try:
            return os.environ[envName]
        except:
            return None
    else:
        return result


def getTestDelay(idTest):
    return listToString(getConf("delay",idTest,[0]))

def getTestProportion(idTest):
    return listToString(getConf("proportions",idTest,[50]))

def getModeLen(idTest):
    return len(json_dict["Tests"][int(idTest)]['module'])

def getAppHost(idTest, idMod):
    return getRdbConf("server_app_default",idTest,"0.0.0.0","host",idMod)

def getAppPort(idTest, idMod):
    return json_dict["Tests"][int(idTest)]['module'][int(idMod)]['port']

def getThCount(idTest, idMod):
    return getConf("thread",idTest,"100",idMod)

def getRdbProtocol(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,"http","protocol",idMod)
    return retValueOrEnv(result,'RDB_PROTOCOL')

def getRDBHost(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,False,"host",idMod)
    try:
        result =retValueOrEnv(result,'RDB_HOST')
    except:
        return "localhost"
    if not result:
        return "localhost"
    return result

def getAuthCode(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,"none","rdb_auth",idMod)
    return result

def getTag(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,"nightly","rdb_docker_tag",idMod)
    return result

def getHub(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,"docker.revdebug.com/","rdb_docker_tag",idMod)
    return result

def getServerName(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,getRDBHost(idTest, idMod),"server_name",idMod)
    return result

def checkSsl(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,"http","protocol",idMod)
    if result=='https':
        return 'ssl'
    return 'non-ssl'

def getSSLActive(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,"http","protocol",idMod)
    if result=='https':
        return "1"
    return "0"

def getslave():
    return json_dict["slave"]

def getApplicationName():
    return getRdbConf("server_app_default",idTest,"Non-Name-App","application_name",idMod)


def getKeycloakActiveBash(idTest, idMod):
    if  to_bool(getKeycloakActiv(idTest, idMod)):
        return '1'
    return '0'

def getKeycloakActiv(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,False,"keycloak_active",idMod)
    return to_bool(retValueOrEnv(result,'KEYCLOAK_ACTIVE')) 

def getLogin(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,False,"login",idMod)
    return retValueOrEnv(result,'LC_RDB_LOGIN')

def getPass(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,False,"password",idMod)
    return retValueOrEnv(result,'LC_RDB_PASS')


def getRdbDB(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,False,"db",idMod)
    return retValueOrEnv(result,'RDB_DB')

def getRdbDBUser(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,False,"db_user",idMod)
    return retValueOrEnv(result,'RDB_USER')

def getRdbDBPass(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,False,"db_pass",idMod)
    return retValueOrEnv(result,'RDB_PASS')

def getRdbKey(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,False,"key_path",idMod)
    return retValueOrEnv(result,'LC_STRESS_KEY_RDB')

def getRdbDBPort(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,False,"db_port",idMod)
    return retValueOrEnv(result,'RDB_PORT_DB')

def getRdbDBSysUser(idTest, idMod):
    result = getRdbConf("server_rdb_default",idTest,False,"user_sys",idMod)
    return retValueOrEnv(result,'RDB_USER_SYSTEM')

def getSlave(idTest,idMod):
    return getConf("slave",idTest,"6",idMod)

def getDeduplication(idTest,idMod):
    result = getRdbConf("server_rdb_default",idTest,"0","deduplication",idMod)
    return result

def getPgContainerName(idTest,idMod):
    result = getRdbConf("server_rdb_default",idTest,"revdebug-server-docker-compose_postgres_1","pg_container_name",idMod)
    return retValueOrEnv(result,'POSTGRESS_CONTAINER_NAME')

def FileTestActiv():
        try:
            if to_bool(json_dict['FileTestActiv']):
                return "1"
            else:
                return "0"
        except:
            return "0"

def RDBTestActiv():
        try:
            if to_bool(json_dict['RDBTestActiv']):
                return "1"
            else:
                return "0"
        except:
            return "0"

def AppTestActiv():
        try:
            if to_bool(json_dict['AppTestActiv']):
                return "1"
            else:
                return "0"
        except:
            return "0"

def customSingleTest():
    return listToString(json_dict['start_my_file_test']["names"])

def slaveingleTest():
    return json_dict['start_my_file_test']["slave"]

def getRaportName(idTest,idMod):
    return getConf("raport_name",idTest,f'Raport{os.getenv("RUN_ID")}',idMod)

def getMV(idTest,idMod):
    return getRdbConf("server_rdb_default",idTest,"Non set","MV",idMod)

def getTestModOnly(idTest,idMod,name):
    if idMod!=None:
        result=getConfMod(name,idTest, idMod)
    if result!=None:
        return result
    
    if  name in json_dict["Tests"][int(idTest)]:
        if not json_dict["Tests"][int(idTest)][name]:
            return '-'
        else:
            return json_dict["Tests"][int(idTest)][name]
    return '-'

def getLang(idTest,idMod):
    return getRdbConf("server_app_default",idTest,"Not set lang","language",idMod)
    

def getFramework(idTest,idMod):
    return getRdbConf("server_app_default",idTest,"-","framework",idMod)

def getKeyPathApp(idTest,idMod):
    return getRdbConf("server_app_default",idTest,".","key_path",idMod)

def getAppDir(idTest,idMod):
    return getRdbConf("server_app_default",idTest,".","appDir",idMod)

def getUserAppSys(idTest,idMod):
    return getRdbConf("server_app_default",idTest,"azureuser","user_sys",idMod)

def getAppPath(idTest,idMod):
    return getRdbConf("server_app_default",idTest,"azureuser","appPath",idMod)

def getAppVersion(idTest,idMod):
    result= getRdbConf("server_app_default",idTest,"-","app_version",idMod)
    if result=='-':
        return {'agent':'-','compiler':'-'}
    return result

def getActiveMod(idTest,idMod):
    return json_dict["Tests"][int(idTest)]["module"][int(idMod)]['name']


def getColor(idTest,idMod):
    return getConfMod("color",idTest, idMod)

def getAvgCodeLen(idTest,idMod):
    value=getRdbConf("server_app_default",idTest,[],"endpoints",idMod)
    i=0
    sum_=0
    for x in value:
        if 'code' in x:
            try:
                len_=int(x['code'])
                sum_=sum_+len_
                i=i+1
            except:
                print("Convert error")
    if sum_>0 and i>0:
        return str(int(sum_/i))
    return '-'


def getdefaultRaportName(idTest, idMod):
    return to_bool(getConf("defaultRaportName",idTest,True,idMod)) 

def getUsersOnRDB(idTest, idMod):
    return getConf("user_on_rdb",idTest,False,idMod)

def getdataRetentionRDB(idTest, idMod):
    return getRdbConf("server_rdb_default",idTest,False,"data_retention_rdb",idMod)
    
def getdataRetentionAPM(idTest, idMod):
    return getRdbConf("server_rdb_default",idTest,False,"data_retention_apm",idMod)

def getMultiservice(idTest, idMod):
    return getConf("multiservice",idTest,False,idMod)

def getDB(idTest, idMod):
    return getConf("db",idTest,False,idMod)

def clearRDBAfterMod():
    if to_bool(json_dict["clear_RDB_after_mod"]):
        return '1'
    return '0'

def clearRDBAfterTest():
    if to_bool(json_dict["clear_RDB_after_test"]):
        return '1'
    return '0'

def clearRDBAfterAll():
    if to_bool(json_dict["clear_RDB_after_all"]):
        return '1'
    return '0'

def rebuildAppAfterMod():
    if to_bool(json_dict["rebuild_app_after_mod"]):
        return '1'
    return '0'

def rebuildAppAfterTest():
    if to_bool(json_dict["rebuild_app_after_test"]):
        return '1'
    return '0'

def rebuildAppAfterAll():
    if to_bool(json_dict["rebuild_app_after_all"]):
        return '1'
    return '0'

def rebuildDataGenApp(idTest,idMod):
    result= getRdbConf("server_rdb_default",idTest,False,"server",idMod)
    if 'rebuildDataGenApp' in result:
        if to_bool(result['rebuildDataGenApp' ]):
            return '1'
    return '0'


def initData(idTest,idMod):
    result= getRdbConf("server_rdb_default",idTest,False,"server",idMod)
    if 'cleanAfterSingleApp' in result:
        if to_bool(result['cleanAfterSingleApp' ]):
            return '1'
    return '0'

def initialFilling(idTest,idMod):
    result= getRdbConf("server_rdb_default",idTest,False,"server",idMod)
    if "initialFilling" in result:
        return result['initialFilling']
    return 0

def getAppGenDataDir(idTest,idMod):
    result= getRdbConf("server_rdb_default",idTest,False,"server",idMod)
    if "appGen" in result:
        if "genAppPath" in result['appGen']:
            return result['appGen']['genAppPath']
    return '.'

def getAppGenDataPort(idTest,idMod):
    result= getRdbConf("server_rdb_default",idTest,False,"server",idMod)
    if "appGen" in result:
        if "port" in result['appGen']:
            return result['appGen']['port']
    return '8080'

def getAppGenDataEndpoint(idTest,idMod):
    result= getRdbConf("server_rdb_default",idTest,False,"server",idMod)
    if "appGen" in result:
        if "endpoint" in result['appGen']:
            return result['appGen']['endpoint']
    return '/err'

def initServerAll(x,mod):
    if to_bool(json_dict["initServerAll"]):
        return '1'
    return '0'
def initServerTest(x,mod):
    if to_bool(json_dict["initServerTest"]):
        return '1'
    return '0'
def initServerMod(x,mod):
    if to_bool(json_dict["initServerMod"]):
        return '1'
    return '0'


def getDockerRDBPath(idTest,idMod):
    return getRdbConf("server_rdb_default",idTest,"~/rdb-docker-stress","rdb_docker_path",idMod)