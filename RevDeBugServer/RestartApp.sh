#!/bin/bash

            
chmod 600 $LC_STRESS_KEY_APP

mkdir /root/.ssh
touch /root/.ssh/known_hosts

IP="$1"
APP_PATH="$2"

ssh-keyscan -H $IP >> ~/.ssh/known_hosts
ssh-keyscan -H $APP_USER_SYSTEM >> ~/.ssh/known_hosts

ssh -i  $LC_STRESS_KEY_APP $APP_USER_SYSTEM@$IP  '
cd '$APPS_PATH'/'$APP_PATH';
sudo docker-compose down;
sudo docker-compose build;
sudo docker-compose up -d;
'
