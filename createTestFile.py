
import sys
import re
import json
import os
import random


FILE=os.getenv('MODEL_TEST_FILE') 
JSON_CONFIG=os.getenv('JSON_CONFIG')

with open(JSON_CONFIG) as f:
    json_dict = json.load(f)

PROPORTION=json_dict["proportion"]

TEST_TIME=json_dict["TestTime"]
THREAD_COUNT=json_dict["threadCount"]
CALL_S=int(json_dict["callPerS"])*100
IP_CHANGE=json_dict["ip"]
PORT_CHANGE=json_dict["port"]

CON_TIM=str(json_dict["connect_timeou"])
RES_TIM=str(json_dict["response_timeout"])

with open(FILE) as f:
    f = [line.rstrip() for line in f]
f=str(f)[2:]
f=str(f)[:-2]

f=str(f).replace("\\n","")
f=str(f).replace("', '","")

f=str(f).replace("_THREAD_COUNT_",str(THREAD_COUNT))
f=str(f).replace("_CALL_S",str(CALL_S))
f=str(f).replace("_TEST_TIME_",str(TEST_TIME))

f=str(f).replace("IP_CHANGE",str(IP_CHANGE))
f=str(f).replace("PORT_CHANGE",str(PORT_CHANGE))




def createTestString(endpoint, conTim,resTim):
    return """         
            <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="Test" enabled="true">
            <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" enabled="true">
              <collectionProp name="Arguments.arguments"/>
            </elementProp>
            <stringProp name="HTTPSampler.domain">${BASE_URL_1}</stringProp>
            <stringProp name="HTTPSampler.port">${PORT_}</stringProp>
            <stringProp name="HTTPSampler.protocol">http</stringProp>
            <stringProp name="HTTPSampler.contentEncoding"></stringProp>
            <stringProp name="HTTPSampler.path">"""+endpoint+"""</stringProp>
            <stringProp name="HTTPSampler.method">GET</stringProp>
            <boolProp name="HTTPSampler.follow_redirects">false</boolProp>
            <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
            <boolProp name="HTTPSampler.use_keepalive">false</boolProp>
            <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
            <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
            <stringProp name="HTTPSampler.implementation">HttpClient4</stringProp>
            <stringProp name="HTTPSampler.connect_timeout">"""+conTim+"""</stringProp>
            <stringProp name="HTTPSampler.response_timeout">"""+resTim+"""</stringProp>
          </HTTPSamplerProxy>
          <hashTree/>
"""


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

def getEndpoint(status):
    result=[]
    for x in json_dict["endpoints"]:
        if x.get("error")==status:
            result.append(x)
    return result




for x in range(0,lenProp):
  if error_count>0:
    errEndpoint=random.choice(getEndpoint(True)).get('name')
    string=f'{string}{createTestString(str(errEndpoint),CON_TIM,RES_TIM)}'
  if success_count>0:
    sucEndpoint=random.choice(getEndpoint(False)).get('name')
    string=f'{string}{createTestString(str(sucEndpoint),CON_TIM,RES_TIM)}'
  error_count=error_count-1
  success_count=success_count-1


z =str(f).replace("_ENDPOINTS_",string )


f = open("./TestJM/result.jmx", "w")
f.write(z)
f.close()

