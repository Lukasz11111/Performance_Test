
slave="$1"
RESULT_PATH=/testJM/result

LOG_PATH=/testJM/path/jmeter.log


rm -rf $RESULT_PATH
mkdir $RESULT_PATH

rm -rf $LOG_PATH
touch $LOG_PATH

jmeter -n -Jserver.rmi.ssl.disable=true  $slave -t /testJM/test.jmx  -l $RESULT_PATH/tmp.jtl -e -o $RESULT_PATH -j $LOG_PATH

