import gspread
from gspread.urls import SPREADSHEETS_API_V4_BASE_URL
from gspread_formatting import *
import sys
import operationOnConfigPython
import operationOnResult
import json
import os
idTest=sys.argv[1]
idMod=sys.argv[2]
time_=sys.argv[3]
delay=sys.argv[4]

gc = gspread.service_account(filename='./file.json')

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1BToFDEIASReYQERkGrCwgzo6TgWNNT9ySw2dWG5FHc4/edit#gid=0')

worksheet = sh.get_worksheet(0)

OrderInRow=[
    {"ID":False},
    {"TIME":False},
    {"RECORDINGS":True},
    {"RECORDING_PRECENT":True},
    {"TRACE_ERROR":True},
    {"TRACE_SUCCES":True},
    {"TRACE_PERCENT":True},
    {"TRACE":True},
    {"ALL_CALLS":True},
    {"CALLS_PER_S":True},
    {"SEND_KB_PER_S":True},
    {"AVG_RESPONSE_APP_TIME":True},
    {"PROPORION_ERROR_TO_SUCCES":True},
    {"MODULE_NAME":True},
    {"CALL_DELAY":True},
    {"RAM_RDB":True},
    {"CPU_RDB":True},
    {"DISK_SIZE_RDB":True},
    {"DISK_TYPE_RDB":True},
    {"DISK_IOPS":True},
    {"PLATFORM_RDB":True},
    {"VERSION_RDB":True},
    {"COMPILER_VERSION":True},
    {"AGENT_VERSION":True},
    {"SSL_ON_RDB":True},
    {"ENDPOINTS":True},
    {"ENDPOINT_LEN":True},
    {"MULTISERVICE":True},
    {"DB_CALLS":True},
    {"USERS_ON_RDB":True},
    {"DATA_RETENTION":True},
    

]


class CallsOption():
    type_=''
    value=''
    hide=''
    def __init__(self,type_='',value=''):
        self.type_=type_
        self.value=value



class StyleOptions():
    def __init__(self,color,bold,horizontalAlignment):
        self.color=color
        self.bold=bold
        self.horizontalAlignment=horizontalAlignment
    color=0
    bold=False
    horizontalAlignment='CENTER'



def getColor(colorValue=False):
    result = {  
    'antiquewhite': "#FAEBD7",
    'azure': "#E0EEEE",
    'bisque': "#FFE4C4",
    'darkseagreen': "#B4EEB4",
    'gray': "#A1A1A1",
    'lavenderblus': "#FFF0F5",
    'black': "#292421",
    'lightpink': "#FFB6C1",
    'mistyrose': "#FFE4E1",
    'orangered': "#8B2500",
    'plum': "#DDA0DD",
    'seashell': "#CDC5BF",
    'slategray': "#C6E2FF",
    'thistle': "#D8BFD8",
    'pink': "#FFC0CB",
    'orange': "#FFA500",
    'red': "#FFC1C1",
    'blue': "#BBFFFF",
    'green': "#98FB98",
    'yellow': "#FFEC8B",
    'white': "#FFFFFF",
    }
    import random
    if not colorValue:
        colorValue=random.choice(list(result.keys()))
    result=result[colorValue]
    return color.fromHex(result)

def setSyle(worksheet,styleOption,range_):
    fmt = cellFormat(
    backgroundColor=color(styleOption.color.red, styleOption.color.green, styleOption.color.blue),
    textFormat=textFormat(bold=styleOption.bold, foregroundColor=color(1-styleOption.color.red, 1-styleOption.color.green, 1-styleOption.color.blue)),
    horizontalAlignment=styleOption.horizontalAlignment
    )

    format_cell_range(worksheet, range_, fmt)


def insert_note(worksheet, row, col, note):
    spreadsheet_id = worksheet.spreadsheet.id
    worksheet_id = worksheet.id

    url = f"{SPREADSHEETS_API_V4_BASE_URL}/{spreadsheet_id}:batchUpdate"
    payload = {
        "requests": [
            {
                "updateCells": {
                    "range": {
                        "sheetId": worksheet_id,
                        "startRowIndex": row,
                        "endRowIndex": row + 1,
                        "startColumnIndex": col,
                        "endColumnIndex": col + 1
                    },
                    "rows": [
                        {
                            "values": [
                                {
                                    "note": note
                                }
                            ]
                        }
                    ],
                    "fields": "note"
                }
            }
        ]
    }
    worksheet.spreadsheet.client.request("post", url, json=payload)



def hideColumn(worksheet,colStart,colEnd):
    spreadsheet_id = worksheet.spreadsheet.id
    worksheet_id = worksheet.id
    url = f"{SPREADSHEETS_API_V4_BASE_URL}/{spreadsheet_id}:batchUpdate"
    body = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": worksheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": colStart,
                        "endIndex": colEnd+1
                    },
                    "properties": {
                        "hiddenByUser": True
                    },
                    "fields": "hiddenByUser"
                }
            }
        ]
    }
    worksheet.spreadsheet.client.request("post", url, json=body)

def col2num(col):
    from string import ascii_letters
    num = 0
    for c in col:
        if c in ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num

def colnum_string(n):
    n=int(n+1)
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def addNewSheet(name):
    return sh.add_worksheet(title=name, rows="100", cols="20")


def openCreateWorkSheet(name):
    try:
        worksheet = sh.worksheet(name)
    except:
        worksheet=addNewSheet(name)
    return worksheet


global iRow
iRow=0
def iterationRow():
    global iRow
    iRow=iRow+1
    return iRow-1

def createRowCallsValue():  
    result=operationOnResult.createDictOfResult(idTest,idMod)
    listResult=[]

    listResult.append(CallsOption("RECORDINGS",result['Recordings']))
    listResult.append(CallsOption("RECORDING_PRECENT",result['Recordings_Percent']))
    listResult.append(CallsOption("TRACE_ERROR",result['Trace_Error']))
    listResult.append(CallsOption("TRACE_SUCCES",result['Trace_Succes']))
    listResult.append(CallsOption("TRACE_PERCENT",result['Trace_Percent']))
    listResult.append(CallsOption("TRACE",result['Trace']))
    listResult.append(CallsOption("ALL_CALLS",result['sampleCount']))
    listResult.append(CallsOption("CALLS_PER_S",result['Calls']))
    listResult.append(CallsOption("SEND_KB_PER_S",result['sentKBytesPerSec']))
    listResult.append(CallsOption("AVG_RESPONSE_APP_TIME",result['meanResTime']))
    listResult.append(CallsOption("PROPORION_ERROR_TO_SUCCES",result['errorPct']))
    listResult.append(CallsOption("MODULE_NAME",result['Mod']))
    listResult.append(CallsOption("CALL_DELAY",delay))

    listResult.append(CallsOption("ID",os.getenv("RUN_ID")))
    listResult.append(CallsOption("TIME",operationOnResult.getStartTime()))

    listResult.append(CallsOption("RAM_RDB",result['MV']['cpu']))
    listResult.append(CallsOption("CPU_RDB",result['MV']['ram']))
    listResult.append(CallsOption("DISK_SIZE_RDB",result['MV']['disk_size']))
    listResult.append(CallsOption("DISK_TYPE_RDB",result['MV']['disk_type']))
    listResult.append(CallsOption("DISK_IOPS",result['MV']['disk_iops']))
    listResult.append(CallsOption("PLATFORM_RDB",result['MV']['platform']))

    return listResult
       
def createRowCalls(activeLine,worksheet):
    rowOption=createRowCallsValue()
    for x in rowOption:
        try:
            worksheet.update(createNr(x,activeLine),x.value)
        except:
            print("Call err")



def getType(val):
    for index, item in enumerate(OrderInRow):
        if val in item:
            return index


def createNr(rowOption,activeLine):
    print(rowOption.type_)
    print(colnum_string(getType(rowOption.type_)))
    return f'{colnum_string(getType(rowOption.type_))}{activeLine}'


def addRow(activeLine,worksheet):
    worksheet.insert_row([],activeLine)
    createRowCalls(activeLine,worksheet)

def hideColumnStart(worksheet):
    for index, item in enumerate(OrderInRow):
        if not item[next(iter(item))]:
            hideColumn(worksheet,index,index)

def getAllValueFromRow(line):
    values_list = worksheet.row_values(line)
activeLine=3
worksheet=openCreateWorkSheet(operationOnConfigPython.getRaportName(idTest,idMod,time_))
addRow(activeLine,worksheet)



# insert_note(worksheet, 1, 1, "note")

styleOption=StyleOptions(getColor(),False,'CENTER')
setSyle(worksheet,styleOption,f'{colnum_string(0)}{activeLine}:{colnum_string(len(OrderInRow))}{activeLine}')

hideColumnStart(worksheet)
# hideColumn(worksheet,col2num('A'),3)




