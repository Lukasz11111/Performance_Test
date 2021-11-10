import sys
import re
FILE=sys.argv[1]
DELAY=sys.argv[2]
with open(FILE) as f:
    f = f.readlines()
f=str(f)[2:]
f=str(f)[:-2]

f=str(f).replace("\\n","")
f=str(f).replace("', '","")


string =f'<stringProp name="ConstantTimer.delay">{DELAY}</stringProp>'

z= f.split('<stringProp name="ConstantTimer.delay">')
z=z[1].split('</stringProp>')[0]
search='<stringProp name="ConstantTimer.delay">'+z+'</stringProp>'

x =str(x).replace(search, string)


f = open(FILE, "w")
f.write(x)
f.close()