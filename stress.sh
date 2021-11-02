#!/bin/bash
RESULT_PATH=./test/result/
RESULT_STATISTICS_PATH=.test/result/statistics.json
JSON_RAPORT_PATH=./test/stress.json
INIT_JM=./test/startJmeter.sh
RAPORTS_FOLDER=./raports
CHANGE_info_PATH=./Application/.rdb-info

JMETER_FILE="$1"
CONFIG_TEST_FILE_PATH="$3"
RAPORT_NAME="$2"
DELAY="$4"
MODE="$5"
PROPORTION="$6"
FLAG_DEDUPLICATION="$7"
POSTGRESS_CONTAINER_NAME="$8"

 python3 change_delay.py $JMETER_FILE $DELAY

 python3 get_app_name.py $CONFIG_TEST_FILE_PATH $JSON_RAPORT_PATH $RESULT_STATISTICS_PATH 

date +%s > '.StartTime'



if [ $FLAG_DEDUPLICATION -ne 0 ]; then
chmod 777 deduplicatiion.py
        python3 deduplicatiion.py $CONFIG_TEST_FILE_PATH
fi 

rm -rf $RESULT_PATH

python3 get_trace_beafore.py $CONFIG_TEST_FILE_PATH

bash $INIT_JM 6 $JMETER_FILE

echo $CONFIG_TEST_FILE_PATH 
python3 get_recording_and_trace.py $CONFIG_TEST_FILE_PATH

rm -rf .StartTime

echo  python3 conv.py $PROPORTION $JSON_RAPORT_PATH $RAPORT_NAME  $CONFIG_TEST_FILE_PATH $CHANGE_info_PATH $DELAY $MODE
python3 conv.py $PROPORTION $JSON_RAPORT_PATH $RAPORT_NAME  $CONFIG_TEST_FILE_PATH $CHANGE_info_PATH $DELAY $MODE 


#todo after all cp to new folder (date name)
#todo the amount of space used by the recordings
# env CYPRESS_xxx