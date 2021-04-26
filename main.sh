# #!/bin/bash
FOLDERS=tmp_test/*
SLAVE_COUNT=3

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
        sudo bash stress.sh $f $VARIABLE
      done
    done
  fi
done
