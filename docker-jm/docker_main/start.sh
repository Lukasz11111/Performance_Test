#!/bin/bash
chmod 600 server1.pem
ssh -i  server1.pem azureuser@20.43.39.179  "cd /home/azureuser/Jmeter_test; bash /home/azureuser/Jmeter_test/start.sh"