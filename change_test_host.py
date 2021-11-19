import sys
import re
import json
FILE=sys.argv[1]
HOST_PORT=sys.argv[2]

PATH_CONF=sys.argv[3]

HOST_PORT_array=HOST_PORT.split(":")



if HOST_PORT_array.__len__()==1:
    PORT='null'
else:
    PORT=HOST_PORT_array[1]

HOST=HOST_PORT_array[0]

if PORT=='null':
    PORT=''



with open(PATH_CONF) as f:
    json_dict = json.load(f)

try:
    TEST_TIME=str(int(json_dict["test_time"]))
except:
    TEST_TIME='15'






with open(FILE) as f:
    f = f.readlines()
f=str(f)[2:]
f=str(f)[:-2]

f=str(f).replace("\\n","")
f=str(f).replace("', '","")



test_time_new='<stringProp name="ThreadGroup.duration">'+TEST_TIME+'</stringProp>'
port_new='<stringProp name="Argument.value">'+PORT+'</stringProp>'
host_new='<stringProp name="Argument.value">'+HOST+'</stringProp>'

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

f = open(FILE, "w")
f.write(b)
f.close()