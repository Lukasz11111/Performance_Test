import requests
import sys
import json

HOST=sys.argv[1]
SAVE=sys.argv[2]

r =requests.get(HOST)

if SAVE=='y':
    result=str(r.text)
    result=result.split('|')
    result[0]=result[0].split(':')
    result[1]=result[1].split(':')
    f = open("rdb_res", "w")
    f.write(result[1][1]+'\n'+result[0][1])
    f.close()
 