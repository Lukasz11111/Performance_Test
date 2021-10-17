#!/bin/bash

test_file="$2"
slave_count="$1"

chmod 600 ./test/server1.pem

mkdir /root/.ssh
touch /root/.ssh/known_hosts

IP="$(curl https://ipinfo.io/ip)"


ssh-keyscan -H $IP >> ~/.ssh/known_hosts
ssh-keyscan -H azureuser >> ~/.ssh/known_hosts

ssh -i  ./test/server1.pem azureuser@$IP  "cd $PATH_/test; . $PATH_/test/initJmeter.sh $test_file  $slave_count $PATH_ "