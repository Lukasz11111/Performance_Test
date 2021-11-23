import argparse
import json
import datetime
import os

import operationOnConfigPython

parser = argparse.ArgumentParser(description='Get config')

parser.add_argument('-mod')
parser.add_argument('-singleTestsActive',  nargs='?')
parser.add_argument('-getDeduplication',  nargs='?')
parser.add_argument('-getModeLen',  nargs='?')
parser.add_argument('-getTestDelay',  nargs='?')
parser.add_argument('-getRDBHost',  nargs='?')
parser.add_argument('-getTestProportion',  nargs='?')
parser.add_argument('-ifTestIsActive',  nargs='?')
parser.add_argument('-getCountOfAllTest',  nargs='?')
parser.add_argument('-approximateTime',  nargs='?')
parser.add_argument('-getTestsLen',  nargs='?')
parser.add_argument('-getSlave',  nargs='?')
parser.add_argument('-getRDBKey',  nargs='?')
parser.add_argument('-getPgContainerName',  nargs='?')
parser.add_argument('-getRdbDBSysUser',  nargs='?')
parser.add_argument('-customSingleTest',  nargs='?')
parser.add_argument('-slaveingleTest',  nargs='?')


argsP=parser.parse_args().__dict__

filtered = {k: v for k, v in argsP.items() if v is not None}
argsP.clear()
argsP.update(filtered)

mod=''
if 'mod' in argsP:
    mod = argsP.pop("mod")

def getResult(argsP):
    for key, val in argsP.items():
        result = {  
        'slaveingleTest': lambda x: operationOnConfigPython.slaveingleTest(),
        'customSingleTest': lambda x: operationOnConfigPython.customSingleTest(),
        'getRdbDBSysUser': lambda x: operationOnConfigPython.getRdbDBSysUser(x,mod),
        'singleTestsActive': lambda x: operationOnConfigPython.singleTestsActive(),
        'getPgContainerName': lambda x: operationOnConfigPython.getPgContainerName(x,mod),
        'getRDBKey': lambda x: operationOnConfigPython.getRdbKey(x,mod),
        'getDeduplication': lambda x: operationOnConfigPython.getDeduplication(x,mod),
        'getSlave': lambda x: operationOnConfigPython.getSlave(x,mod),
        'getRDBHost': lambda x: operationOnConfigPython.getRDBHost(x,mod),
        'getModeLen': lambda x: operationOnConfigPython.getModeLen(x),
        'getTestDelay': lambda x: operationOnConfigPython.getTestDelay(x),
        'getTestProportion': lambda x: operationOnConfigPython.getTestProportion(x),
        'ifTestIsActive': lambda x: operationOnConfigPython.ifTestIsActive(x),
        'getTestsLen': lambda x: operationOnConfigPython.getTestsLen(),
        'getslave': lambda x: operationOnConfigPython.getslave(),
        'getCountOfAllTest': lambda x: operationOnConfigPython.getAllRun()['allRun'],
        'approximateTime': lambda x: str(datetime.timedelta(seconds=operationOnConfigPython.getAllRun()["testTime"])),
        }[key](val)
    return result

if bool(argsP):
    result=str(getResult(argsP))

    from sys import exit
    exit(result)

else:
    print("Nothing is set")
    pass


