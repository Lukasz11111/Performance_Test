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


HOST=operationOnConfigPython.getRDBHost(idTest, idMod)
PROTOCOL=operationOnConfigPython.getRdbProtocol(idTest, idMod)


DBNAME=operationOnConfigPython.getRdbDB(idTest, idMod)
USER=operationOnConfigPython.getRdbDBUser(idTest, idMod)
PASSWORD=operationOnConfigPython.getRdbDBPass(idTest, idMod)

SSH_PKEY=operationOnConfigPython.getRdbKey(idTest, idMod)
PORT=operationOnConfigPython.getRdbDBPort(idTest, idMod)

DB_HOST=os.getenv('IP_REMOTE_RDB_DB')
KEY_PW=operationOnConfigPython.getRdbDBSysUser(idTest, idMod)

operationOnResult.beforeStart()

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


trace_err = singleOperation(f'''(SELECT COUNT(*) FROM public."segment"  WHERE is_error=1 );''')
trace_suc = singleOperation(f'''(SELECT COUNT(*) FROM public."segment"  WHERE is_error=0 );''')


operationOnResult.setTraceBefore(trace_err,trace_suc)