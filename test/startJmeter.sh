#!/bin/bash

test_file="$2"
slave_count="$1"

chmod 600 $LC_STRESS_KEY_JMETER_VM

mkdir /root/.ssh
touch /root/.ssh/known_hosts

IP="$(curl https://ipinfo.io/ip)"


ssh-keyscan -H $IP >> ~/.ssh/known_hosts
ssh-keyscan -H $LC_USER_SYSTEM >> ~/.ssh/known_hosts

ssh -i  $LC_STRESS_KEY_JMETER_VM $LC_USER_SYSTEM@$IP  "cd $PATH_/test; . $PATH_/test/initJmeter.sh $test_file  $slave_count $PATH_ "