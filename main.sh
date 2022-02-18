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

rebuildAppAfterMod="$(python3 operationOnConfig.py -rebuildAppAfterMod 1 2>&1)"
rebuildAppAfterTest="$(python3 operationOnConfig.py -rebuildAppAfterTest 1 2>&1)"
rebuildAppAfterAll="$(python3 operationOnConfig.py -rebuildAppAfterAll 1 2>&1)"

#todo init server/dedulikacja afterstart+retencja

function clearInitRebuild() {
  clear=$1
  init=$2
  rebuild=$3
  idTest=$4
  idMod=$5
  claearServerRdb $clear $init $rebuild $idTest $idMod
}

function claearServerRdb() {
  if [[ $1 == "1" ]]; then
    echo CLEAR SERVER
    . $RDB_SERVER_FILE_PATH/CreateServer.sh $4 $5
  fi

  if [[ $2 == "1" ]]; then
    initDataDef $4 $5
  fi

  if [[ $3 == "1" ]]; then
    rebuildApp $4 $5
  fi
}

function rebuildApp() {
  echo Rebuild Apps
  . $APP_SERVER_FILE_PATH/BuildApp.sh $1 $2 "app"
}

function initDataDef() {
  echo INIT DATA
  rebuildDataGenApp=$(python3 operationOnConfig.py -rebuildDataGenApp $1 -mod $2 2>&1)
  if [[ $rebuildDataGenApp == "1" ]]; then
    . $APP_SERVER_FILE_PATH/BuildApp.sh $1 $2 "gen"
  fi
  . getDBIpRDB.sh $1 $2
  python3 TestApp/DataGeneration.py $1 $2
}

function exec_tests() {
  testsLen=$(expr $1 - 1)
  clearInitRebuild $clearRDBAfterAll $initRDBAll $rebuildAppAfterAll 0 0
  for test in $(seq 0 1 $testsLen); do
    ifTestIsActive=$(python3 operationOnConfig.py -ifTestIsActive $test 2>&1)
    if [[ $ifTestIsActive != "0" ]]; then
      clearInitRebuild $clearRDBAfterTest $initRDBTest $rebuildAppAfterTest $test 0
      typeTest=$(python3 operationOnConfig.py -typeTest $test 2>&1)
      echo $typeTest "sss"
      if [[ $typeTest == "RDB" ]]; then
        echo "Start RevDeBug test"
        bash $RDBTEST $test
      else
        echo "Start App test"
        exec_testsProp $test
      fi
    fi
  done
  clearInitRebuild $clearRDBAfterAll $initRDBAll $rebuildAppAfterAll 0 0
}

function exec_testsProp() {
  proportion=($(python3 operationOnConfig.py -getTestProportion $1 2>&1))
  for proportionVal in "${proportion[@]}"; do
    export ACTUAL_PROPORTION="$proportionVal"
    DELAY_array=($(python3 operationOnConfig.py -getTestDelay $1 2>&1))
    for testDelay in "${DELAY_array[@]}"; do
      exec_testMod $proportionVal $1 $testDelay
    done
  done
  python3 RaportGenerationGoogle.py $1 0 hide
}

function exec_testMod() {
  modesLen=($(python3 operationOnConfig.py -getModeLen $2 2>&1))
  modesIt=$(expr $modesLen - 1)
  for mod in $(seq 0 1 $modesIt); do
    clearInitRebuild $clearRDBAfterMod $initRDBMod $rebuildAppAfterMod $1 $mod
    python3 change_proportion.py $1 $2 $3 $mod
    . getDBIpRDB.sh $2 $mod

    singleTest $2 $mod $3
    rm ./tmp.jmx
  done
}

function singleTest() {
  counterall_done=$(($counterall_done + 1))
  printf '%.0s-' {1..75}
  echo
  echo "$counterall_done  test out of $counterall, estimated total run time: ~$timeTests"
  printf '%.0s-' {1..75}
  echo

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

function customSingleTest() {
  customSingleTest=($(python3 operationOnConfig.py -customSingleTest 1 2>&1))
  slave=$(python3 operationOnConfig.py -slaveingleTest 1 2>&1)

  for test_ in "${customSingleTest[@]}"; do
    bash $INIT_JM $slave $test_
  done

}

file_tests_active="$(python3 operationOnConfig.py -FileTestActiv 1 2>&1)"
app_tests_active="$(python3 operationOnConfig.py -AppTestActiv 1 2>&1)"

if [[ $file_tests_active == "1" ]]; then
  echo "Start file test"
  customSingleTest
fi

if [[ $app_tests_active == "1" ]]; then
  exec_tests $testsLen
fi

echo RUN END
