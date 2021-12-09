#!/bin/bash


RDB_KEY="$(python3 operationOnConfig.py -getRDBKey $1 -mod $2 2>&1)"


REMOTE_RDB_HOST="$(python3 operationOnConfig.py -getRDBHost $1 -mod $2 2>&1)"
RDB_USER_SYSTEM="$(python3 operationOnConfig.py -getRdbDBSysUser $1 -mod $2 2>&1)"
REVDEBUG_DOCKER_PATH="$(python3 operationOnConfig.py -getDockerRDBPath $1 -mod $2 2>&1)"

chmod 600 $RDB_KEY

if [ ! -d /root/.ssh ]; then
    mkdir /root/.ssh
        if [ ! -f /root/.ssh/known_hosts ]; then
            touch /root/.ssh/known_hosts
fi
fi

(&>/dev/null ssh-keyscan -H $REMOTE_RDB_HOST >> ~/.ssh/known_hosts &)
(&>/dev/null ssh-keyscan -H $RDB_USER_SYSTEM >> ~/.ssh/known_hosts &)


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
    startCmmand='sudo docker-compose -f docker-compose.keycloak.yml -f docker-compose.yml -p rdb up -d'
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

sudo docker-compose -f docker-compose.keycloak.yml -f docker-compose.yml -p rdb pull;
sudo docker-compose -f docker-compose.keycloak.yml -f docker-compose.yml -p rdb down;
'$startCmmand'
'

echo "$bashCommand";

ssh -i  $LC_STRESS_KEY_RDB $RDB_USER_SYSTEM@$REMOTE_RDB_HOST  "$bashCommand";

deduplication=$(python3 operationOnConfig.py -getDeduplication $1 -mod $2 2>&1)

if [ $deduplication -ne 1 ]; then
sleep 180
python3 RevDeBugServer/CreateNewUserKeyCloak.py  $1 $2
else
sleep 60
fi 


#Na servie trzeba recznie zrobić ssl i przerzucić rdb-docker-stress 
#lub pobrac repo ale zmodyfikowac taga w dockerze od keycloka >zapisac patha w configu