#!/bin/bash
RESULT_PATH=/home/azureuser/Jmeter_test/result
JMETER_PATH=/home/azureuser/jmeter/apache-jmeter-5.4/bin/jmeter
JSON_RAPORT_PATH=/home/azureuser/devopscypresstests/stress.json
RESULT_STATISTICS_PATH=$RESULT_PATH/statistics.json
CYPRESS_PATH=~/devopscypresstests

#Test names in jmeter:

#All sections are divided by _
# 1. application language name (dotnet,java,js,python)
# 2. Called endpoints, divided by "-"
# 3. Endpoint type
# 4. Code len (in the case of multiple endpoints (various))
# 5. Number of threads
# 6. Repeat calls
# 7. Test time
# 8. Testing application name (In devOps)


file="$1"

sudo python3 get_app_name.py $file $JSON_RAPORT_PATH $RESULT_STATISTICS_PATH

#!/bin/sh
STRESS_APP_NAME=`cat tmp.txt`

RAPORT_NAME="./raport_$STRESS_APP_NAME.xlsx"

sudo rm tmp.txt

sudo npm run test:linux_before --prefix $CYPRESS_PATH 

sudo rm -rf $RESULT_PATH

slave_count="$2"

case $slave_count in
"0")
    slave=""
    ;;
"1")
    slave=-R10.0.1.6
    ;;

"2")
    slave=-R10.0.1.6,10.0.1.7
    ;;

"3")
    slave=-R10.0.1.6,10.0.1.7,10.0.1.8
    ;;

*)
    slave=-R10.0.1.6,10.0.1.7,10.0.1.8
    ;;
esac

sudo bash $JMETER_PATH -n -X -t $file $slave -l $RESULT_PATH/tmp.jtl -e -o $RESULT_PATH

sudo npm run test:linux_after  --prefix $CYPRESS_PATH

sudo cat $JSON_RAPORT_PATH

sudo python3 conv.py $file $JSON_RAPORT_PATH $RAPORT_NAME

#todo after all cp to new folder (date name)
#todo the amount of space used by the recordings
# env CYPRESS_xxx