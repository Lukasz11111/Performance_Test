import re
import sys
import os
import json

def clear_raport_result(json_dict):
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


JSON_CONFIG_PATH=sys.argv[1]

with open(JSON_CONFIG_PATH+"/.config") as f:
    json_config = json.load(f)

result=json_config['application_name'] 

f = open("tmp.txt", "a")
f.write(result)
f.close()

JSON_RAPORT_PATH=sys.argv[2]

with open(JSON_RAPORT_PATH, 'r', encoding='utf-8' ) as x:
    json_dict = json.load(x)


clear_raport_result(json_dict)
json_dict["Application_name"]=result
json_dict["Jmeter_raport_path"]=sys.argv[3]


with open(JSON_RAPORT_PATH, "w", encoding='utf-8') as x:    
    json.dump(json_dict, x, ensure_ascii=False, indent=4)



