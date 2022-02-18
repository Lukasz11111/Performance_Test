import argparse
import json
import datetime
import os

import operationOnConfigPython

parser = argparse.ArgumentParser(description='Get config')

parser.add_argument('-mod')

parser.add_argument('-RDBrestartAfterSingleRun',  nargs='?')
parser.add_argument('-initServerAll',  nargs='?')
parser.add_argument('-initServerTest',  nargs='?')
parser.add_argument('-initServerMod',  nargs='?')
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
parser.add_argument('-ifRaportGen',  nargs='?')
parser.add_argument('-getSSLActive',  nargs='?')
parser.add_argument('-getKeycloakActive',  nargs='?')
parser.add_argument('-getDockerRDBPath',  nargs='?')
parser.add_argument('-clearRDBAfterMod',  nargs='?')
parser.add_argument('-clearRDBAfterTest',  nargs='?')
parser.add_argument('-clearRDBAfterAll',  nargs='?')
parser.add_argument('-initData',  nargs='?')
parser.add_argument('-getKeyPathApp',  nargs='?')
parser.add_argument('-getAppPath',  nargs='?')
parser.add_argument('-getAppHost',  nargs='?')
parser.add_argument('-getUserAppSys',  nargs='?')
parser.add_argument('-getAppDir',  nargs='?')
parser.add_argument('-rebuildAppAfterMod',  nargs='?')
parser.add_argument('-rebuildAppAfterTest',  nargs='?')
parser.add_argument('-rebuildAppAfterAll',  nargs='?')
parser.add_argument('-rebuildDataGenApp',  nargs='?')
parser.add_argument('-getAppGenDataDir',  nargs='?')

parser.add_argument('-FileTestActiv',  nargs='?')
parser.add_argument('-AppTestActiv',  nargs='?')
parser.add_argument('-typeTest',  nargs='?')

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
        'typeTest': lambda x: operationOnConfigPython.typeTest(x),
        'RDBrestartAfterSingleRun': lambda x: operationOnConfigPython.RDBrestartAfterSingleRun(x,mod),
        'getAppGenDataDir': lambda x: operationOnConfigPython.getAppGenDataDir(x,mod),
        'rebuildAppAfterMod': lambda x: operationOnConfigPython.rebuildAppAfterMod(),
        'rebuildAppAfterTest': lambda x: operationOnConfigPython.rebuildAppAfterTest(),
        'rebuildAppAfterAll': lambda x: operationOnConfigPython.rebuildAppAfterAll(),
        'rebuildDataGenApp': lambda x: operationOnConfigPython.rebuildDataGenApp(x,mod),
        'getAppDir': lambda x: operationOnConfigPython.getAppDir(x,mod),
        'getUserAppSys': lambda x: operationOnConfigPython.getUserAppSys(x,mod),
        'getAppHost': lambda x: operationOnConfigPython.getAppHost(x,mod),
        'getAppPath': lambda x: operationOnConfigPython.getAppPath(x,mod),
        'getKeyPathApp': lambda x: operationOnConfigPython.getKeyPathApp(x,mod),
        'initData': lambda x: operationOnConfigPython.initData(x,mod),
        'initServerAll': lambda x: operationOnConfigPython.initServerAll(x,mod),
        'initServerTest': lambda x: operationOnConfigPython.initServerTest(x,mod),
        'initServerMod': lambda x: operationOnConfigPython.initServerMod(x,mod),
        'getDockerRDBPath': lambda x: operationOnConfigPython.getDockerRDBPath(x,mod),
        'clearRDBAfterMod': lambda x: operationOnConfigPython.clearRDBAfterMod(),
        'clearRDBAfterTest': lambda x: operationOnConfigPython.clearRDBAfterTest(),
        'clearRDBAfterAll': lambda x: operationOnConfigPython.clearRDBAfterAll(),
        'getKeycloakActive': lambda x: operationOnConfigPython.getKeycloakActiveBash(x,mod),
        'getSSLActive': lambda x: operationOnConfigPython.getSSLActive(x,mod),
        'ifRaportGen': lambda x: operationOnConfigPython.ifRaportGen(x,mod),
        'slaveingleTest': lambda x: operationOnConfigPython.slaveingleTest(),
        'customSingleTest': lambda x: operationOnConfigPython.customSingleTest(),
        'getRdbDBSysUser': lambda x: operationOnConfigPython.getRdbDBSysUser(x,mod),
        'FileTestActiv': lambda x: operationOnConfigPython.FileTestActiv(),
        'RDBTestActiv': lambda x: operationOnConfigPython.RDBTestActiv(),
        'AppTestActiv': lambda x: operationOnConfigPython.AppTestActiv(),
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


