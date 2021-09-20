#!/bin/bash

chmod 600 server1.pem

readlink -f file.txt

mkdir /root/.ssh
touch /root/.ssh/known_hosts

IP="$(curl https://ipinfo.io/ip)"
PATH="$(readlink -f ../..)"

ssh-keyscan -H $IP >> ~/.ssh/known_hosts
ssh-keyscan -H azureuser >> ~/.ssh/known_hosts

ssh -i  server1.pem azureuser@$IP  "export CYPRESS_RAPORT_ACTIVE=${CYPRESS_RAPORT_ACTIVE:-'1'}; export CYPRESS_DEDUPLICATION=${CYPRESS_DEDUPLICATION:-'1'}; cd $PATH; . $PATH/start.sh $PATH"