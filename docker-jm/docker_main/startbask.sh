#!/bin/bash

chmod 600 server1.pem

mkdir /root/.ssh
touch /root/.ssh/known_hosts

IP="$(curl https://ipinfo.io/ip)"
# PATH_="$(readlink -f ../..)"

ssh-keyscan -H $IP >> ~/.ssh/known_hosts
ssh-keyscan -H azureuser >> ~/.ssh/known_hosts

ssh -i  server1.pem azureuser@$IP  "cd $PATH_; export POSTGRESS_CONTAINER_NAME=$POSTGRESS_CONTAINER_NAME; . $PATH_/start.sh $PATH_"