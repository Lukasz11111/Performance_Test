# #!/bin/bash
FOLDERS=tmp_test/*
SLAVE_COUNT=0

date_str=$(date +"%m-%d-%y_%H;%M")
RAPORT_NAME="raports/raport-$date_str.xlsx"

RDB_REMOVE="$1"
PATH="$3"
CYPRESS_PATH=~/devopscypresstests

CHANGE_TEST_HOST_PATH=./change_test_host.py

# echo RevDeBug server restart...
# #rdb server
# sudo python3 request.py http://20.188.58.169:8888/up n
# sleep 50
# # apps
# echo Applcations server restart...
# sudo python3 request.py http://40.89.147.34:8888 n
# sleep 45

# (cd $CYPRESS_PATH && sudo npm run test:linux_deduplication --prefix $CYPRESS_PATH && cd $PATH)

counterall=0
counterall_done=0
# 5000 2500 2000 1500 1000 500 50
START=0
END=$SLAVE_COUNT

DELAY="$2"
case $DELAY in
1)
  DELAY_array=(0 1000)
  ;;
2)
  DELAY_array=(10 100 250 500 1000 1500 10000)
  ;;
3)
  DELAY_array=(10 50 100 150 250 400 500 600 750 1000 1500 2000 3000 5000 10000)
  ;;
*)
  DELAY_array=(0)
  ;;
esac
for mode in 1 2 3 4; do
active_mod_host_port=$(python3 rdb_module.py ./tmp_test/java_rdbapm/.config $mode 2>&1)
  if [[ $active_mod_host_port != "0" ]]; then
    for i in "${DELAY_array[@]}"; do
      for ((VARIABLE = $START; VARIABLE <= $END; VARIABLE++)); do
        for x in $FOLDERS; do
          FILES=$x/*
          if [ "$(ls -A $FILES)" ]; then
            for test_file in $FILES; do
              ((counterall++))
              echo $counterall
            done
          fi
        done
      done
    done
  fi
done

for x in $FOLDERS; do
  echo "Processing $x folder..."
  FILES=$x/*
  counter=0

  if [ "$(ls -A $FILES)" ]; then
    for iZ in "${DELAY_array[@]}"; do
      for test_file in $FILES; do
        ((counter++))
      done
    done
  fi

  var=$((counter * ((SLAVE_COUNT + 1))))
  i=0
  if [ "$counter" -gt 0 ]; then
    for test_file in $FILES; do
      for iZ in "${DELAY_array[@]}"; do
        for mode in 1 2 3 4; do
        active_mod_host_port=$(python3 rdb_module.py ./tmp_test/java_rdbapm/.config $mode 2>&1)
          if [[ $active_mod_host_port != "0" ]]; then
            echo $mode
            echo $active_mod_host_port
            sudo python3 $CHANGE_TEST_HOST_PATH $test_file $active_mod_host_port
            echo "Processing $test_file file..."
            # take action on each file. $test_file store current file name
            START=0
            END=$SLAVE_COUNT
            for ((VARIABLE = $START; VARIABLE <= $END; VARIABLE++)); do
              ((i++))
              ((counterall_done++))
              echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ $counterall_done of $counterall ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ $i of $var from folder ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
              echo $iZ

              sudo bash stress.sh $test_file 5 $RAPORT_NAME $x $iZ $CYPRESS_PATH $mode

            done

          fi

        done
      done
    done
  fi

done

# tmp=$(echo $RDB_REMOVE)
# R=1
# if [[ $tmp == "1" ]]; then
#   echo RevDeBug instance removing...
#   sudo python3 request.py http://20.188.58.169:8888/down y
#   sudo python3 save_data_removing.py $RAPORT_NAME
#   echo Applcations server restart...
#   sudo python3 request.py http://40.89.147.34:8888 n
# fi
echo RUN END
