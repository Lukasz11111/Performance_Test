from openpyxl import Workbook
from openpyxl import load_workbook
import json
import os
import sys
import re

JSON_RAPORT_PATH=sys.argv[2]
JSON_CONFIG_PATH=sys.argv[4]+"/.config"


def createSheet(sheet):
    sheet["A1"] = "Application in RevDeBug"
    sheet["B1"] = json_config['application_name']
    sheet["C1"] = "Git link"
    sheet["D1"] = json_config['git_link'] 
    sheet["E1"] = "RevDeBug server"
    sheet["F1"] = json_config['server_rdb']
    sheet["G1"] = "Language"
    sheet["H1"] = json_config['language']

    sheet["A3"] = "Recordings"
    sheet["B3"] = "Trace Span"
    sheet["C3"] = "JM Count"
    sheet["D3"] = "Calls/s avg" 
    sheet["E3"] = "sent  kb/s"
    sheet["F3"] = "Response AVG /s"
    sheet["G3"] = "Endpoint type"
    sheet["H3"] = "Code length"
    sheet["I3"] = "Threads count"
    sheet["J3"] = "Repeat calls"
    sheet["K3"] = "Time"
    sheet["L3"] = "Endpoints"
    sheet.column_dimensions['A'].width =13
    sheet.column_dimensions['B'].width =10
    sheet.column_dimensions['C'].width =10
    sheet.column_dimensions['D'].width =10
    sheet.column_dimensions['E'].width =10
    sheet.column_dimensions['F'].width =15
    sheet.column_dimensions['G'].width =7
    sheet.column_dimensions['H'].width =7
    sheet.column_dimensions['I'].width =7
    sheet.column_dimensions['J'].width =15
    sheet.column_dimensions['K'].width =5
    sheet.column_dimensions['L'].width =5
    sheet.column_dimensions['M'].width =15


with open(JSON_RAPORT_PATH) as f:
    json_dict = json.load(f)

with open(JSON_CONFIG_PATH) as f:
    json_config = json.load(f)

filename_raport=sys.argv[3]

sheet_name=json_config['application_name'] 

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
    if not sheet_name in workbook.sheetnames:
        workbook.create_sheet(sheet_name)
        sheet_ac = workbook.get_sheet_by_name(sheet_name)
        workbook.active=sheet_ac
        sheet = workbook.active
        createSheet(sheet)
    else:
        sheet_ac = workbook.get_sheet_by_name(sheet_name)
        workbook.active=sheet_ac
        sheet = workbook.active
    
else:
    workbook = Workbook()
    workbook.create_sheet(sheet_name)
    sheet_ac = workbook.get_sheet_by_name(sheet_name)
    workbook.active=sheet_ac
    sheet = workbook.active
    createSheet(sheet)





sheet.insert_rows(idx=4)

sheet["A4"] = json_dict["Recordings"]
sheet["B4"] = json_dict["Trace_Span"]
sheet["C4"] = json_dict["TotalJmeter"]["sampleCount"]
sheet["D4"]=list_result[len(list_result)-1]
sheet["E4"] = json_dict["TotalJmeter"]["sentKBytesPerSec"]
sheet["F4"] = json_dict["TotalJmeter"]["meanResTime"]
sheet["G4"] = data_name[0]
sheet["G4"] = data_name[2]
sheet["H4"] = data_name[3]
sheet["I4"] = data_name[4]
sheet["J4"] = data_name[5]
sheet["K4"] = data_name[6]
sheet["L4"] = data_name[1].replace("-"," /")


workbook.save(filename=filename_raport)
