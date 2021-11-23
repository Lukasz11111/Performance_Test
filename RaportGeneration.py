from openpyxl import Workbook
from openpyxl import load_workbook
import json
import os
import sys
import re
from openpyxl.styles import PatternFill, colors, Alignment
import ast
import pickle
import copy



def getCallsPerSecond():
    infile = os.getenv("LOG_PATH")
    with open(infile) as f:
        f = f.readlines()
    calls=0
    list_result=[]
    for line in f: 
        x = re.search("summary = .* Avg", line)
        if x:
            tmp =x.group(0).split("=")
            tmp[2]=tmp[2][:-3]
            list_result.append(tmp[2])
            calls=list_result[len(list_result)-1].split("/s")[0]
    return calls

