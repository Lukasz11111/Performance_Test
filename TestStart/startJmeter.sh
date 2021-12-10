#!/bin/bash

test_file="$2"
slave_count="$1"


RDB_KEY=$LC_STRESS_KEY_JMETER_VM
USER_SYSTEM=$LC_USER_SYSTEM


if [ ! -d /root/.ssh ]; then
    mkdir /root/.ssh
        if [ ! -f /root/.ssh/known_hosts ]; then
            touch /root/.ssh/known_hosts
fi
fi

IP="$(curl https://ipinfo.io/ip)"


chmod 600 $RDB_KEY

if [ ! -d /root/.ssh ]; then
    mkdir /root/.ssh
        if [ ! -f /root/.ssh/known_hosts ]; then
            touch /root/.ssh/known_hosts
fi
fi

(&>/dev/null ssh-keyscan -H $IP >> ~/.ssh/known_hosts &)
(&>/dev/null ssh-keyscan -H $RDB_USER_SYSTEM >> ~/.ssh/known_hosts &)

sleep 1

ssh -i  $RDB_KEY $RDB_USER_SYSTEM@$IP  "cd $PATH_/TestStart; . $PATH_/TestStart/initJmeter.sh $test_file  $slave_count $PATH_ "