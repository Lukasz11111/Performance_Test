import time
from datetime import datetime
import sys
import os
import json
import operationOnConfigPython

idTest=sys.argv[1]
idMod=sys.argv[2]
JSON_RAPORT_PATH=os.getenv('JSON_RAPORT_PATH')

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
    result['commits']=getRDBCommits(idTest, idMod)
    result['lang']=operationOnConfigPython.getLang(idTest,idMod)
    result['initialFilling']=operationOnConfigPython.initialFilling(idTest,idMod)
    return result

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
        result=str(result)+ "%"
    else:
        result="-"
    return result

def getRDBCommits(idTest, idMod):
    import requests
    r = requests.get(f'{operationOnConfigPython.getRdbProtocol(idTest, idMod)}://{operationOnConfigPython.getRDBHost(idTest, idMod)}/info/hashes.version')
    return r.text

def saveValue(rec,trace,traceErr,traceSuc):
    with open(os.getenv("RESULT_STATISTICS_PATH")) as f:
        json_JM= json.load(f)

    json_result = load_json()
    json_result["TotalJmeter"]["sampleCount"] = json_JM["Total"]["sampleCount"]
    json_result["TotalJmeter"]["meanResTime"] = json_JM["Total"]["meanResTime"]
    json_result["TotalJmeter"]["receivedKBytesPerSec"] =json_JM["Total"]["receivedKBytesPerSec"]
    json_result["TotalJmeter"]["sentKBytesPerSec"] = json_JM["Total"]["sentKBytesPerSec"]

    json_result["Recordings"]=rec
    json_result["Trace"]=trace
    json_result["Trace_Succes"]=traceErr
    json_result["Trace_Error"]=traceSuc
    with open(os.getenv("JSON_RAPORT_PATH"), "w", encoding='utf-8') as x:    
        json.dump(json_result, x, ensure_ascii=False, indent=4)
