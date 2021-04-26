from openpyxl import Workbook
from openpyxl import load_workbook
import json
import os
import sys
import re

JSON_RAPORT_PATH=sys.argv[2]


with open(JSON_RAPORT_PATH) as f:
    json_dict = json.load(f)

filename_raport=sys.argv[3]


infile = r"./jmeter.log"

with open(infile) as f:
    f = f.readlines()

list_result=[]
for line in f: 
    x = re.search("summary = .* Avg", line)
    if x:
        tmp =x.group(0).split("=")
        tmp[2]=tmp[2][:-3]
        list_result.append(tmp[2])

data_name=sys.argv[1].split("/")
data_name=data_name[len(data_name)-1].split("_")


if os.path.exists(filename_raport):
    workbook = load_workbook(filename=filename_raport)
    sheet = workbook.active
else:
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = "Recordings"
    sheet["B1"] = "Trace Span"
    sheet["C1"] = "JM Count"
    sheet["D1"] = "Calls/s avg" 
    sheet["E1"] = "received kb/s"
    sheet["F1"] = "sent  kb/s"
    sheet["G1"] = "Response AVG /s"
    sheet["H1"] = "Language"
    sheet["I1"] = "Endpoint type"
    sheet["J1"] = "Code length"
    sheet["K1"] = "Applicaation name"
    sheet["L1"] = "Threads count"
    sheet["M1"] = "Repeat calls"
    sheet["N1"] = "Time"
    sheet["O1"] = "Endpoints"
    sheet.column_dimensions['A'].width =13
    sheet.column_dimensions['B'].width =10
    sheet.column_dimensions['C'].width =10
    sheet.column_dimensions['D'].width =10
    sheet.column_dimensions['E'].width =15
    sheet.column_dimensions['F'].width =10
    sheet.column_dimensions['G'].width =15
    sheet.column_dimensions['H'].width =7
    sheet.column_dimensions['I'].width =7
    sheet.column_dimensions['J'].width =7
    sheet.column_dimensions['K'].width =15
    sheet.column_dimensions['L'].width =15
    sheet.column_dimensions['M'].width =5
    sheet.column_dimensions['N'].width =5
    sheet.column_dimensions['O'].width =15



sheet.insert_rows(idx=2)

sheet["A2"] = json_dict["Recordings"]
sheet["B2"] = json_dict["Trace_Span"]
sheet["C2"] = json_dict["TotalJmeter"]["sampleCount"]
sheet["D2"]=list_result[len(list_result)-1]
sheet["E2"] = json_dict["TotalJmeter"]["receivedKBytesPerSec"]
sheet["F2"] = json_dict["TotalJmeter"]["sentKBytesPerSec"]
sheet["G2"] = json_dict["TotalJmeter"]["meanResTime"]
sheet["H2"] = data_name[0]
sheet["I2"] = data_name[2]
sheet["J2"] = data_name[3]
sheet["K2"] = data_name[7][:-4]
sheet["L2"] = data_name[4]
sheet["M2"] = data_name[5]
sheet["N2"] = data_name[6]
sheet["O2"] = data_name[1].replace("-"," /")


workbook.save(filename=filename_raport)
