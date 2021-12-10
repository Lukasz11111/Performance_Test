
import sys
import re
import json
import os

FILE=os.getenv('MODEL_TEST_FILE') 

import operationOnConfigPython
import random

JSON_CONFIG=os.getenv('JSON_CONFIG')

with open(JSON_CONFIG) as f:
    json_dict = json.load(f)
idTest=int(sys.argv[2])
idMod=int(sys.argv[4])
PROTOCOL_= operationOnConfigPython.getProtocoleApp(idTest,idMod)


#100=100% succes, 0= 100% error, 50=50% succes itd.
PROPORTION=int(sys.argv[1])


with open(FILE) as f:
    f = [line.rstrip() for line in f]
f=str(f)[2:]
f=str(f)[:-2]

f=str(f).replace("\\n","")
f=str(f).replace("', '","")


def createTestString(endpoint):
  return ''' <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="'''+endpoint+'''" enabled="true">
              <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" enabled="true">
                <collectionProp name="Arguments.arguments"/>
              </elementProp>
              <stringProp name="HTTPSampler.domain">${BASE_URL_1}</stringProp>
              <stringProp name="HTTPSampler.port">${PORT}</stringProp>
              <stringProp name="HTTPSampler.protocol">'''+PROTOCOL_+'''</stringProp>
              <stringProp name="HTTPSampler.contentEncoding"></stringProp>
              <stringProp name="HTTPSampler.path">'''+endpoint+'''</stringProp>
              <stringProp name="HTTPSampler.method">GET</stringProp>
              <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
              <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
              <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
              <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
              <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
              <stringProp name="HTTPSampler.connect_timeout"></stringProp>
              <stringProp name="HTTPSampler.response_timeout"></stringProp>
            </HTTPSamplerProxy>
          <hashTree>
              <ConstantTimer guiclass="ConstantTimerGui" testclass="ConstantTimer" testname="Constant Timer" enabled="true">
                <stringProp name="ConstantTimer.delay">0</stringProp>
              </ConstantTimer>
              <hashTree/>
            </hashTree>'''



string=''
error_count=100-PROPORTION
success_count=PROPORTION


def division_(error_count,success_count):
  modList=[100, 50, 30, 25, 20, 15, 13,11,10,5,7,6,4,3,2]
  for value in modList:
    if chcekIfYouCanDivision(error_count,success_count, value):
      error_count=error_count/value
      success_count=success_count/value
  return [error_count,success_count]

def chcekIfYouCanDivision(value, value2,mod):
  if value % mod == 0 and value2 % mod == 0:
    return True
  return False

listProp= division_(error_count,success_count)
error_count=int(listProp[0])
success_count=int(listProp[1])
lenProp=0
if error_count>=success_count:
  lenProp=error_count
else:
  lenProp=success_count




for x in range(0,lenProp):
  if error_count>0:
    errEndpoint=random.choice(operationOnConfigPython.getErrorEndpoint(idTest, idMod)).get('name')
    string=f'{string}{createTestString(str(errEndpoint))}'
  if success_count>0:
    sucEndpoint=random.choice(operationOnConfigPython.getSuccesEndpoint(idTest, idMod)).get('name')
    string=f'{string}{createTestString(str(sucEndpoint))}'
  error_count=error_count-1
  success_count=success_count-1


z =str(f).replace("ERRORS_",string )

FILE_RESULT=os.getenv('TMP_TEST_FILE')

f = open(FILE_RESULT, "w")
f.write(z)
f.close()

DELAY=sys.argv[3]

with open(FILE_RESULT) as f:
    f = [line.rstrip() for line in f]

f=str(f)[2:]
f=str(f)[:-2]

f=str(f).replace("\\n","")
f=str(f).replace("', '","")


string =f'<stringProp name="ConstantTimer.delay">{DELAY}</stringProp>'

z= f.split('<stringProp name="ConstantTimer.delay">')

z=z[1].split('</stringProp>')[0]

search='<stringProp name="ConstantTimer.delay">'+z+'</stringProp>'

x =str(f).replace(search, string)


f = open(FILE_RESULT, "w")
f.write(x)
f.close()




with open(FILE_RESULT) as f:
    f = f.readlines()
f=str(f)[2:]
f=str(f)[:-2]

f=str(f).replace("\\n","")
f=str(f).replace("', '","")

TEST_TIME=operationOnConfigPython.getTestTime(idTest,idMod)
PORT=str(operationOnConfigPython.getAppPort(idTest, idMod))
HOST=str(operationOnConfigPython.getAppHost(idTest, idMod))
THREAD_COUNT=str(operationOnConfigPython.getThCount(idTest, idMod))



test_time_new='<stringProp name="ThreadGroup.duration">'+TEST_TIME+'</stringProp>'
port_new='<stringProp name="Argument.value">'+PORT+'</stringProp>'
host_new='<stringProp name="Argument.value">'+HOST+'</stringProp>'
th_new=f'<stringProp name="ThreadGroup.num_threads">{THREAD_COUNT}</stringProp>'




z= f.split('<elementProp name="PORT" elementType="Argument">')
z=z[1].split('</elementProp>')[0].split('<stringProp name=')[2].split('"Argument.value">')[1].replace('</stringProp>', '').replace(' ', '')
port_old ='<stringProp name="Argument.value">'+z+'</stringProp>'

f =str(f).replace(port_old, port_new)


z= f.split('<elementProp name="BASE_URL_1" elementType="Argument">')
z=z[1].split('</elementProp>')[0].split('<stringProp name=')[2].split('"Argument.value">')[1].replace('</stringProp>', '').replace(' ', '')
host_old ='<stringProp name="Argument.value">'+z+'</stringProp>'

x =str(f).replace(host_old, host_new)


z= f.split('<stringProp name="ThreadGroup.duration">')
z=z[1].split('</stringProp>')[0].replace(' ', '')
test_time_old =' <stringProp name="ThreadGroup.duration">'+z+'</stringProp>'

b =str(x).replace(test_time_old, test_time_new)

z=f.split('<stringProp name="ThreadGroup.num_threads">')
z=z[1].split('</stringProp>')[0].replace(' ', '')
th_old ='<stringProp name="ThreadGroup.num_threads">'+z+'</stringProp>'

b=str(b).replace(th_old, th_new)

f = open(FILE_RESULT, "w")
f.write(b)
f.close()