
slave="$1"

LOG_PATH=testJM/path/jmeter.log
RESULT_PATH=testJM/result

rm -rf $RESULT_PATH
mkdir $RESULT_PATH

rm -rf $LOG_PATH
touch $LOG_PATH

jmeter -n -Jserver.rmi.ssl.disable=true  $slave -t /testJMStart/test.jmx  -l $RESULT_PATH/tmp.jtl -e -o $RESULT_PATH -j $LOG_PATH

