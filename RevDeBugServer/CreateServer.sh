#!/bin/bash

chmod 600 $LC_STRESS_KEY_RDB

mkdir /root/.ssh
touch /root/.ssh/known_hosts

IP="$1"

ssh-keyscan -H $IP >> ~/.ssh/known_hosts
ssh-keyscan -H $RDB_USER_SYSTEM >> ~/.ssh/known_hosts

ssh -i  $LC_STRESS_KEY_RDB $RDB_USER_SYSTEM@$IP  '
sudo docker stop $(sudo docker ps -q); 
sudo rm -rf /var/revdebug;
sudo rm -rf rdb-stress;
git clone https://github.com/RevDeBug/revdebug-server-docker-compose rdb-stress;
cd rdb-stress;
echo "
REVDEBUG_AUTH='$REVDEBUG_AUTH'
# Server fully qualified domain name
REVDEBUG_SERVER_NAME='$REVDEBUG_SERVER_NAME'
# Below settings can be left as they are and are optional
REVDEBUG_ROOTVOLUME_PATH=/var/revdebug
REVDEBUG_VOLUME_PATH=/var/revdebug/server/repo
REVDEBUG_VOLUME_CAPATH=/var/revdebug/ca
# Put the crt (public key) and pem (private key) certificate files here
REVDEBUG_CERTIFICATE_PATH=/var/revdebug/cert
# File name of certificate files without the extensions
REVDEBUG_CERTIFICATE_NAME='$REVDEBUG_CERTIFICATE_NAME'
REVDEBUG_KEEP_ACCESS_LOGS=false
# Default version, do not change.
REVDEBUG_DOCKER_TAG='$REVDEBUG_DOCKER_TAG'
" > .env
sudo docker-compose -p rdb up -d;
'
