#!/bin/bash


RDB_KEY="$(python3 operationOnConfig.py -getRDBKey $1 -mod $2 2>&1)"


REMOTE_RDB_HOST="$(python3 operationOnConfig.py -getRDBHost $1 -mod $2 2>&1)"
RDB_USER_SYSTEM="$(python3 operationOnConfig.py -getRdbDBSysUser $1 -mod $2 2>&1)"
REVDEBUG_DOCKER_PATH="$(python3 operationOnConfig.py -getDockerRDBPath $1 -mod $2 2>&1)"


sslActive="$(python3 operationOnConfig.py -getSSLActive $1 -mod $2 2>&1)"
keyCloak="$(python3 operationOnConfig.py -getKeycloakActive $1 -mod $2 2>&1)"


if [[ $sslActive == "1" ]]; then
    sslComannd='
    sudo mkdir /var/revdebug;
    sudo mkdir /var/revdebug/cert;
    sudo cp ~/mycert/mycert.key /var/revdebug/cert;
    sudo cp ~/mycert/mycert.crt /var/revdebug/cert;
    '
else
    sslComannd=''
fi

if [[ $keyCloak == "1" ]]; then
    startCmmand='
    sudo docker-compose -f docker-compose.keycloak.yml -f docker-compose.yml -p rdb restart'
else
    startCmmand=' sudo docker-compose -p rdb restart'
fi


bashCommand='
cd '$REVDEBUG_DOCKER_PATH';
'$startCmmand'
'

echo "$bashCommand";

. RemoteServer.sh $RDB_KEY $REMOTE_RDB_HOST $RDB_USER_SYSTEM "$bashCommand"

sleep 20