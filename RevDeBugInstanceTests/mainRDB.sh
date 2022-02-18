
idTest="$1"
idMod=0


function startJM(){
rm -rf $RESULT_PATH
SLAVE_COUNT="$(python3 operationOnConfig.py -getSlave $idTest -mod $idMod 2>&1)"
bash $INIT_JM $SLAVE_COUNT $TEST_FILE_RDB
 if_raport_gen="$(python3 operationOnConfig.py -ifRaportGen $idTest -mod $idMod 2>&1)"
  if [[ $if_raport_gen != "0" ]]; then
   echo gen raport
   python3 $GEN_RDB_RAPORT $idTest $idMod $1
  fi

  restartAfterRun=$(python3 operationOnConfig.py -RDBrestartAfterSingleRun $1 -mod $2 2>&1)
  if [[ $restartAfterRun == "1" ]]; then
  echo Restart RevDeBug
    . $RESTART_RDB
    sleep 30
  fi
}


function itAll(){
  DELAY_array=($(python3 operationOnConfig.py -getTestDelay $idTest 2>&1))
for testDelay in "${DELAY_array[@]}"; do 
    python3 RevDeBugInstanceTests/GetCookis.py  $idTest $idMod $testDelay
    startJM $testDelay
done
 if_raport_gen="$(python3 operationOnConfig.py -ifRaportGen $idTest -mod $idMod 2>&1)"
  if [[ $if_raport_gen != "0" ]]; then
   python3 $GEN_RDB_RAPORT $idTest $idMod hide
  fi
}

itAll