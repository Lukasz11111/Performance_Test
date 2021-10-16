#!/bin/bash
FOLDERS=Application/*
SLAVE_COUNT=0

date_str=$(date +"%m-%d-%y_%H;%M")
RAPORT_NAME="raport-$date_str.xlsx"

RDB_REMOVE="$1"
MAIN_PATH="$3"
CYPRESS_PATH=./cy

CHANGE_TEST_HOST_PATH=./change_test_host.py

sudo rm -rf ./dict_legend.txt

counterall=0
counterall_done=0

START=0
END=$SLAVE_COUNT


for x in $FOLDERS; do
active_folder=$(python3 if_folder_is_active.py $x/.config 2>&1)
  if [[ $active_folder != "0" ]]; then
    if [ "$CYPRESS_DEDUPLICATION" != "0" ]; then
    rdb_hostname=$(python3 get_ip_rdb_instance.py $x/.config 2>&1)
    fi
  fi
done


for x in $FOLDERS; do
active_folder=$(python3 if_folder_is_active.py $x/.config 2>&1)
if [[ $active_folder != "0" ]]; then
DELAY_array=($(python3 delay.py $x/.config 2>&1))
for mode in 1 2 3 4; do
  active_mod_host_port=$(python3 rdb_module.py $x/.config $mode 2>&1)
  if [[ $active_mod_host_port != "0" ]]; then
    for i in "${DELAY_array[@]}"; do
      for ((VARIABLE = $START; VARIABLE <= $END; VARIABLE++)); do
          if [ ! -f $x/.config ]; then
            echo "File not found!"
          else
            for prop in 100 95 90 85 80 75 70 65 60 55 50 45 40 35 30 25 20 15 10 5 0; do
              proportion_on=$(python3 if_this_proportion_is_on.py $x/.config $prop 2>&1)
              if [[ $proportion_on == "1" ]]; then
                ((counterall++))
              fi
            done
          fi

        
      done
    done
  fi
done
fi
done

for x in $FOLDERS; do
deduplication=1
active_folder=$(python3 if_folder_is_active.py $x/.config 2>&1)
if [[ $active_folder != "0" ]]; then
DELAY_array=($(python3 delay.py $x/.config 2>&1))
  if [ ! -f $x/.config ]; then
    echo "File not found!"
  else

    echo "Processing $x folder..."
    for prop in 100 95 90 85 80 75 70 65 60 55 50 45 40 35 30 25 20 15 10 5 0; do
      proportion_on=$(python3 if_this_proportion_is_on.py $x/.config $prop 2>&1)
      if [[ $proportion_on == "1" ]]; then
        FILES=$x/*
        counter=0
        
        sudo python3 change_proportion.py model.jmx $x/.config $prop
        sudo cp tmp.jmx $x/tmp.jmx
        test_file=$x/tmp.jmx
        i=0

        for iZ in "${DELAY_array[@]}"; do
          for mode in 1 2 3 4; do
            active_mod_host_port=$(python3 rdb_module.py $x/.config $mode 2>&1)
            if [[ $active_mod_host_port != "0" ]]; then
              rdb_hostname=$(python3 get_ip_rdb_instance.py $x/.config 2>&1)
              sudo python3 $CHANGE_TEST_HOST_PATH $test_file $active_mod_host_port $x/.config
              echo "Processing $test_file file..."
            
              START=0
              END=$SLAVE_COUNT
              for ((VARIABLE = $START; VARIABLE <= $END; VARIABLE++)); do
                ((i++))
                ((counterall_done++))
                echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ $counterall_done of $counterall ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ $i of $var from folder ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
               sudo bash stress.sh $test_file 5 $RAPORT_NAME $x $iZ $CYPRESS_PATH $mode $prop $rdb_hostname $MAIN_PATH $deduplication
              deduplication=0
              done

            fi

          done
        done

      fi

    done
  fi
  fi
  sudo rm $x/tmp.jmx
done

echo RUN END
