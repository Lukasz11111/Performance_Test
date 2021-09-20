#!/bin/bash

chmod 600 server1.pem

mkdir /root/.ssh
touch /root/.ssh/known_hosts

IP="$(curl https://ipinfo.io/ip)"
# PATH_="$(readlink -f ../..)"

echo $PATH_

ssh-keyscan -H $IP >> ~/.ssh/known_hosts
ssh-keyscan -H azureuser >> ~/.ssh/known_hosts

ssh -i  server1.pem azureuser@$IP  "export CYPRESS_RAPORT_ACTIVE=${CYPRESS_RAPORT_ACTIVE:-'1'}; export CYPRESS_DEDUPLICATION=${CYPRESS_DEDUPLICATION:-'1'}; cd $PATH_; . $PATH_/start.sh $PATH_"