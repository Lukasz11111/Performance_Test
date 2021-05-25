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


string1 ='<stringProp name="RandomTimer.range">'+DELAY+'</stringProp>'
string2 ='<stringProp name="ConstantTimer.delay">'+DELAY+'</stringProp>'


##TESTS must have same delay time!!!!!!!!!!!! this find first delay and replace all this delay
z= f.split('<stringProp name="RandomTimer.range">')
z=z[1].split('</stringProp>')[0]
search_one='<stringProp name="RandomTimer.range">'+z+'</stringProp>'

z= f.split('<stringProp name="ConstantTimer.delay">')
z=z[1].split('</stringProp>')[0]
search_two='<stringProp name="ConstantTimer.delay">'+z+'</stringProp>'


x =str(f).replace(search_one, string1)
x =str(x).replace(search_two, string2)


f = open(FILE, "w")
f.write(x)
f.close()