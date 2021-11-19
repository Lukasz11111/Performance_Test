import argparse
import json
import datetime

import operationOnConfigPython

JSON_CONFIG="TestsConfig/Configuration.json"

parser = argparse.ArgumentParser(description='Get config')


parser.add_argument('-getModeLen',  nargs='?')
parser.add_argument('-getTestDelay',  nargs='?')
parser.add_argument('-getRDBHost',  nargs='?')
parser.add_argument('-getTestProportion',  nargs='?')
parser.add_argument('-ifTestIsActive',  nargs='?')
parser.add_argument('-getCountOfAllTest',  nargs='?')
parser.add_argument('-approximateTime',  nargs='?')
parser.add_argument('-getTestsLen',  nargs='?')


argsP=parser.parse_args().__dict__

filtered = {k: v for k, v in argsP.items() if v is not None}
argsP.clear()
argsP.update(filtered)



def getResult(argsP):
    for key, val in argsP.items():
        result = {
        'getRDBHost': lambda x: operationOnConfigPython.getRDBHost(x),
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


