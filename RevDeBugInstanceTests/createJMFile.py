import sys
import re
import json
import os
sys.path.append("/app")
import operationOnConfigPython

def addCookie(json_):
    return f''' <elementProp name="{json_["name"]}" elementType="Cookie" testname="{json_["name"]}">
<stringProp name="Cookie.value">{json_["value"]}</stringProp>
<stringProp name="Cookie.domain">{json_["domain"]}</stringProp>
<stringProp name="Cookie.path">{json_["path"]}</stringProp>
<boolProp name="Cookie.secure">{json_["secure"]}</boolProp>
<longProp name="Cookie.expires">0</longProp>
<boolProp name="Cookie.path_specified">true</boolProp>
<boolProp name="Cookie.domain_specified">true</boolProp>
</elementProp> '''

def addCookies(jsonList_, model):
    result=''
    for x in jsonList_:
        result=result+addCookie(x)
    return str(model).replace("COOKIES_",result )


def getModel(FILE):
    with open(FILE) as f:
        f = [line.rstrip() for line in f]
    f=str(f)[2:]
    f=str(f)[:-2]

    f=str(f).replace("\\n","")
    f=str(f).replace("', '","")
    return f



def createTestEndpoint(endpoint,PROTOCOL_):
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
            <boolProp name="HTTPSampler.follow_redirects">false</boolProp>
            <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
            <boolProp name="HTTPSampler.use_keepalive">false</boolProp>
            <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
            <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
            <stringProp name="HTTPSampler.connect_timeout">600000</stringProp>
            <stringProp name="HTTPSampler.response_timeout">600000</stringProp>
            </HTTPSamplerProxy>
          <hashTree>
              <ConstantTimer guiclass="ConstantTimerGui" testclass="ConstantTimer" testname="Constant Timer" enabled="true">
                <stringProp name="ConstantTimer.delay">0</stringProp>
              </ConstantTimer>
              <hashTree/>
            </hashTree>'''


def createEndpoints(model,idTest, idMod,PROTOCOL_):
    endpointList=operationOnConfigPython.getEndpoints(idTest, idMod)
    string=''
    for x in endpointList:
        string=f'{string}{createTestEndpoint(str(x["name"]),PROTOCOL_)}'
    model=str(model).replace("ERRORS_",string )
    return model

def createDelay(model,DELAY):
    string =f'<stringProp name="ConstantTimer.delay">{DELAY}</stringProp>'
    z=model.split('<stringProp name="ConstantTimer.delay">')
    z=z[1].split('</stringProp>')[0]
    search='<stringProp name="ConstantTimer.delay">'+z+'</stringProp>'
    return str(model).replace(search, string)
    

def createHeader(idTest,idMod,model):
    TEST_TIME=operationOnConfigPython.getTestTime(idTest,idMod)
    PORT=''
    HOST=str(operationOnConfigPython.getRDBHost(idTest, idMod))
    THREAD_COUNT=str(operationOnConfigPython.getThCount(idTest, idMod))
    test_time_new='<stringProp name="ThreadGroup.duration">'+TEST_TIME+'</stringProp>'
    port_new='<stringProp name="Argument.value">'+PORT+'</stringProp>'
    host_new='<stringProp name="Argument.value">'+HOST+'</stringProp>'
    th_new=f'<stringProp name="ThreadGroup.num_threads">{THREAD_COUNT}</stringProp>'
    f=model
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
    return b

def saveFile(model):
    FILE_RESULT=os.getenv('TEST_FILE_RDB')
    f = open(FILE_RESULT, "w")
    f.write(model)
    f.close()

def create(jsonList_, idTest,idMod, DELAY):
    FILE=os.getenv('MODEL_TEST_FILE_RDB')
    PROTOCOL_= operationOnConfigPython.getRdbProtocol(idTest, idMod)
    model=getModel(FILE)
    model=createEndpoints(model,idTest, idMod,PROTOCOL_)
    model=addCookies(jsonList_, model)
    model=createDelay(model,DELAY)
    model=createHeader(idTest,idMod,model)
    saveFile(model)
