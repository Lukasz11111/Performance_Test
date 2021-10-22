#!/bin/bash


JSON_CONFIG_PATH="$1"
chmod 600 $LC_STRESS_KEY_RDB
REMOTE_RDB_HOST=$(python3 get_ip_rdb_instance.py $JSON_CONFIG_PATH/.config 2>&1)
mkdir /root/.ssh
touch /root/.ssh/known_hosts

ssh-keyscan -H $REMOTE_RDB_HOST >> ~/.ssh/known_hosts
ssh-keyscan -H $RDB_USER_SYSTEM >> ~/.ssh/known_hosts
REMOTE_COMAND="sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $POSTGRESS_CONTAINER_NAME" 
ipPg=$(ssh -i  $LC_STRESS_KEY_RDB $RDB_USER_SYSTEM@$REMOTE_RDB_HOST  $REMOTE_COMAND)

export IP_REMOTE_RDB_DB="$ipPg"


