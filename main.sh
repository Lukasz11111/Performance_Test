# #!/bin/bash
FOLDERS=tmp_test/*
SLAVE_COUNT=0

date_str=$(date +"%m-%d-%y_%H;%M")
RAPORT_NAME="raports/raport-$date_str.xlsx"

RDB_REMOVE="$1"

echo RevDeBug server restart...
#rdb server
sudo python3 request.py http://20.188.58.169:8888/up n
sleep 50
#apps
echo Applcations server restart...
sudo python3 request.py http://40.89.147.34:8888 n
sleep 45

counterall=0
counterall_done=0
# 5000 2500 2000 1500 1000 500 50
START=0
END=$SLAVE_COUNT

DELAY="$2"
case $DELAY in
1)
  DELAY_array=(0 1 10 500 1000)
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

for i in "${DELAY_array[@]}"; do
  for ((VARIABLE = $START; VARIABLE <= $END; VARIABLE++)); do
    for x in $FOLDERS; do
      FILES=$x/*
      if [ "$(ls -A $FILES)" ]; then
        for f in $FILES; do
          ((counterall++))
        done
      fi
    done
  done
done

for x in $FOLDERS; do
  echo "Processing $x folder..."
  FILES=$x/*
  counter=0

  if [ "$(ls -A $FILES)" ]; then
    for iZ in "${DELAY_array[@]}"; do
      for f in $FILES; do
        ((counter++))
      done
    done
  fi

  var=$((counter * ((SLAVE_COUNT + 1))))
  i=0
  if [ "$counter" -gt 0 ]; then
    for iZ in "${DELAY_array[@]}"; do
      for f in $FILES; do
        echo "Processing $f file..."
        # take action on each file. $f store current file name
        START=0
        END=$SLAVE_COUNT
        for ((VARIABLE = $START; VARIABLE <= $END; VARIABLE++)); do
          ((i++))
          ((counterall_done++))
          echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ $counterall_done of $counterall ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ $i of $var from folder ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
          echo $iZ
          sudo bash stress.sh $f 5 $RAPORT_NAME $x $iZ

        done
      done
    done

  fi

done

tmp=$(echo $RDB_REMOVE)
R=1
# if [[ $tmp == "1" ]]; then
#   echo RevDeBug instance removing...
#   sudo python3 request.py http://20.188.58.169:8888/down y
#   sudo python3 save_data_removing.py $RAPORT_NAME
# fi
