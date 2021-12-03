
from sshtunnel import SSHTunnelForwarder

import time
import os
import sys
import json
import psycopg2
from datetime import datetime




HOST="20.199.127.147"

DBNAME="revdebug_db"
USER="rdb_user"
PASSWORD="masterkey"

SSH_PKEY='TestStart/server1.pem'
PORT=5432

DB_HOST="192.168.80.3"
KEY_PW="azureuser"



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

dictMod=['Trace','Alarm','Dashboard','Log','Topology','Monitor','CodeView']

import random

query=f'''INSERT INTO public."UsageStatistics" (
"User", "Activity", "LastSeen", "Count") VALUES (
'alpaka'::text, 'Trace'::text, '2021-11-26 12:14:27.943809'::timestamp without time zone, '435634'::integer)
 returning "User","Activity";'''
singleOperation(query)