#!/bin/bash
RDB_KEY="$(python3 operationOnConfig.py -getRDBKey $1 -mod $2 2>&1)"
REMOTE_RDB_HOST="$(python3 operationOnConfig.py -getRDBHost $1 -mod $2 2>&1)"
RDB_USER_SYSTEM="$(python3 operationOnConfig.py -getRdbDBSysUser $1 -mod $2 2>&1)"
POSTGRESS_CONTAINER_NAME="$(python3 operationOnConfig.py -getPgContainerName $1 -mod $2 2>&1)"

sleep 0.1

REMOTE_COMAND="sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $POSTGRESS_CONTAINER_NAME" 

ipPg=$(. RemoteServer.sh $RDB_KEY $REMOTE_RDB_HOST $RDB_USER_SYSTEM "$REMOTE_COMAND")

export IP_REMOTE_RDB_DB="$ipPg"


