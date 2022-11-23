#!/bin/bash
python3  createTestFile.py

rm -rf ./logJm.log
# rm -rf ./TestJM/logs

# mkdir ./TestJM/logs

jmeter -n -Jserver.rmi.ssl.disable=true -t ./TestJM/result.jmx
# jmeter -n -Jserver.rmi.ssl.disable=true -t ./TestJM/result.jmx  -l  logJm.log -e -o  ./TestJM/logs

date=$(date '+%m%d%H%M%S')

# tar -zcvf ./TestJM/result_$date.tar.gz ./TestJM/logs

