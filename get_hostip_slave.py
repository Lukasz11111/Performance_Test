import re
import sys
import os


slave_count=int(sys.argv[1])
f = open("iphost.txt", "r").read()
f =f.split("/")
ip='-R'
ite=0
if not slave_count==0:
    for x in f[:]:
        if not "slave" in str(x):
            f.remove(x)
        else:
            if  int(sys.argv[1]) > ite:
                i=f.index(x)
                x = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", x)
                ip=ip+x[0]+','
            ite=ite+1
    exit(ip[:-1]) 
else:
    exit(ip[:-2]) 


