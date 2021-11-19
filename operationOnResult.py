import time
from datetime import datetime
import sys
import os
import json
import operationOnConfigPython

idTest=sys.argv[1]
idMod=sys.argv[2]
JSON_RAPORT_PATH="./TestResult/stress.json"

with open( JSON_RAPORT_PATH,'r', encoding='utf-8' ) as x:
    json_dict = json.load(x)

def clear_raport_result():
    json_dict["APM_Spans_Before"]=0
    json_dict["APM_Spans_After"]=0
    json_dict["Recording_Before"]=0
    json_dict["Recording_After"]=0
    json_dict["Recordings"]=0
    json_dict["Trace_Span"]=0
    json_dict["TotalJmeter"]["sampleCount"]=0
    json_dict["TotalJmeter"]["meanResTime"]=0
    json_dict["TotalJmeter"]["receivedKBytesPerSec"]=0
    json_dict["TotalJmeter"]["sentKBytesPerSec"]=0
    return json_dict


def getStartTime():
    