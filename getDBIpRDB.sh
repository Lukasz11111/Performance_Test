#!/bin/bash
RDB_KEY="$(python3 operationOnConfig.py -getRDBKey $1 -mod $2 2>&1)"
REMOTE_RDB_HOST="$(python3 operationOnConfig.py -getRDBHost $1 -mod $2 2>&1)"
RDB_USER_SYSTEM="$(python3 operationOnConfig.py -getRdbDBSysUser $1 -mod $2 2>&1)"
POSTGRESS_CONTAINER_NAME="$(python3 operationOnConfig.py -getPgContainerName $1 -mod $2 2>&1)"


chmod 600 $RDB_KEY

if [ ! -d /root/.ssh ]; then
    mkdir /root/.ssh
        if [ ! -f /root/.ssh/known_hosts ]; then
            touch /root/.ssh/known_hosts
fi
fi


(&>/dev/null ssh-keyscan -H $REMOTE_RDB_HOST >> ~/.ssh/known_hosts  &)
(&>/dev/null ssh-keyscan -H $RDB_USER_SYSTEM >> ~/.ssh/known_hosts  &)

sleep 0.1

REMOTE_COMAND="sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $POSTGRESS_CONTAINER_NAME" 
ipPg=$(ssh -i  $RDB_KEY $RDB_USER_SYSTEM@$REMOTE_RDB_HOST  $REMOTE_COMAND)

export IP_REMOTE_RDB_DB="$ipPg"


