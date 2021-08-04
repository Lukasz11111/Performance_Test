#!/bin/bash

# gdzie z tym kluczem
chmod 600 server1.pem

# Sztywne ip !!!!!!!!!!!!!
# sztywne pathy!!!!!!
mkdir /root/.ssh
touch /root/.ssh/known_hosts

ssh-keyscan -H 20.199.122.246 >> ~/.ssh/known_hosts
ssh-keyscan -H azureuser >> ~/.ssh/known_hosts

ssh -i  server1.pem azureuser@20.199.122.246  "export CYPRESS_RAPORT_ACTIVE=${CYPRESS_RAPORT_ACTIVE:-'1'}; export CYPRESS_DEDUPLICATION=${CYPRESS_DEDUPLICATION:-'1'}; cd /home/azureuser/stress_test/; . /home/azureuser/stress_test/start.sh /home/azureuser/stress_test/"