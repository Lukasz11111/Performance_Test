#!/bin/bash
python3  createTestFile.py

jmeter -n -Jserver.rmi.ssl.disable=true -t ./TestJM/result.jmx