#!/bin/bash

. SetStaticPath.sh

RDB_REMOVE="$1"

counterall_done=0

counterall="$(python3 operationOnConfig.py -getCountOfAllTest 1 2>&1)"

testsLen="$(python3 operationOnConfig.py -getTestsLen 1 2>&1 >/dev/null)"

timeTests="$(python3 operationOnConfig.py -approximateTime 1 2>&1)"


initRDBAll="$(python3 operationOnConfig.py -initServerAll 1 2>&1)"
initRDBTest="$(python3 operationOnConfig.py -initServerTest 1 2>&1)"
initRDBMod="$(python3 operationOnConfig.py -initServerMod 1 2>&1)"

clearRDBAfterMod="$(python3 operationOnConfig.py -clearRDBAfterMod 1 2>&1)"
clearRDBAfterTest="$(python3 operationOnConfig.py -clearRDBAfterTest 1 2>&1)"
clearRDBAfterAll="$(python3 operationOnConfig.py -clearRDBAfterAll 1 2>&1)"


#todo init server/dedulikacja afterstart+retencja
function claearServerRdb(){
  if [[ $1 == "1" ]]; then
    echo CLEAR SERVER
        # . $RDB_SERVER_FILE_PATH/CreateServer.sh $2 $3
      fi
initData="$(python3 operationOnConfig.py -initData $2 -mod $3 2>&1)"
echo $initData
  if [[ $initData == "1" ]]; then
  echo INIT DATA
    . getDBIpRDB.sh $2 $3
    python3 DataGenerationApp/DataGeneration.py $2 $3
  fi
}

function exec_tests(){
  testsLen=$(expr $1 - 1)
  claearServerRdb $initRDBAll 0 0 $initData

  for test in $(seq 0 1 $testsLen); do
    ifTestIsActive=$(python3 operationOnConfig.py -ifTestIsActive $test 2>&1)
      if [[ $ifTestIsActive != "0" ]]; then
        claearServerRdb $initRDBTest $test 0
          exec_testsProp  $test
          claearServerRdb $clearRDBAfterTest $test 0
      fi   
  done
  claearServerRdb $clearRDBAfterAll 0 0 
}

function exec_testsProp(){
 proportion=($(python3 operationOnConfig.py -getTestProportion $1 2>&1))
    for proportionVal in "${proportion[@]}"; do
      DELAY_array=($(python3 operationOnConfig.py -getTestDelay $1 2>&1))
      for testDelay in "${DELAY_array[@]}"; do
          exec_testMod  $proportionVal $1 $testDelay
        done
      done
     python3 RaportGenerationGoogle.py $1 0 hide
}

function exec_testMod(){
    modesLen=($(python3 operationOnConfig.py -getModeLen $2 2>&1))
    modesIt=$(expr $modesLen - 1)
    for mod in $(seq 0 1 $modesIt); do
      claearServerRdb $initRDBMod $test $mod
      python3 change_proportion.py $1 $2 $3 $mod
      . getDBIpRDB.sh $2 $mod
      
     
      singleTest $2 $mod $3
      rm ./tmp.jmx
      claearServerRdb $clearRDBAfterMod $1 $mod
    done
}

function singleTest(){
counterall_done=$[$counterall_done +1]
printf '%.0s-' {1..75}; echo
echo "$counterall_done  test out of $counterall, estimated total run time: ~$timeTests"
printf '%.0s-' {1..75}; echo
  
python3 GetTraceBefore.py $1 $2

rm -rf $RESULT_PATH

SLAVE_COUNT="$(python3 operationOnConfig.py -getSlave $1 -mod $2 2>&1)"

bash $INIT_JM $SLAVE_COUNT $TMP_TEST_FILE
python3 GetRecordingAndTrace.py $1 $2

if_raport_gen="$(python3 operationOnConfig.py -ifRaportGen $1 -mod $2 2>&1)"

 if [[ $if_raport_gen != "0" ]]; then
python3 RaportGenerationGoogle.py $1 $2 $3
 fi 

}


function customSingleTest(){
customSingleTest=($(python3 operationOnConfig.py -customSingleTest 1 2>&1))
slave=$(python3 operationOnConfig.py -slaveingleTest 1 2>&1)
for test_ in "${customSingleTest[@]}"; do
        bash $INIT_JM $slave $test_
done

}

single_tests_active="$(python3 operationOnConfig.py -singleTestsActive 1 2>&1)"


if [[ $single_tests_active != "1" ]]; then
    exec_tests $testsLen
else
customSingleTest 
fi


echo RUN END

