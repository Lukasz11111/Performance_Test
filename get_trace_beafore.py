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

with open('./StartTime') as t:
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


resultERR = singleOperation(f'''(SELECT COUNT(*) FROM public."segment"  WHERE is_error=1 );''')
resultSUC = singleOperation(f'''(SELECT COUNT(*) FROM public."segment"  WHERE is_error=0 );''')


f = open(".trace", "w")
f.write(f'''{resultERR}-{resultSUC}''')
f.close()