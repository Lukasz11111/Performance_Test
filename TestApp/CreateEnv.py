import sys
sys.path.append("/app")
import os
import operationOnConfigPython

import uuid;

idTest=sys.argv[1]
idMod=sys.argv[2]


protocol =operationOnConfigPython.getRdbProtocol(idTest, idMod)
if protocol=='https':
    tls='REVDEBUG_FORCE_TLS=true'
else:
    tls='REVDEBUG_FORCE_TLS=false'


version=operationOnConfigPython.getAppVersion(idTest,idMod)
if version["agent"]=='-' or version["compiler"]=='-'or str(sys.argv[3])=="no-version":
    versions=''
else:
    versions=f'''\n
AGENT_VERSION={version["agent"]}
COMPILER_VERSION={version["compiler"]}
''' 

result= f'''\n
REVDEBUG_APM={operationOnConfigPython.getRDBHost(idTest, idMod)}
REVDEBUG_HOST={operationOnConfigPython.getRDBHost(idTest, idMod)}
{versions}\n
{tls}\n
'''

#pamietaj + 11800 w dockerfile

envPath=f"{os.getenv('APP_SERVER_FILE_PATH')}.env"

text_file = open(envPath, "w")
text_file.write(result)
text_file.close()

# sys.exit(result)