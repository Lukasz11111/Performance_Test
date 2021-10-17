#!/bin/bash
KEY="$1"
IP="$2"
USER="$3"
POSTGRESS_CONTAINER_NAME="$4"

echo $POSTGRESS_CONTAINER_NAME

sudo chmod 600 $KEY

mkdir /root/.ssh
touch /root/.ssh/known_hosts

ssh-keyscan -H $IP >> ~/.ssh/known_hosts
ssh-keyscan -H $USER >> ~/.ssh/known_hosts
REMOTE_COMAND="sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $POSTGRESS_CONTAINER_NAME" 
ipPg=$(ssh -i  $KEY $USER@$IP  $REMOTE_COMAND)

