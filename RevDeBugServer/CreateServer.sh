#!/bin/bash


RDB_KEY="$(python3 $OPERATION_ON_CONFIG_PATH -getRDBKey $1 -mod $2 2>&1)"
echo  $OPERATION_ON_CONFIG_PATH

REMOTE_RDB_HOST="$(python3 $OPERATION_ON_CONFIG_PATH -getRDBHost $1 -mod $2 2>&1)"
RDB_USER_SYSTEM="$(python3 $OPERATION_ON_CONFIG_PATH -getRdbDBSysUser $1 -mod $2 2>&1)"
REVDEBUG_DOCKER_PATH="$(python3 $OPERATION_ON_CONFIG_PATH -getDockerRDBPath $1 -mod $2 2>&1)"

chmod 600 $RDB_KEY

mkdir /root/.ssh
touch /root/.ssh/known_hosts

(&>/dev/null ssh-keyscan -H $REMOTE_RDB_HOST >> ~/.ssh/known_hosts &)
(&>/dev/null ssh-keyscan -H $RDB_USER_SYSTEM >> ~/.ssh/known_hosts &)

env="$(python3 $RDB_SERVER_FILE_PATH/CreateEnv.py  $1 $2 2>&1)"
sslActive="$(python3 $OPERATION_ON_CONFIG_PATH -getSSLActive $1 -mod $2 2>&1)"
keyCloak="$(python3 $OPERATION_ON_CONFIG_PATH -getKeycloakActive $1 -mod $2 2>&1)"


echo $REMOTE_RDB_HOST
echo $RDB_USER_SYSTEM
echo $RDB_KEY
echo $RDB_SERVER_FILE_PATH
echo $env
echo $sslActive
echo $keyCloak
sleep 100

if [[ $sslActive != "1" ]]; then
    sslComannd='
    sudo cp ~/mycert/mycert.key /var/revdebug/cert;
    sudo cp ~/mycert/mycert.cert /var/revdebug/cert;
    '
else
    sslComannd=''
fi

if [[ $keyCloak != "1" ]]; then
    startCmmand='sudo docker-compose -f docker-compose.keycloak.yml -f docker-compose.yml -p rdb up -d'
else
    startCmmand=' sudo docker-compose -p rdb up -d'
fi


bashCommand='
sudo docker stop $(sudo docker ps -q); 
sudo rm -rf /var/revdebug;
'$sslComannd'
cd '$REVDEBUG_DOCKER_PATH';
echo "
'$env'
" > .env;
sudo docker-compose -f docker-compose.keycloak.yml -f docker-compose.yml -p rdb pull;
'$startCmmand'
'

echo $bashCommand
# ssh -i  $LC_STRESS_KEY_RDB $RDB_USER_SYSTEM@$REMOTE_RDB_HOST  $bashCommand

#Na servie trzeba recznie zrobić ssl i przerzucić rdb-docker-stress 
#lub pobrac repo ale zmodyfikowac taga w dockerze od keycloka >zapisac patha w configu