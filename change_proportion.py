
import sys
import re
import json
FILE=sys.argv[1]


with open("TestsConfig/Configuration.json") as f:
    json_dict = json.load(f)


# Error=json_dict["err"]
# Success=json_dict["success"]
# PROTOCOL_= json_dict["protocol"]

Error="json_dict[err]"
Success="json_dict[success]"
PROTOCOL_= "json_dict[protocol]"




#100=100% succes, 0= 100% error, 50=50% succes itd.
PROPORTION=int(sys.argv[2])



with open(FILE) as f:
    f = f.readlines()
f=str(f)[2:]
f=str(f)[:-2]

f=str(f).replace("\\n","")
f=str(f).replace("', '","")



ERROR_CALL_STR=''' <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="'''+Error+'''" enabled="true">
            <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" enabled="true">
              <collectionProp name="Arguments.arguments"/>
            </elementProp>
            <stringProp name="HTTPSampler.domain">${BASE_URL_1}</stringProp>
            <stringProp name="HTTPSampler.port">${PORT}</stringProp>
            <stringProp name="HTTPSampler.protocol">'''+PROTOCOL_+'''</stringProp>
            <stringProp name="HTTPSampler.contentEncoding"></stringProp>
            <stringProp name="HTTPSampler.path">'''+Error+'''</stringProp>
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

SUCCESSES_CALL_STR=''' <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="'''+Success+'''" enabled="true">
            <elementProp name="HTTPsampler.Arguments" elementType="Arguments" guiclass="HTTPArgumentsPanel" testclass="Arguments" enabled="true">
              <collectionProp name="Arguments.arguments"/>
            </elementProp>
            <stringProp name="HTTPSampler.domain">${BASE_URL_1}</stringProp>
            <stringProp name="HTTPSampler.port">${PORT}</stringProp>
            <stringProp name="HTTPSampler.protocol">'''+PROTOCOL_+'''</stringProp>
            <stringProp name="HTTPSampler.contentEncoding"></stringProp>
            <stringProp name="HTTPSampler.path">'''+Success+'''</stringProp>
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
    string=f'{string}{ERROR_CALL_STR}'
  if success_count>0:
    string=f'{string}{SUCCESSES_CALL_STR}'
  error_count=error_count-1
  success_count=success_count-1


z =str(f).replace("ERRORS_",string )


f = open("./tmp.jmx", "w")
f.write(z)
f.close()