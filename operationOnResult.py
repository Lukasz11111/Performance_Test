import time
from datetime import datetime
import sys
import os
import json
import operationOnConfigPython

idTest=sys.argv[1]
idMod=sys.argv[2]
JSON_RAPORT_PATH=os.getenv('JSON_RAPORT_PATH')
JSON_CONFIG=os.getenv('JSON_CONFIG')
def load_json():
    with open(JSON_RAPORT_PATH) as f:
        return json.load(f)

def clear_raport_result():
    json_dict = load_json()
    json_dict["Trace_Error_Before"]=0
    json_dict["Trace_Error"]=0
    json_dict["Trace_Succes_Before"]=0
    json_dict["Trace_Succes"]=0
    json_dict["Recordings"]=0
    json_dict["Trace"]=0
    json_dict["TotalJmeter"]["sampleCount"]=0
    json_dict["TotalJmeter"]["meanResTime"]=0
    json_dict["TotalJmeter"]["receivedKBytesPerSec"]=0
    json_dict["TotalJmeter"]["sentKBytesPerSec"]=0
    return json_dict

def beforeStart():
    json_dict_result=clear_raport_result()

    timeResult = time.time()
    json_dict_result["StartTime"]=str(datetime.fromtimestamp(timeResult))

    with open(JSON_RAPORT_PATH, "w", encoding='utf-8') as x:    
        json.dump(json_dict_result, x, ensure_ascii=False, indent=4)

def getStartTime():
    json_dict = load_json()
    return json_dict["StartTime"]

def setTraceBefore(trace_err,trace_suc):
    json_dict = load_json()
    json_dict["Trace_Succes_Before"]=trace_suc
    json_dict["Trace_Error_Before"]=trace_err
    with open(JSON_RAPORT_PATH, "w", encoding='utf-8') as x:    
        json.dump(json_dict, x, ensure_ascii=False, indent=4)
    

def getTraceERRORBefore():
    json_dict = load_json()
    return json_dict["Trace_Error_Before"]

def getTraceSUCCESBefore():
    json_dict = load_json()
    return json_dict["Trace_Succes_Before"]

def createDictOfResult(idTest,idMod):
    json_dict = load_json()
    result={}

    result['sampleCount']=json_dict["TotalJmeter"]["sampleCount"]
    result['meanResTime']=json_dict["TotalJmeter"]["meanResTime"]
    result['receivedKBytesPerSec']=json_dict["TotalJmeter"]["receivedKBytesPerSec"]
    result['sentKBytesPerSec']=json_dict["TotalJmeter"]["sentKBytesPerSec"]
    result['errorPct']=json_dict["TotalJmeter"]["errorPct"]
    result['Recordings']=json_dict["Recordings"]
    result['Trace']=json_dict["Trace"]
    result['Calls']=getCallsPerSecond()
    result['Trace_Succes']=json_dict["Trace_Succes"]
    result['Trace_Error']=json_dict["Trace_Error"]
    result['Recordings_Percent']=percent(result['sampleCount'],json_dict["Recordings"],100-result['errorPct'])
    result['Trace_Percent']=percent(result['sampleCount'],json_dict["Trace"],0)
    result['Mod']=operationOnConfigPython.getActiveMod(idTest,idMod)

    result['MV']=operationOnConfigPython.getMV(idTest,idMod)
    result['rdb_version']=json_dict["version"]
    result['commits']=getRDBCommits(idTest, idMod)
    result['lang']=operationOnConfigPython.getLang(idTest,idMod)
    result['initialFilling']=operationOnConfigPython.initialFilling(idTest,idMod)

    result['app_version']=operationOnConfigPython.getAppVersion(idTest,idMod)
    result['ssl']=operationOnConfigPython.checkSsl(idTest, idMod)

    result['endpoint_len']=operationOnConfigPython.getAvgCodeLen(idTest, idMod)

    result['user_on_rdb']=operationOnConfigPython.getUsersOnRDB(idTest, idMod)
    result['data_retention_rdb']=operationOnConfigPython.getdataRetentionRDB(idTest, idMod)
    result['data_retention_apm']=operationOnConfigPython.getdataRetentionAPM(idTest, idMod)
    result['multiservice']=operationOnConfigPython.getMultiservice(idTest, idMod)
    result['db']=operationOnConfigPython.getDB(idTest, idMod)


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
    colorValue =operationOnConfigPython.getColor(idTest,idMod)

    import random
    if not colorValue:
        colorValue=random.choice(list(result.keys()))
        setColor(idTest,idMod, colorValue)
    try:
        result=result[colorValue]
    except:
        colorValue=random.choice(list(result.keys()))
        setColor(idTest,idMod, colorValue)
        result=result[colorValue]
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

    
def setColor(idTest,idMod, colorValue):
    with open(JSON_CONFIG) as f:
        json_dict= json.load(f)
    json_dict["Tests"][int(idTest)]["module"][int(idMod)]['color']=colorValue
    with open(JSON_CONFIG, "w", encoding='utf-8') as x:    
        json.dump(json_dict, x, ensure_ascii=False, indent=4)
    

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
    json_dict = load_json()
    json_dict["version"]=version
    with open(JSON_RAPORT_PATH, "w", encoding='utf-8') as x:    
        json.dump(json_dict, x, ensure_ascii=False, indent=4)

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

def saveValue(rec,trace,traceErr,traceSuc):
    with open(os.getenv("RESULT_STATISTICS_PATH")) as f:
        json_JM= json.load(f)

    json_result = load_json()
    json_result["TotalJmeter"]["errorPct"] = int(json_JM["Total"]["errorPct"])

    json_result["TotalJmeter"]["sampleCount"] = json_JM["Total"]["sampleCount"]
    json_result["TotalJmeter"]["meanResTime"] = int(json_JM["Total"]["meanResTime"])
    json_result["TotalJmeter"]["receivedKBytesPerSec"] =int(json_JM["Total"]["receivedKBytesPerSec"])
    json_result["TotalJmeter"]["sentKBytesPerSec"] = int(json_JM["Total"]["sentKBytesPerSec"])

    json_result["Recordings"]=rec
    json_result["Trace"]=trace
    json_result["Trace_Succes"]=traceErr
    json_result["Trace_Error"]=traceSuc
    with open(os.getenv("JSON_RAPORT_PATH"), "w", encoding='utf-8') as x:    
        json.dump(json_result, x, ensure_ascii=False, indent=4)
    from time import sleep
    sleep(0.5)
