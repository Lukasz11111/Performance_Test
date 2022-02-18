import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import sys
import json
import createJMFile
sys.path.append("/app")
import operationOnConfigPython
import operationOnResult
 


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-xss-auditor")
options.add_argument("disable-web-security")
options.add_argument("allow-running-insecure-content")
options.add_argument("no-sandbox")
options.add_argument("disable-setuid-sandbox")
options.add_argument("disable-webgl")
options.add_argument("disable-popup-blocking")
options.add_argument('--disable-dev-shm-usage')
options.add_argument('ignore-certificate-errors')

idTest=sys.argv[1]
idMod=sys.argv[2]
DELAY=sys.argv[3]

HOST=operationOnConfigPython.getRDBHost(idTest,idMod)
PROTOCOL=operationOnConfigPython.getRdbProtocol(idTest,idMod)

driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=options)  

driver.get(f'{PROTOCOL}://{HOST}/home')

if operationOnConfigPython.getKeycloakActiv(idTest,idMod):
    Xuser="/html//input[@id='username']"
    Xpass="/html//input[@id='password']"
else:
    Xuser="/html//input[@id='email']"
    Xpass="/html//input[@id='password']"


search_user = driver.find_element(By.XPATH,Xuser)

search_user.send_keys(str(operationOnConfigPython.getLogin(idTest,idMod)))

search_pass= driver.find_element(By.XPATH,Xpass)

search_pass.send_keys(str(operationOnConfigPython.getPass(idTest,idMod)))

search_pass.submit()

driver.find_element(By.XPATH,"//html//a[@id='settings-dropdown']").click()
version = driver.find_element(By.XPATH,"//div[@id='settings-submenu']/p").get_attribute("innerHTML")

operationOnResult.setVersion(version)

print(version)

createJMFile.create(driver.get_cookies(),idTest,idMod, DELAY)

driver.quit()
