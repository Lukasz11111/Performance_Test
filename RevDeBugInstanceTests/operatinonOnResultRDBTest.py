import time
from datetime import datetime
import sys
import os
import json
sys.path.append("/app")
import operationOnConfigPython

idTest=sys.argv[1]
idMod=sys.argv[2]
JSON_CONFIG=os.getenv('JSON_CONFIG')
JSON_RAPORT_RDB_PATH=os.getenv('RESULT_STATISTICS_PATH')

def load_json():
    with open(JSON_RAPORT_RDB_PATH) as f:
        return json.load(f)

def createEndpointNamesString(listJson_):
    result=''
    for x in listJson_:
        if result=='':
            result=x['name']
        else:
            result=result+", "+x['name']
    return result

def createDictOfResult(idTest,idMod):
    json_dict = load_json()
    result={}
    result['Calls']=getCallsPerSecond()
    result['users']=operationOnConfigPython.getThCount(idTest, idMod)

    result['endpoints']=createEndpointNamesString(operationOnConfigPython.getEndpoints(idTest, idMod))
    result['emptyServer']=operationOnConfigPython.getEmptyServer(idTest, idMod)

    result['sampleCount']=json_dict["Total"]["sampleCount"]
    result['errorCount']=json_dict["Total"]["errorCount"]
    result['errorPct']=json_dict["Total"]["errorPct"]
    result['meanResTime']=json_dict["Total"]["meanResTime"]
    result['medianResTime']=json_dict["Total"]["medianResTime"]
    result['minResTime']=json_dict["Total"]["minResTime"]
    result['maxResTime']=json_dict["Total"]["maxResTime"]
    result['pct1ResTime']=json_dict["Total"]["pct1ResTime"]
    result['pct2ResTime']=json_dict["Total"]["pct2ResTime"]
    result['pct3ResTime']=json_dict["Total"]["pct3ResTime"]
    result['throughput']=json_dict["Total"]["throughput"]
    result['receivedKBytesPerSec']=json_dict["Total"]["receivedKBytesPerSec"]
    result['sentKBytesPerSec']=json_dict["Total"]["sentKBytesPerSec"]

    result['MV']=operationOnConfigPython.getMV(idTest,idMod)

    result['rdb_version']=getVersion()
    result['commits']=getRDBCommits(idTest, idMod)
    

    result['ssl']=operationOnConfigPython.checkSsl(idTest, idMod)
    return result

def getColor(idTest,idMod):
    result = {  
    'antiquewhite': "#FAEBD7",
    'azure': "#E0EEEE",
    'bisque': "#FFE4C4",
    'darkseagreen': "#B4EEB4",
    'gray': "#A1A1A1",
    'lavenderblus': "#FFF0F5",
    'black': "#292421",
    'lightpink': "#FFB6C1",
    'mistyrose': "#FFE4E1",
    'orangered': "#8B2500",
    'plum': "#DDA0DD",
    'seashell': "#CDC5BF",
    'slategray': "#C6E2FF",
    'thistle': "#D8BFD8",
    'pink': "#FFC0CB",
    'orange': "#FFA500",
    'red': "#FFC1C1",
    'blue': "#BBFFFF",
    'green': "#98FB98",
    'yellow': "#FFEC8B",
    'white': "#FFFFFF",
    }
    endpoints=operationOnConfigPython.getEndpoints(idTest, idMod)
    if len(endpoints)>1:
        result=result['antiquewhite']
    else:
        try:
            result=result[endpoints[0]['color']] 
        except:
            result=result['antiquewhite']
    return result

def getSheetName(idTest, idMod):
    lang=str(operationOnConfigPython.getLang(idTest,idMod))
    framework=str(operationOnConfigPython.getFramework(idTest,idMod))
    if framework.strip()=='-':
        if lang.strip()=='-':
            return "Not specified report"
        else:
            return lang
    else:
        return f'{lang}-{framework}'


def getCallsPerSecond():
    import re
    infile = os.getenv("LOG_PATH")
    with open(infile) as f:
        f = f.readlines()
    calls=0
    list_result=[]
    for line in f: 
        x = re.search("summary = .* Avg", line)
        if x:
            tmp =x.group(0).split("=")
            tmp[2]=tmp[2][:-3]
            list_result.append(tmp[2])
            calls=list_result[len(list_result)-1].split("/s")[0]
    calls=calls.replace(' ','')
    return float(calls)

def setVersion(version):
    with open(os.getenv('JSON_RAPORT_PATH')) as f:
        json_dict= json.load(f)
    json_dict["version"]=version
    with open(os.getenv('JSON_RAPORT_PATH'), "w", encoding='utf-8') as x:    
        json.dump(json_dict, x, ensure_ascii=False, indent=4)

def getVersion():
    with open(os.getenv('JSON_RAPORT_PATH')) as f:
        json_dict= json.load(f)
    return json_dict["version"]
   

def percent(all_,value,scuProportion):
    howManyShould=((100-int(scuProportion))/100)*all_
    if(int(howManyShould)!=0):
        result =int((int(value)/howManyShould)*100)
        result=str(result)
    else:
        result="0"
    return result

def getRDBCommits(idTest, idMod):
    import requests
    protocol=operationOnConfigPython.getRdbProtocol(idTest, idMod)
    r = requests.get(f'{protocol}://{operationOnConfigPython.getRDBHost(idTest, idMod)}/info/hashes.version')
    return r.text


