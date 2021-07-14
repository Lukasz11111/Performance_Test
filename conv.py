from openpyxl import Workbook
from openpyxl import load_workbook
import json
import os
import sys
import re
from openpyxl.styles import PatternFill, colors, Alignment


JSON_RAPORT_PATH=sys.argv[2]
JSON_CONFIG_PATH=sys.argv[4]+"/.config"
JSON_RDB_INFO=sys.argv[5]

active_line="6"
col_nr_Recordings='A'
col_nr_How_many_rec_should='B'
col_nr_TraceSpan='C'
col_nr_JMCount='D'
col_nr_Calls='E'
col_nr_Sent='F'
col_nr_Response='G'
col_nr_Successes='H'
col_nr_Module='I'
col_nr_Delay='J'
col_nr_JmeterErr='K'

dict_Recordings={}
dict_How_many_rec_should={}
dict_TraceSpan={}
dict_JMCount={}
dict_Calls={}
dict_Sent={}
dict_Response={}
dict_Successes={}
dict_Module={}
dict_Delay={}
dict_JmeterErr={}


dict_legend={
    "Recordings":dict_Recordings,
    'How_many_rec_should':dict_How_many_rec_should,
    'TraceSpan':dict_TraceSpan,
    'JMCount':dict_JMCount,
    'Calls':dict_Calls,
    'Sent':dict_Sent,
    'Response':dict_Response,
    'Successes':dict_Successes,
    'Module':dict_Module,
    'Delay':dict_Delay,
    'JmeterErr':dict_JmeterErr
}





def style(sheet,active_line):
    color = str(getColor(getMode(str(sys.argv[7])) ))
    print(color)
    Line_legend="6"
    setStyl(sheet[col_nr_Recordings+active_line],color)
    setStyl(sheet[col_nr_TraceSpan+active_line],color)
    setStyl(sheet[col_nr_JMCount+active_line],color)
    setStyl(sheet[col_nr_Calls+active_line],color)
    setStyl(sheet[col_nr_Sent+active_line],color)
    setStyl(sheet[col_nr_Response+active_line],color)
    setStyl(sheet[col_nr_Successes+active_line],color)
    setStyl(sheet[col_nr_Module+active_line],color)
    setStyl(sheet[col_nr_Delay+active_line],color)
    setStyl(sheet[col_nr_JmeterErr+active_line],color)
    setStyl(sheet[col_nr_How_many_rec_should+active_line],color)


def setStyl(call,color):
    call.fill = PatternFill(fgColor=color, fill_type = "solid")
    


    

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
    Line_RevDeBug_spec="1"
    Line_Application_spec="2"
    Line_Application_name="3"
    Line_legend="5"

    sheet["A"+Line_RevDeBug_spec] = "RevDeBug spec"
    sheet["B"+Line_RevDeBug_spec] = "CPU: "
    sheet["C"+Line_RevDeBug_spec] = rdb_info['cpu']
    sheet["D"+Line_RevDeBug_spec] = "RAM: " 
    sheet["E"+Line_RevDeBug_spec] =  rdb_info['ram']
    sheet["F"+Line_RevDeBug_spec] = "Size: "
    sheet["G"+Line_RevDeBug_spec] =  rdb_info['size']

    sheet["A"+Line_Application_spec] = "Application spec"
    sheet["B"+Line_Application_spec] = "CPU: "
    sheet["C"+Line_Application_spec] = json_config['cpu']
    sheet["D"+Line_Application_spec] = "RAM: " 
    sheet["E"+Line_Application_spec] =  json_config['ram']
    sheet["F"+Line_Application_spec] = "Size: "
    sheet["G"+Line_Application_spec] =  json_config['size']

    sheet["A"+Line_Application_name] = "Application name"
    sheet["B"+Line_Application_name] = json_config['application_name']
    sheet["C"+Line_Application_name] = "Git link"
    sheet["D"+Line_Application_name] = json_config['git_link'] 
    sheet["E"+Line_Application_name] = "RevDeBug server"
    sheet["F"+Line_Application_name] = json_config['server_rdb']
    sheet["G"+Line_Application_name] = "Language"
    sheet["H"+Line_Application_name] = json_config['language']

    sheet[col_nr_Recordings+Line_legend] = "Recordings"
    sheet[col_nr_TraceSpan+Line_legend] = "Trace Span"
    sheet[col_nr_JMCount+Line_legend] = "JM Count"
    sheet[col_nr_Calls+Line_legend] = "Calls/s avg" 
    sheet[col_nr_Sent+Line_legend] = "Sent  kb/s"
    sheet[col_nr_Response+Line_legend] = "Response AVG /s"
    sheet[col_nr_Successes+Line_legend] = "Successes"
    sheet[col_nr_Module+Line_legend] = "RDB/APM"
    sheet[col_nr_Delay+Line_legend] = "Delay"
    sheet[col_nr_JmeterErr+Line_legend] = "Jmeter proportion"
    sheet[col_nr_How_many_rec_should+Line_legend] = "Expected number of recordings"

    sheet[col_nr_Recordings+Line_legend].alignment = Alignment(wrap_text=True)
    sheet[col_nr_TraceSpan+Line_legend].alignment = Alignment(wrap_text=True)
    sheet[col_nr_JMCount+Line_legend].alignment = Alignment(wrap_text=True)
    sheet[col_nr_Calls+Line_legend].alignment = Alignment(wrap_text=True)
    sheet[col_nr_Sent+Line_legend].alignment = Alignment(wrap_text=True)
    sheet[col_nr_Response+Line_legend].alignment = Alignment(wrap_text=True)
    sheet[col_nr_Successes+Line_legend].alignment = Alignment(wrap_text=True)
    sheet[col_nr_Module+Line_legend].alignment = Alignment(wrap_text=True)
    sheet[col_nr_Delay+Line_legend].alignment = Alignment(wrap_text=True)
    sheet[col_nr_JmeterErr+Line_legend].alignment = Alignment(wrap_text=True)
    sheet[col_nr_How_many_rec_should+Line_legend].alignment = Alignment(wrap_text=True)
    

    sheet.column_dimensions[col_nr_Recordings].width =10
    sheet.column_dimensions[col_nr_TraceSpan].width =10
    sheet.column_dimensions[col_nr_JMCount].width =10
    sheet.column_dimensions[col_nr_Calls].width =10
    sheet.column_dimensions[col_nr_Sent].width =10
    sheet.column_dimensions[col_nr_Response].width =15
    sheet.column_dimensions[col_nr_Successes].width =15
    sheet.column_dimensions[col_nr_Module].width =15
    sheet.column_dimensions[col_nr_Delay].width =15
    sheet.column_dimensions[col_nr_JmeterErr].width =15
    sheet.column_dimensions[col_nr_How_many_rec_should].width =17



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

data_name=sys.argv[1]



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

value_Recordings=str(json_dict["Recordings"])
value_Trace_Span = json_dict["Trace_Span"]
value_sampleCount= json_dict["TotalJmeter"]["sampleCount"]
value_CallsPerSec= list_result[len(list_result)-1]
value_sentKBytesPerSec= json_dict["TotalJmeter"]["sentKBytesPerSec"]
value_meanResTime= json_dict["TotalJmeter"]["meanResTime"]
value_predicted_proportion= data_name
value_real_proportion =json_dict["TotalJmeter"]["errorPct"]
value_rdb_module=getMode(str(sys.argv[7])) 
value_Delay= sys.argv[6]
if (str(sys.argv[7])=="4" or str(sys.argv[7])=="1"):
    value_How_many_rec_should='~'+str((float(value_real_proportion)/100)*value_sampleCount)
else:
    value_How_many_rec_should="0"


style(sheet, active_line)
sheet[col_nr_Recordings+active_line]  = value_Recordings
sheet[col_nr_TraceSpan+active_line]  = value_Trace_Span
sheet[col_nr_JMCount+active_line] = value_sampleCount
sheet[col_nr_Calls+active_line]=value_CallsPerSec
sheet[col_nr_Sent+active_line] = value_sentKBytesPerSec
sheet[col_nr_Response+active_line] = value_meanResTime
sheet[col_nr_Successes+active_line] =value_predicted_proportion
sheet[col_nr_Module+active_line] = value_rdb_module 
sheet[col_nr_Delay+active_line] = value_Delay
sheet[col_nr_JmeterErr+active_line]= value_real_proportion
sheet[col_nr_How_many_rec_should+active_line]= value_How_many_rec_should

workbook.save(filename=filename_raport)
