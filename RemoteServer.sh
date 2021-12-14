#!/bin/bash
KEY=$1
REMOTE_HOST=$2
USER_SYSTEM=$3
BASHCOMMAND=$4

chmod 600 $KEY

if [ ! -d /root/.ssh ]; then
    mkdir /root/.ssh
        if [ ! -f /root/.ssh/known_hosts ]; then
            touch /root/.ssh/known_hosts
fi
fi

(&>/dev/null ssh-keyscan -H $REMOTE_HOST >> ~/.ssh/known_hosts &)
(&>/dev/null ssh-keyscan -H $USER_SYSTEM >> ~/.ssh/known_hosts &)


sleep 1
ssh -i $KEY $USER_SYSTEM@$REMOTE_HOST  "$BASHCOMMAND";



