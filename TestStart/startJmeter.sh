#!/bin/bash

test_file="$2"
slave_count="$1"


RDB_KEY=$LC_STRESS_KEY_JMETER_VM
USER_SYSTEM=$LC_USER_SYSTEM

IP="$(curl https://ipinfo.io/ip)"

bashCommand="cd $PATH_/TestStart; . $PATH_/TestStart/initJmeter.sh $test_file  $slave_count $PATH_ "
. RemoteServer.sh $RDB_KEY $IP $RDB_USER_SYSTEM "$bashCommand"
