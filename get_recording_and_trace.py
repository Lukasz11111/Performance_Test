from sshtunnel import SSHTunnelForwarder

import time
import os
import sys
import json
import psycopg2
from datetime import datetime

JSON_CONFIG_PATH=sys.argv[1]+"/.config"
with open(JSON_CONFIG_PATH) as f:
    json_config = json.load(f)

HOST=json_config['server_rdb']
PROTOCOL=json_config['protocol']


DBNAME=os.getenv('RDB_DB')
USER=os.getenv('RDB_USER')  
PASSWORD=os.getenv('RDB_PASS') 

SSH_PKEY=os.getenv('LC_STRESS_KEY_RDB')

PORT=os.getenv('RDB_PORT_DB')

DB_HOST=os.getenv('IP_REMOTE_RDB_DB')
KEY_PW=os.getenv('RDB_USER_SYSTEM')

with open('./.StartTime') as t:
    StartTime = json.load(t)
    StartTime=datetime.fromtimestamp(StartTime)



def singleOperation(query):
    with SSHTunnelForwarder(
            (HOST, 22),
            ssh_private_key=SSH_PKEY,
            ### in my case, I used a password instead of a private key
            ssh_username=KEY_PW,
        #  ssh_password="<mypasswd>", 
            remote_bind_address=(DB_HOST, 5432)) as server:
            server.start()    

            params = {
                'database': DBNAME,
                'user': USER,
                'password': PASSWORD,
                'host': 'localhost',
                'port': server.local_bind_port
                }

            conn = psycopg2.connect(**params)
            curs = conn.cursor()
            curs.execute(query)
            result = curs.fetchall()
            curs.close()
        
            return result[0][0]

def getREC():
    getall=True
    i=0
    result2=-1
    while getall:
        EndTime = time.time()
        EndTime=datetime.fromtimestamp(EndTime)
        result = singleOperation(f'''(SELECT COUNT(*) FROM public."Recordings"  WHERE "Created" >= '{StartTime}'::timestamp  and "Created" <=  '{EndTime}'::timestamp );''')
        time.sleep(5)
        EndTimeNext = time.time()
        EndTimeNext=datetime.fromtimestamp(EndTimeNext)
        result2 = singleOperation(f'''(SELECT COUNT(*) FROM public."Recordings"  WHERE "Created" >= '{StartTime}'::timestamp  and "Created" <=  '{EndTimeNext}'::timestamp );''')
        if(result==result2):
            getall=False
        if(i==60):
            result2="Oh, something went wrong"
            getall=False
        i=i+1
    return result2




def getTRACE(is_err):
    getall=True
    i=0
    result2=-1
    while getall:
        result = singleOperation(f'''(SELECT COUNT(*) FROM public."segment"  WHERE is_error={is_err} );''')
        time.sleep(5)
        result2 = singleOperation(f'''(SELECT COUNT(*) FROM public."segment"  WHERE is_error={is_err} );''')
        if(result==result2):
            getall=False
        if(i==60):
            result2="Oh, something went wrong"
            getall=False
        i=i+1
    return result2


resultRecording = getREC()

f = open(".trace", "r")
listTrace =f.readline().split('-')

resultTraceErrBefore = listTrace[0]
resultTraceSucBefore =  listTrace[1]

resultTraceErrAfter = getTRACE(1)
resultTraceSucAfter = getTRACE(0)

resultTraceErr=int(resultTraceErrAfter)-int(resultTraceErrBefore)
resultTraceSuc=int(resultTraceSucAfter)-int(resultTraceSucBefore)
resultTrace=resultTraceErr+resultTraceSuc
print(f'Recording: {resultRecording}')
print(f'Trace all: {resultTrace}')
print(f'Trace err: {resultTraceErr}')
print(f'Trace suc: {resultTraceSuc}')


with open("test/result/statistics.json") as f:
    json_JM= json.load(f)

with open("test/stress.json") as f:
    json_result= json.load(f)

json_result["TotalJmeter"]["sampleCount"] = json_JM["Total"]["sampleCount"]
json_result["TotalJmeter"]["meanResTime"] = json_JM["Total"]["meanResTime"]
json_result["TotalJmeter"]["receivedKBytesPerSec"] =json_JM["Total"]["receivedKBytesPerSec"]
json_result["TotalJmeter"]["sentKBytesPerSec"] = json_JM["Total"]["sentKBytesPerSec"]

json_result["Recordings"]=resultRecording
json_result["Trace_Span"]=resultTrace
json_result["Trace_Span_Suc"]=resultTraceSuc
json_result["Trace_Span_Err"]=resultTraceErr

with open("test/stress.json", "w", encoding='utf-8') as x:    
    json.dump(json_result, x, ensure_ascii=False, indent=4)