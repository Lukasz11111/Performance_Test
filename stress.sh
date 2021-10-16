#!/bin/bash
RESULT_PATH=./test/result/
MAIN_PATH="${10}"
FLAG_DEDUPLICATION="${11}"
RESULT_STATISTICS_PATH=$MAIN_PATH/test/result//statistics.json
CYPRESS_PATH="$6"
JSON_RAPORT_PATH=$MAIN_PATH/cy/stress.json
INIT_JM=./docker-jm/init.sh
RAPORTS_FOLDER=./raports
CONFIG_TEST_FILE_PATH="$4"
CHANGE_DELAY_PATH=./change_delay.py 

##Delete this?
CHANGE_info_PATH=./Application/.rdb-info
MODE="$7"
PROP="$8"
RDB_INSTANCE="$9"


#Test names in jmeter:

#TODO budowanie obrazow mastera /slave

# YOU MUST SET .CONFIG IN TEST FOLDER


#All sections are divided by _
# 1. Id order
# 2. Testing application name (In devOps)
# 3. Err proportion
# 4. Endpoint type
# 5. Code len (in the case of multiple endpoints (various))

DELAY="$5"

file="$1"



sudo python3 $CHANGE_DELAY_PATH $file $DELAY

echo $file
 
sudo python3 get_app_name.py $CONFIG_TEST_FILE_PATH $JSON_RAPORT_PATH $RESULT_STATISTICS_PATH 

#!/bin/sh
STRESS_APP_NAME=`cat tmp.txt`

RAPORT_NAME="$3"  

sudo rm tmp.txt

echo $file

date +%s > 'StartTime'


if [ $FLAG_DEDUPLICATION -ne 0 ]; then
       sudo python3 deduplicatiion.py $CONFIG_TEST_FILE_PATH
fi 


# if [ "$CYPRESS_RAPORT_ACTIVE" != "0" ]; then
#  sudo npm run test:linux_before --prefix $CYPRESS_PATH -- --env RDB_HOSTNAME=$RDB_INSTANCE
# fi

echo $file

sudo rm -rf $RESULT_PATH

slave_count="$2"

sudo bash $INIT_JM $slave_count $file

echo $file

# if [ "$CYPRESS_RAPORT_ACTIVE" != "0" ]; then
# sudo npm run test:linux_after  --prefix $CYPRESS_PATH -- --env RDB_HOSTNAME=$RDB_INSTANCE
# sudo cat $JSON_RAPORT_PATH


echo sudo python3 conv.py $PROP $JSON_RAPORT_PATH $RAPORT_NAME  $CONFIG_TEST_FILE_PATH $CHANGE_info_PATH $DELAY $MODE
sudo python3 conv.py $PROP $JSON_RAPORT_PATH $RAPORT_NAME  $CONFIG_TEST_FILE_PATH $CHANGE_info_PATH $DELAY $MODE 
# fi

#todo after all cp to new folder (date name)
#todo the amount of space used by the recordings
# env CYPRESS_xxx