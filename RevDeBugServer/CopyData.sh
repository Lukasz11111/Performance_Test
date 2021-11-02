#!/bin/bash

chmod 600 $LC_STRESS_KEY_RDB

mkdir /root/.ssh
touch /root/.ssh/known_hosts

IP="$1"

ssh-keyscan -H $IP >> ~/.ssh/known_hosts
ssh-keyscan -H $RDB_USER_SYSTEM >> ~/.ssh/known_hosts

ssh -i  $LC_STRESS_KEY_RDB $RDB_USER_SYSTEM@$IP  '
sudo docker stop $(sudo docker ps -q); 
sudo rm -rf /var/revdebugBackup;
sudo cp -r /var/revdebug /var/revdebugBackup/;

cd rdb-stress;
sudo docker-compose -p rdb up -d;
'
