import sys
sys.path.append("/app")
sys.path.append("/home/azureuser/stress_test")
import os
import operationOnConfigPython

import uuid;

idTest=sys.argv[1]
idMod=sys.argv[2]

result= f'''
REVDEBUG_AUTH={operationOnConfigPython.getAuthCode(idTest, idMod)}
REVDEBUG_SERVER_NAME={operationOnConfigPython.getServerName(idTest, idMod)}
REVDEBUG_ROOTVOLUME_PATH=/var/revdebug
REVDEBUG_VOLUME_PATH=/var/revdebug/server/repo
REVDEBUG_VOLUME_CAPATH=/var/revdebug/ca

REVDEBUG_CERTIFICATE_PATH=/var/revdebug/cert

REVDEBUG_DOCKER_TAG={operationOnConfigPython.getTag(idTest, idMod)}
'''

if operationOnConfigPython.checkSsl(idTest, idMod):
    result=result+f"REVDEBUG_CERTIFICATE_NAME=mycert"

if operationOnConfigPython.getKeycloakActiv(idTest, idMod):
    result=result+f'''
REVDEBUG_AUTH_OPENID_SECRET={str(uuid.uuid4())}
REVDEBUG_AUTH_METHOD=openid-connect
REVDEBUG_AUTH_OPENID_ADDRESS={operationOnConfigPython.getRdbProtocol(idTest, idMod)}://{operationOnConfigPython.getRDBHost(idTest, idMod)}/auth/realms/rdbRealm
REVDEBUG_AUTH_SAMESITE_OVERRIDE=None
REVDEBUG_AUTH_ROLESPROVIDER=external'''


# envPath=f"{os.getenv('RDB_SERVER_FILE_PATH')}.env"
# text_file = open(envPath, "w")
# text_file.write(result)
# text_file.close()

sys.exit(result)