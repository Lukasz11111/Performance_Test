#!/bin/bash
date_str=$(date +"%m%d%y%H%M")
export RUN_ID=$date_str
export JSON_CONFIG="TestsConfig/Configuration.json"
export RESULT_PATH="TestResult/result/"
export RESULT_STATISTICS_PATH="TestResult/result/statistics.json"
export JSON_RAPORT_PATH="TestResult/stress.json"


export INIT_JM="TestStart/startJmeter.sh"
export RAPORTS_FOLDER="./Raports"
export TMP_TEST_FILE="./tmp.jmx"
export MODEL_TEST_FILE="./model.jmx"
export LOG_PATH="TestResult/path/jmeter.log"

export OPERATION_ON_CONFIG_PATH="/app/operationOnConfig.py"

export RDB_SERVER_FILE_PATH='RevDeBugServer/'
export APP_SERVER_FILE_PATH='TestApp/'
export RDBTEST='RevDeBugInstanceTests/mainRDB.sh'

export MODEL_TEST_FILE_RDB='RevDeBugInstanceTests/modelRDB.jmx'
export TEST_FILE_RDB='RevDeBugInstanceTests/testFile.jmx'
export RESTART_RDB='RevDeBugInstanceTests/restartRDB.sh'
export GEN_RDB_RAPORT="RevDeBugInstanceTests/GenGoogleRaport.py"
