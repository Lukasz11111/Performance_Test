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
    startCmmand='sudo docker-compose -p rdb up -d'
else
    startCmmand=' sudo docker-compose -p rdb up -d'
fi

python3 $RDB_SERVER_FILE_PATH/CreateEnv.py  $1 $2
env="$(cat $RDB_SERVER_FILE_PATH.env)"

bashCommand='
sudo docker stop $(sudo docker ps -q); 
sudo rm -rf /var/revdebug;
'$sslComannd'

if [  -f ~/.env ]; then
           sudo rm ~/.env;
fi;

sudo echo "'$env'" > .env;

sudo rm '$REVDEBUG_DOCKER_PATH'/.env;
sudo mv .env '$REVDEBUG_DOCKER_PATH';
cd '$REVDEBUG_DOCKER_PATH';


sudo mkdir /var/revdebug;
sudo mkdir /var/revdebug/server;
sudo mkdir /var/revdebug/server;
sudo mkdir /var/revdebug/server/repo;

sudo cp license.dat /var/revdebug/server/repo/license.dat;


sudo docker-compose -p rdb pull;
sudo docker-compose -p rdb down;
'$startCmmand'
'

echo "$bashCommand";

. RemoteServer.sh $RDB_KEY $REMOTE_RDB_HOST $RDB_USER_SYSTEM "$bashCommand"

deduplication=$(python3 operationOnConfig.py -getDeduplication $1 -mod $2 2>&1)

if [ $deduplication -ne 1 ]; then
sleep 180
python3 RevDeBugServer/CreateNewUserKeyCloak.py  $1 $2
else
sleep 60
fi 


#Na servie trzeba recznie zrobić ssl i przerzucić rdb-docker-stress 
#lub pobrac repo ale zmodyfikowac taga w dockerze od keycloka >zapisac patha w configu