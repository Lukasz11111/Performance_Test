import gspread
from gspread.urls import SPREADSHEETS_API_V4_BASE_URL
from gspread_formatting import *
import sys
import operationOnConfigPython
import operationOnResult
import json
idTest=sys.argv[1]
idMod=sys.argv[2]
time_=sys.argv[3]
delay=sys.argv[4]

gc = gspread.service_account(filename='./file.json')

sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1BToFDEIASReYQERkGrCwgzo6TgWNNT9ySw2dWG5FHc4/edit#gid=0')

worksheet = sh.get_worksheet(0)
worksheet.update('B1', 'Bingo!')

class RowOption():
    recordings=0
    trace=0
    traceErr=0
    traceSuc=0
    procentRecording=0
    procentTrace=0
    allCallJM=0
    callPerSecond=0
    sentKbPerSecond=0
    responseAvg=0
    proportionSuccesToError=0
    mod=0
    callDelay=0
    def __init__(self,recordings,trace,traceErr,traceSuc,procentRecording,procentTrace,allCallJM,callPerSecond,sentKbPerSecond,responseAvgproportionSuccesToError,mod,callDelay):
        self.recordings=recordings
        self.trace=trace
        self.traceErr=traceErr
        self.traceSuc=traceSuc
        self.procentRecording=procentRecording
        self.procentTrace=procentTrace
        self.allCallJM=allCallJM
        self.callPerSecond=callPerSecond
        self.sentKbPerSecond=sentKbPerSecond
        self.responseAvg=responseAvg
        self.proportionSuccesToError=proportionSuccesToError
        self.mod=mod
        self.callDelay=callDelay

class CallsOption():
    column=0
    value=''
    valLegend=''
    def __init__(self,column=0,value=0):
        self.column=column
        self.value=value



class StyleOptions():
    def __init__(self,red,blue,green,bold,horizontalAlignment):
        self.red=red
        self.blue=blue
        self.green=green
        self.bold=bold
        self.horizontalAlignment=horizontalAlignment
    red=0
    blue=0
    green=0
    bold=False
    horizontalAlignment='CENTER'

def setSyle(worksheet,styleOption,range_):
    fmt = cellFormat(
    backgroundColor=color(styleOption.red,styleOption.green, styleOption.blue),
    textFormat=textFormat(bold=styleOption.bold, foregroundColor=color(1-styleOption.red, 1-styleOption.green, 1-styleOption.blue)),
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
                        "endIndex": colEnd
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

def addNewSheet(name):
    return sh.add_worksheet(title=name, rows="100", cols="20")


def openCreateWorkSheet(name):
    try:
        worksheet = sh.worksheet(name)
    except:
        worksheet=addNewSheet(name)
    return worksheet


openCreateWorkSheet(operationOnConfigPython.getRaportName(idTest,idMod,time_))


def addRow(activeLine):
    sheet.append_row(activeLine)

global iRow
iRow=0
def iterationRow():
    global iRow
    iRow=iRow+1
    return iRow-1

def createRowCalls():  
    resultJson=operationOnResult
    recordings=CallsOption(iterationRow(),)
    trace=CallsOption(iterationRow(),)
    traceErr=CallsOption(iterationRow(),)
    traceSuc=CallsOption(iterationRow(),)
    procentRecording=CallsOption(iterationRow(),)
    procentTrace=CallsOption(iterationRow(),)
    allCallJM=CallsOption(iterationRow())
    callPerSecond=CallsOption(iterationRow())
    sentKbPerSecond=CallsOption(iterationRow())
    responseAvg=CallsOption(iterationRow())
    proportionSuccesToError=CallsOption(iterationRow())
    mod=CallsOption(iterationRow())
    callDelay=CallsOption(iterationRow())
    return RowOption(recordings,trace,traceErr,traceSuc,procentRecording,procentTrace,allCallJM,callPerSecond,sentKbPerSecond,responseAvgproportionSuccesToError,mod,callDelay):
       


createRowCalls()
# insert_note(worksheet, 1, 1, "note")

# styleOption=StyleOptions(0.2,0.5,0,False,'CENTER')
# setSyle(worksheet,styleOption,'A1:A1')

# hideColumn(worksheet,col2num('A'),3)
