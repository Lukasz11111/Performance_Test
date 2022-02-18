import gspread
from gspread.urls import SPREADSHEETS_API_V4_BASE_URL
from gspread_formatting import *
import sys
import operatinonOnResultRDBTest
sys.path.append("/app")
import operationOnConfigPython
import operationOnResult
import json
import os
import time
from datetime import datetime


gc = gspread.service_account(filename='./file.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1BToFDEIASReYQERkGrCwgzo6TgWNNT9ySw2dWG5FHc4/edit#gid=0')

legendLine=1
activeLine=2


OrderInRow=[
    
    {"ID":False},
    {"TIME":False},
    {"ERROR_COUNT":True},
    {"ERROR_PCT":True},
    {"ENDPOINTS":True},
    {"USERS":True},
    {"ALL_CALLS":True},
    {"CALLS_PER_S":True},
    {"CALL_DELAY":True},
    {"MEAN_RES_TIME":True},
    {"MEDIAN_RES_TIME":True},
    {"MIN_RES_TIME":True},
    {"MAX_RES_TIME":True},
    {"PCT_RES_TIME_90":True},
    {"PCT_RES_TIME_95":True},
    {"PCT_RES_TIME_99":True},
    {"THROUGHPUT":True},
    {"RECEIVED_KBYTES_PER_SEC":True},
    {"SENT_KBYTES_PER_SEC":True},
    {"EMPTY_SERVER":True},
    {"CPU_RDB":False},
    {"RAM_RDB":False},
    {"DISK_SIZE_RDB":False},
    {"DISK_TYPE_RDB":False},
    {"DISK_IOPS":False},
    {"PLATFORM_RDB":False},
    {"VERSION_RDB":False},
    {"SSL_ON_RDB":False},
]


class CallsOption():
    type_=''
    value=''
    hide=''
    def __init__(self,type_='',value=''):
        self.type_=type_
        self.value=value



class StyleOptions():
    def __init__(self,color,bold,horizontalAlignment,size=10):
        self.color=color
        self.bold=bold
        self.horizontalAlignment=horizontalAlignment
        self.size=size
    color=0
    bold=False
    horizontalAlignment='CENTER'





def setSyle(worksheet,styleOption,range_,fontSize_=10,wrapStrategy_='OVERFLOW_CELL'):
    fmt = cellFormat(
    backgroundColor=color(styleOption.color.red, styleOption.color.green, styleOption.color.blue),
    textFormat=textFormat(bold=styleOption.bold,fontSize=fontSize_,foregroundColor=color(1-styleOption.color.red, 1-styleOption.color.green, 1-styleOption.color.blue)),
    horizontalAlignment=styleOption.horizontalAlignment , wrapStrategy =wrapStrategy_
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
                        "startRowIndex": row-1,
                        "endRowIndex": row,
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



def getNote(worksheet, cell_):
    spreadsheet_id = worksheet.spreadsheet.id
    worksheet_id = worksheet.id
    return worksheet.spreadsheet.get_worksheet_by_id(worksheet_id).get_note(cell=cell_)
    

    

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
    worksheet=sh.add_worksheet(title=name, rows="100", cols="20")
    createLegend(worksheet)
    return worksheet
    
def createLegend(worksheet):
    list_=[]
    for index, item in enumerate(OrderInRow):
        list_.append(formatString(next(iter(item))))

    worksheet.update(createRowNr(legendLine),[list_])
    styleOption=StyleOptions(color.fromHex('#292421'),True,"CENTER")
    setSyle(worksheet,styleOption,createRowNr(legendLine),8,"WRAP")

def formatString(string_):
    string_=str(string_)
    string_=string_.replace("_", " ")
    string_=string_.lower()
    string_=string_.capitalize() 
    return string_

def sheetName(idTest,idMod):
    return operationOnResult.getSheetName(idTest, idMod)

def openCreateWorkSheet(idTest,idMod):
    name=operationOnConfigPython.getRaportName(idTest,idMod)
    try:
        worksheet = sh.worksheet(name)
    except:
        worksheet=addNewSheet(name)
        time.sleep(3)
    return worksheet

def createRowCallsValue(idTest, idMod):  
    result=operatinonOnResultRDBTest.createDictOfResult(idTest,idMod)

    listResult=[]
    listResult.append(CallsOption("ID",os.getenv("RUN_ID")))
    listResult.append(CallsOption("TIME",str(datetime.fromtimestamp(time.time()))))

    listResult.append(CallsOption("USERS",result['users']))
    listResult.append(CallsOption("ERROR_COUNT",result['errorCount']))
    listResult.append(CallsOption("ERROR_PCT",result['errorPct']))
    listResult.append(CallsOption("ENDPOINTS",result['endpoints']))
    listResult.append(CallsOption("ALL_CALLS",result['sampleCount']))
    listResult.append(CallsOption("CALLS_PER_S",result['Calls']))

    listResult.append(CallsOption("MEAN_RES_TIME",result['meanResTime']))
    listResult.append(CallsOption("MEDIAN_RES_TIME",result['medianResTime']))
    listResult.append(CallsOption("MIN_RES_TIME",result['minResTime']))
    listResult.append(CallsOption("MAX_RES_TIME",result['maxResTime']))
    listResult.append(CallsOption("PCT_RES_TIME_90",result['pct1ResTime']))
    listResult.append(CallsOption("PCT_RES_TIME_95",result['pct2ResTime']))
    listResult.append(CallsOption("PCT_RES_TIME_99",result['pct3ResTime']))
    listResult.append(CallsOption("THROUGHPUT",result['throughput']))
    listResult.append(CallsOption("RECEIVED_KBYTES_PER_SEC",result['receivedKBytesPerSec']))
    listResult.append(CallsOption("SENT_KBYTES_PER_SEC",result['sentKBytesPerSec']))
    listResult.append(CallsOption("EMPTY_SERVER",result['emptyServer']))
    listResult.append(CallsOption("CALL_DELAY",delay))

    listResult.append(CallsOption("RAM_RDB",result['MV']['cpu']))
    listResult.append(CallsOption("CPU_RDB",result['MV']['ram']))
    listResult.append(CallsOption("DISK_SIZE_RDB",result['MV']['disk_size']))
    listResult.append(CallsOption("DISK_TYPE_RDB",result['MV']['disk_type']))
    listResult.append(CallsOption("DISK_IOPS",result['MV']['disk_iops']))
    listResult.append(CallsOption("PLATFORM_RDB",result['MV']['platform']))

    listResult.append(CallsOption("VERSION_RDB",result['rdb_version']))
    listResult.append(CallsOption("SSL_ON_RDB",result['ssl']))

    return listResult

def sortListValueRow(idTest, idMod):
    rowOptionList=createRowCallsValue(idTest, idMod)
    resultList=[]
    for x in rowOptionList:
        index=getType(x.type_)
        try:
            resultList.insert(index,int(x.value))
        except:
            resultList.insert(index,str(x.value))
        try:
            if resultList[index]==None:
                resultList[index]='-'
        except:
            pass
    return resultList

def createRowCalls(activeLine,worksheet,idTest, idMod):
    rowOptions=sortListValueRow(idTest, idMod)
    try:
        worksheet.update(createRowNr(activeLine),[rowOptions])
    except:
        print("Call err")


def insertNotes(activeLine,worksheet,idTest, idMod):
    insert_note(worksheet, activeLine, getType('VERSION_RDB'), operationOnResult.getRDBCommits(idTest, idMod))

    

def getType(val):
    for index, item in enumerate(OrderInRow):
        if val in item:
            return index


def createRowNr(activeLine):
    return f'A{activeLine}:{colnum_string(len(OrderInRow))}{activeLine}'


def addRow(activeLine,worksheet,idTest, idMod):
    worksheet.insert_row([],activeLine)
    createRowCalls(activeLine,worksheet,idTest, idMod)

def hideColumnStart(worksheet):
    for index, item in enumerate(OrderInRow):
        if not item[next(iter(item))]:
            hideColumn(worksheet,index,index)

def getAllValueFromRow(line):
    values_list = worksheet.row_values(line)


def startGenRaportOnGoogleSheet(idTest,idMod):
    worksheet=openCreateWorkSheet(idTest,idMod)
    addRow(activeLine,worksheet,idTest, idMod)
    styleOption=StyleOptions(color.fromHex(operatinonOnResultRDBTest.getColor(idTest,idMod)),False,'CENTER')
    setSyle(worksheet,styleOption,f'{colnum_string(0)}{activeLine}:{colnum_string(len(OrderInRow)-1)}{activeLine}')
    insertNotes(activeLine,worksheet,idTest, idMod)
 



idTest=sys.argv[1]
idMod=sys.argv[2]
delay=sys.argv[3]




if delay=="hide":
    worksheet=openCreateWorkSheet(idTest,idMod)
    hideColumnStart(worksheet)
else:
    startGenRaportOnGoogleSheet(idTest, idMod)

# getNote(worksheet,"V3")

# values_list = worksheet.row_values(activeLine)
# print(values_list)
# worksheet.update('A2:C4', [[1, 2,2], [1, 2,2], [1, 2,2]])
# hideColumn(worksheet,col2num('A'),3)




