#!/bin/bash

# gdzie z tym kluczem
chmod 600 server1.pem

# Sztywne ip !!!!!!!!!!!!!
# sztywne pathy!!!!!!
ssh -i  server1.pem azureuser@20.199.122.246  "cd /home/azureuser/stress_test/; bash /home/azureuser/stress_test//start.sh /home/azureuser/stress_test/"