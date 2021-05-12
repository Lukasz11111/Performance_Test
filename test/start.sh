
slave="$1"
RESULT_PATH=/testJM/result

rm -rf $RESULT_PATH
mkdir $RESULT_PATH



jmeter -n -Jserver.rmi.ssl.disable=true  $slave -t /testJM/test.jmx  -l $RESULT_PATH/tmp.jtl -e -o $RESULT_PATH

