#!/bin/bash
RESULT_PATH=/home/azureuser/Jmeter_test/test/result/
JSON_RAPORT_PATH=/home/azureuser/devopscypresstests/stress.json
RESULT_STATISTICS_PATH=$RESULT_PATH/statistics.json
CYPRESS_PATH=~/devopscypresstests
INIT_JM=/home/azureuser/Jmeter_test/docker-jm/init.sh
RAPORTS_FOLDER=/home/azureuser/Jmeter_test/raports
CONFIG_TEST_FILE_PATH="$4"
#Test names in jmeter:

# YOU MUST SET .CONFIG IN TEST FOLDER


#All sections are divided by _
# 1. Id order
# 2. Testing application name (In devOps)
# 3. Err proportion
# 4. Endpoint type
# 5. Code len (in the case of multiple endpoints (various))

file="$1"

echo $file

sudo python3 get_app_name.py $CONFIG_TEST_FILE_PATH $JSON_RAPORT_PATH $RESULT_STATISTICS_PATH 

#!/bin/sh
STRESS_APP_NAME=`cat tmp.txt`

RAPORT_NAME="$3"  

sudo rm tmp.txt

echo $file

sudo npm run test:linux_before --prefix $CYPRESS_PATH 

echo $file

sudo rm -rf $RESULT_PATH

slave_count="$2"

sudo bash $INIT_JM $slave_count $file

echo $file

sudo npm run test:linux_after  --prefix $CYPRESS_PATH

sudo cat $JSON_RAPORT_PATH

sudo python3 conv.py $file $JSON_RAPORT_PATH $RAPORT_NAME  $CONFIG_TEST_FILE_PATH

#todo after all cp to new folder (date name)
#todo the amount of space used by the recordings
# env CYPRESS_xxx