
import sys
import re
import json
FILE=sys.argv[1]
PATH_CONF=sys.argv[2]

with open(PATH_CONF) as f:
    json_dict = json.load(f)


Error=json_dict["err"]
Success=json_dict["success"]
PROTOCOL_= json_dict["protocol"]

#100=100% succes, 0= 100% error, 50=50% succes itd.
PROPORTION=int(sys.argv[3])



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
            <UniformRandomTimer guiclass="UniformRandomTimerGui" testclass="UniformRandomTimer" testname="Uniform Random Timer" enabled="true">
              <stringProp name="RandomTimer.range">0</stringProp>
              <stringProp name="ConstantTimer.delay">0</stringProp>
              <stringProp name="TestPlan.comments">Recorded time was 0 milliseconds</stringProp>
            </UniformRandomTimer>
            <hashTree/>
          </hashTree> '''

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
            <UniformRandomTimer guiclass="UniformRandomTimerGui" testclass="UniformRandomTimer" testname="Uniform Random Timer" enabled="true">
              <stringProp name="RandomTimer.range">0</stringProp>
              <stringProp name="ConstantTimer.delay">0</stringProp>
              <stringProp name="TestPlan.comments">Recorded time was 0 milliseconds</stringProp>
            </UniformRandomTimer>
            <hashTree/>
          </hashTree> '''


string=''
error_count=100-PROPORTION
success_count=PROPORTION


if PROPORTION ==100 or  PROPORTION ==0:
  if PROPORTION==100:
    string=SUCCESSES_CALL_STR
  else:
    string=ERROR_CALL_STR

if PROPORTION ==50:
  string=SUCCESSES_CALL_STR+ERROR_CALL_STR

if PROPORTION == 90 or  PROPORTION == 80 or PROPORTION == 70 or  PROPORTION == 60 or  PROPORTION == 40 or PROPORTION == 30 or  PROPORTION == 20 or  PROPORTION == 10:
  now_err=True
  for x in range(0,10):
    if now_err:
      if error_count>0:
        string=string+ERROR_CALL_STR
        error_count=error_count-10
        if(success_count!=0):
          now_err=False
    elif not now_err:
      if success_count>0:
        string=string+SUCCESSES_CALL_STR
        success_count=success_count-10
        if(error_count!=0):
          now_err=True

if PROPORTION == 95 or  PROPORTION == 85 or PROPORTION == 75 or  PROPORTION == 65 or PROPORTION == 55 or  PROPORTION == 45 or PROPORTION == 35 or  PROPORTION == 25 or  PROPORTION == 15 or  PROPORTION == 5:
  now_err=True
  for x in range(0,20):
    if now_err:
      if error_count>0:
        string=string+ERROR_CALL_STR
        error_count=error_count-5
        if(success_count!=0):
          now_err=False
    elif not now_err:
      if success_count>0:
        string=string+SUCCESSES_CALL_STR
        success_count=success_count-5
        if(error_count!=0):
          now_err=True

z =str(f).replace("ERRORS_",string )


f = open("./tmp.jmx", "w")
f.write(z)
f.close()