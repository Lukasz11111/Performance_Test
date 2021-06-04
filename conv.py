from openpyxl import Workbook
from openpyxl import load_workbook
import json
import os
import sys
import re
from openpyxl.styles import PatternFill, colors
JSON_RAPORT_PATH=sys.argv[2]
JSON_CONFIG_PATH=sys.argv[4]+"/.config"
JSON_RDB_INFO=sys.argv[5]

def getMode(x):
    return {
        '1': "rdb and apm",
        '2': "apm",
        '3': "none",
        '4': "rdb"
    }[x]

def getColor(x):
    return {
        'rdb and apm': "ffdbd9",
        'apm': "00CCFFFF",
        'none': "00FFFFCC",
        'rdb': "00C0C0C0"
    }[x]

def createSheet(sheet):
    sheet["A1"] = "RevDeBug spec"
    sheet["B1"] = "CPU: "
    sheet["C1"] = rdb_info['cpu']
    sheet["D1"] = "RAM: " 
    sheet["E1"] =  rdb_info['ram']
    sheet["F1"] = "Size: "
    sheet["G1"] =  rdb_info['size']

    sheet["A2"] = "Application spec"
    sheet["B2"] = "CPU: "
    sheet["C2"] = json_config['cpu']
    sheet["D2"] = "RAM: " 
    sheet["E2"] =  json_config['ram']
    sheet["F2"] = "Size: "
    sheet["G2"] =  json_config['size']

    sheet["A3"] = "Application spec"
    sheet["B3"] = json_config['application_name']
    sheet["C3"] = "Git link"
    sheet["D3"] = json_config['git_link'] 
    sheet["E3"] = "RevDeBug server"
    sheet["F3"] = json_config['server_rdb']
    sheet["G3"] = "Language"
    sheet["H3"] = json_config['language']

    sheet["A5"] = "Recordings"
    sheet["B5"] = "Trace Span"
    sheet["C5"] = "JM Count"
    sheet["D5"] = "Calls/s avg" 
    sheet["E5"] = "sent  kb/s"
    sheet["F5"] = "Response AVG /s"
    sheet["G5"] = "Code length"
    sheet["H5"] = "Err proportion"
    sheet["I5"] = "RDB/APM"
    sheet["J5"] = "Delay"
    sheet.column_dimensions['A'].width =13
    sheet.column_dimensions['B'].width =10
    sheet.column_dimensions['C'].width =10
    sheet.column_dimensions['D'].width =10
    sheet.column_dimensions['E'].width =10
    sheet.column_dimensions['F'].width =15
    sheet.column_dimensions['G'].width =15
    sheet.column_dimensions['H'].width =15
    sheet.column_dimensions['I'].width =20



with open(JSON_RAPORT_PATH) as f:
    json_dict = json.load(f)

with open(JSON_CONFIG_PATH) as f:
    json_config = json.load(f)

with open(JSON_RDB_INFO) as f:
    rdb_info = json.load(f)

filename_raport=sys.argv[3]

sheet_name=json_config['application_name'] 

infile = r"test/path/jmeter.log"

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





sheet.insert_rows(idx=6)

def style(sheet):
    color = str(getColor(getMode(str(sys.argv[7])) ))
    print(color)
    sheet["A6"].fill = PatternFill(fgColor=color, fill_type = "solid")
    sheet["B6"].fill = PatternFill(fgColor=color, fill_type = "solid")
    sheet["C6"].fill = PatternFill(fgColor=color, fill_type = "solid")
    sheet["D6"].fill = PatternFill(fgColor=color, fill_type = "solid")
    sheet["E6"].fill = PatternFill(fgColor=color, fill_type = "solid")
    sheet["F6"].fill = PatternFill(fgColor=color, fill_type = "solid")
    sheet["G6"].fill = PatternFill(fgColor=color, fill_type = "solid")
    sheet["H6"].fill = PatternFill(fgColor=color, fill_type = "solid")
    sheet["I6"].fill = PatternFill(fgColor=color, fill_type = "solid")
    sheet["J6"].fill = PatternFill(fgColor=color, fill_type = "solid")



style(sheet)

sheet["A6"] = json_dict["Recordings"]
sheet["B6"] = json_dict["Trace_Span"]
sheet["C6"] = json_dict["TotalJmeter"]["sampleCount"]
sheet["D6"]=list_result[len(list_result)-1]
sheet["E6"] = json_dict["TotalJmeter"]["sentKBytesPerSec"]
sheet["F6"] = json_dict["TotalJmeter"]["meanResTime"]
sheet["G6"] = data_name[3].replace(".jmx","")
sheet["H6"] = data_name[2].replace("-"," /")
sheet["I6"] = getMode(str(sys.argv[7])) 
sheet["J6"] = sys.argv[6]

workbook.save(filename=filename_raport)
