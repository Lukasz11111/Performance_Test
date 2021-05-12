# #!/bin/bash
FOLDERS=tmp_test/*
SLAVE_COUNT=2

date_str=`date +"%m-%d-%y_%H;%M"`
RAPORT_NAME="raports/raport-$date_str.xlsx"

RDB_REMOVE="$1"

echo RevDeBug server restart...
sudo python3 request.py http://20.188.58.169:8888/up n
for x in $FOLDERS; do
  echo "Processing $x folder..."
  FILES=$x/*
  counter=0

  if [ "$(ls -A $FILES)" ]; then
    for f in $FILES; do
      ((counter++))
    done
  fi

  var=$((counter * ((SLAVE_COUNT + 1))))
  i=0
  if [ "$counter" -gt 0 ]; then
    for f in $FILES; do
      echo "Processing $f file..."
      # take action on each file. $f store current file name
      START=0
      END=$SLAVE_COUNT
      for ((VARIABLE = $START; VARIABLE <= $END; VARIABLE++)); do
        ((i++))
        echo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ $i of $var ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sudo bash stress.sh $f $VARIABLE $RAPORT_NAME $x
      done
    done
  fi
done
tmp=`echo $RDB_REMOVE`
R=1
if [[ $tmp == "1" ]]; then
echo RevDeBug instance removing...
sudo python3 request.py http://20.188.58.169:8888/down y
sudo python3 save_data_removing.py $RAPORT_NAME
fi

