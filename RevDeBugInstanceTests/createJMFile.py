import sys
import re
import json
import os

FILE=os.getenv('MODEL_TEST_FILE_RDB') 

def addCookie(json_):
    return f''' <elementProp name="{json_["name"]}" elementType="Cookie" testname="{json_["name"]}">
<stringProp name="Cookie.value">{json_["value"]}</stringProp>
<stringProp name="Cookie.domain">{json_["domain"]}</stringProp>
<stringProp name="Cookie.path">{json_["path"]}</stringProp>
<boolProp name="Cookie.secure">{json_["secure"]}</boolProp>
<longProp name="Cookie.expires">0</longProp>
<boolProp name="Cookie.path_specified">true</boolProp>
<boolProp name="Cookie.domain_specified">true</boolProp>
</elementProp> '''

def addCookies(jsonList_, model):
    result=''
    for x in jsonList_:
        result=result+addCookie(x)


def getModel():
    
    


def create(jsonList_):
    print(jsonList_)
