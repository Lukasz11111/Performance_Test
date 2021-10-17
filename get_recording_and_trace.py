from sshtunnel import SSHTunnelForwarder

HOST="20.188.58.169"
DBNAME="revdebug_db"
USER="rdb_user"
PASSWORD="masterkey"
PG_UN="rdb_user"
PG_DB_NAME="revdebug_db"
PG_DB_PW="masterkey"
SSH_PKEY="./rdb_demo"
SSH_HOST="20.188.58.169"
DB_HOST="172.29.0.4"
PORT=5432
LOCALHOST="127.0.0.1"
KEY_PW="azureuser"

import psycopg2
from sshtunnel import SSHTunnelForwarder

with SSHTunnelForwarder(
        (HOST, 22),
        ssh_private_key=SSH_PKEY,
        ### in my case, I used a password instead of a private key
        ssh_username=KEY_PW,
    #  ssh_password="<mypasswd>", 
        remote_bind_address=(DB_HOST, 5432)) as server:
        
        server.start()
        print( "server connected")

        params = {
            'database': DBNAME,
            'user': USER,
            'password': PASSWORD,
            'host': 'localhost',
            'port': server.local_bind_port
            }

        conn = psycopg2.connect(**params)
        curs = conn.cursor()

        # curs.execute('SELECT * FROM public."Recordings"  WHERE  "Created" >=  "2021-10-07 07:17:09.001651" and "2021-10-07 07:17:09.001651" ;')
        curs.execute('''(SELECT COUNT(*) FROM public."Recordings"  WHERE "Created" >= '2021-10-07 00:17:09'::timestamp  and "Created" <=  '2021-10-13 23:17:09'::timestamp );''')

        # curs.execute('''(SELECT COUNT(*) FROM public."Recordings"  WHERE "Created" >=  "2021-10-07 07:17:09.001651"::timestamp and "Created" <=  "2021-10-07 07:17:09.001651"::timestamp ; ''')
        # curs.execute('SELECT COUNT(*) FROM public."Recordings"  WHERE "Created" <= sampling_time')
        
        result = curs.fetchall()
        print(result)
        curs.close()
        print( "database connected")





# def execute(query):
#     cur = conn.cursor()
#     cur.execute(query)
#     result = cur.fetchall()
#     cur.close()
#     return result

# execute('\dt')