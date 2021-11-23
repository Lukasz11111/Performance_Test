from sshtunnel import SSHTunnelForwarder

import time
import os
import sys
import json
import psycopg2
from datetime import datetime
import operationOnConfigPython
import operationOnResult

idTest=sys.argv[1]
idMod=sys.argv[2]
JSON_RAPORT_PATH=os.getenv("JSON_RAPORT_PATH")

HOST=operationOnConfigPython.getRDBHost(idTest, idMod)
PROTOCOL=operationOnConfigPython.getRdbProtocol(idTest, idMod)


DBNAME=operationOnConfigPython.getRdbDB(idTest, idMod)
USER=operationOnConfigPython.getRdbDBUser(idTest, idMod)
PASSWORD=operationOnConfigPython.getRdbDBPass(idTest, idMod)

SSH_PKEY=operationOnConfigPython.getRdbKey(idTest, idMod)
PORT=operationOnConfigPython.getRdbDBPort(idTest, idMod)

DB_HOST=os.getenv('IP_REMOTE_RDB_DB')
KEY_PW=operationOnConfigPython.getRdbDBSysUser(idTest, idMod)


StartTime=operationOnResult.getStartTime()


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



resultTraceErrBefore =operationOnResult.getTraceERRORBefore()
resultTraceSucBefore =operationOnResult.getTraceSUCCESBefore()

resultTraceErrAfter = getTRACE(1)
resultTraceSucAfter = getTRACE(0)

resultTraceErr=int(resultTraceErrAfter)-int(resultTraceErrBefore)
resultTraceSuc=int(resultTraceSucAfter)-int(resultTraceSucBefore)
resultTrace=resultTraceErr+resultTraceSuc
print(f'Recording: {resultRecording}')
print(f'Trace all: {resultTrace}')
print(f'Trace err: {resultTraceErr}')
print(f'Trace suc: {resultTraceSuc}')

operationOnResult.saveValue(resultRecording,resultTrace,resultTraceErr,resultTraceSuc)