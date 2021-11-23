#!/bin/bash

test_file="$2"
slave_count="$1"

chmod 600 $LC_STRESS_KEY_JMETER_VM

if [ ! -d /root/.ssh ]; then
    mkdir /root/.ssh
        if [ ! -f /root/.ssh/known_hosts ]; then
            touch /root/.ssh/known_hosts
fi
fi

IP="$(curl https://ipinfo.io/ip)"


ssh-keyscan -H $IP >> ~/.ssh/known_hosts
ssh-keyscan -H $LC_USER_SYSTEM >> ~/.ssh/known_hosts

ssh -i  $LC_STRESS_KEY_JMETER_VM $LC_USER_SYSTEM@$IP  "cd $PATH_/TestStart; . $PATH_/TestStart/initJmeter.sh $test_file  $slave_count $PATH_ "