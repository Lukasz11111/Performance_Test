import requests
import sys
import json
import aiohttp
import asyncio
import time

HOST=sys.argv[1]
SAVE=sys.argv[2]

# rdb removal / startup

async def main():
    async with aiohttp.ClientSession() as session:
            async with session.get(HOST) as resp:
                t = await resp.text()
                return t

loop = asyncio.get_event_loop()
try:
  r = loop.run_until_complete(main())
except:
  print("")
    

if SAVE=='y':
    result=str(r)
    result=result.split('|')
    result[0]=result[0].split(':')
    result[1]=result[1].split(':')
    f = open("rdb_res", "w")
    f.write(result[1][1]+'\n'+result[0][1])
    f.close()
 