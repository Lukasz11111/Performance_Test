#!/bin/bash

chmod 600 $LC_STRESS_KEY_RDB
REMOTE_RDB_HOST="$(python3 operationOnConfig.py -getRDBHost $1 2>&1)"
echo $REMOTE_RDB_HOST
mkdir /root/.ssh
touch /root/.ssh/known_hosts

ssh-keyscan -H $REMOTE_RDB_HOST >> ~/.ssh/known_hosts
ssh-keyscan -H $RDB_USER_SYSTEM >> ~/.ssh/known_hosts
REMOTE_COMAND="sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $POSTGRESS_CONTAINER_NAME" 
ipPg=$(ssh -i  $LC_STRESS_KEY_RDB $RDB_USER_SYSTEM@$REMOTE_RDB_HOST  $REMOTE_COMAND)

export IP_REMOTE_RDB_DB="$ipPg"


