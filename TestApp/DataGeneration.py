from sshtunnel import SSHTunnelForwarder

import time
import os
import sys
sys.path.append("/app")
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
        result = singleOperation(f'''(SELECT COUNT(*) FROM public."Recordings" );''')
        time.sleep(5)
        EndTimeNext = time.time()
        EndTimeNext=datetime.fromtimestamp(EndTimeNext)
        result2 = singleOperation(f'''(SELECT COUNT(*) FROM public."Recordings" );''')
        if(result==result2):
            getall=False
        if(i==60):
            result2="Oh, something went wrong"
            getall=False
        i=i+1
    return result2


import requests
def start():
    resultRecording = int(getREC())
    expectation=operationOnConfigPython.initialFilling(idTest,idMod)
    if (expectation!=False):
        expectation=int(expectation)
    if (expectation>resultRecording):
        howMany=expectation-resultRecording
        howMany=int(howMany+howMany*(howMany*0.0000025))
        print(resultRecording)
        print(expectation)
        print(howMany)
        hostApp=operationOnConfigPython.getAppHost(idTest,idMod)
        portApp=operationOnConfigPython.getAppGenDataPort(idTest,idMod)
        endpoint=operationOnConfigPython.getAppGenDataEndpoint(idTest,idMod)
        for x in range(0,howMany):
            try:   
                r = requests.get(f'http://{hostApp}:{portApp}{endpoint}',timeout=0.0000000001)
            except:
                pass
    else:
        return True
    return False

def main(): 
    sem=True
    for x in range(0,10):
        if sem:
            result = start()
            if result:
                sem=False



main()
