#!/bin/bash
FOLDERS=TestsConfig/*
SLAVE_COUNT=0

date_str=$(date +"%m-%d-%y_%H;%M")
RAPORT_NAME="raport-$date_str.xlsx"

RDB_REMOVE="$1"

CYPRESS_PATH=./cy

CHANGE_TEST_HOST_PATH=./change_test_host.py

 rm -rf ./dict_legend.txt

# counterall=0
counterall_done=0

START=0
END=$SLAVE_COUNT





counterall="$(python3 operationOnConfig.py -getCountOfAllTest 1 2>&1)"

testsLen="$(python3 operationOnConfig.py -getTestsLen 1 2>&1 >/dev/null)"



function exec_tests(){
  testsLen=$(expr $1 - 1)
  for test in $(seq 0 1 $testsLen); do
    deduplication=1
    ifTestIsActive=$(python3 operationOnConfig.py -ifTestIsActive $test 2>&1)
      if [[ $active_folder != "0" ]]; then
          exec_testsProp $deduplication $test
      fi
  done
}

function exec_testsProp(){
    DELAY_array=($(python3 operationOnConfig.py -getTestDelay $2 2>&1))
    for testDelay in "${DELAY_array[@]}"; do
    # todo odkomentuj to 
      # . getRemoteIpRDB.sh $2
      proportion=($(python3 operationOnConfig.py -getTestProportion $2 2>&1))
        for proportionVal in "${proportion[@]}"; do
          python3 change_proportion.py model.jmx $proportionVal
        done
      done
}


exec_tests $testsLen



# active_folder=$(python3 if_folder_is_active.py $file_in_folder/.config 2>&1)
# if [[ $active_folder != "0" ]]; then
# DELAY_array=($(python3 delay.py $file_in_folder/.config 2>&1))

#   if [ ! -f $file_in_folder/.config ]; then
#     echo "File not found!"
#   else

#     . getRemoteIpRDB.sh $file_in_folder
#     echo "Processing $file_in_folder folder..."
#     for prop in 100 95 90 85 80 75 70 65 60 55 50 45 40 35 30 25 20 15 10 5 0; do
#       proportion_on=$(python3 if_this_proportion_is_on.py $file_in_folder/.config $prop 2>&1)
#       if [[ $proportion_on == "1" ]]; then
     



#          python3 change_proportion.py model.jmx $file_in_folder/.config $prop
#          mv tmp.jmx $file_in_folder/tmp.jmx
#         test_file=$file_in_folder/tmp.jmx
#         i=0

#         for iZ in "${DELAY_array[@]}"; do
#           for mode in 1 2 3 4; do
#             active_mod_host_port=$(python3 rdb_module.py $file_in_folder/.config $mode 2>&1)
#             if [[ $active_mod_host_port != "0" ]]; then
#                python3 $CHANGE_TEST_HOST_PATH $test_file $active_mod_host_port $file_in_folder/.config
#               echo "Processing $test_file file..."
            
#               START=0
#               END=$SLAVE_COUNT
#               for ((VARIABLE = $START; VARIABLE <= $END; VARIABLE++)); do
#                 ((i++))
#                 ((counterall_done++))
#                 echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ $counterall_done of $counterall ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                 echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ $i of $var from folder ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#                 bash stress.sh $test_file $RAPORT_NAME $file_in_folder $iZ  $mode $prop  $deduplication $POSTGRESS_CONTAINER_NAME
#               deduplication=0
#               done

#             fi

#           done
#         done

#       fi

#     done
#   fi
#    rm $file_in_folder/tmp.jmx
#   fi


echo RUN END

