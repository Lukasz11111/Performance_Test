import time
import sys
sys.path.append("/app")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os

import json

import operationOnConfigPython
import operationOnResult

options = webdriver.ChromeOptions()
options.add_argument('headless')
# options.add_argument("disable-xss-auditor")
# options.add_argument("disable-web-security")
# options.add_argument("allow-running-insecure-content")
options.add_argument("no-sandbox")
# options.add_argument("disable-setuid-sandbox")
# options.add_argument("disable-webgl")
# options.add_argument("disable-popup-blocking")
# options.add_argument('--disable-dev-shm-usage')

idTest=sys.argv[1]
idMod=sys.argv[2]

password=str(operationOnConfigPython.getPass(idTest,idMod))
user=str(operationOnConfigPython.getLogin(idTest,idMod))



HOST=operationOnConfigPython.getRDBHost(idTest,idMod)
PROTOCOL=operationOnConfigPython.getRdbProtocol(idTest,idMod)


driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=options)  

def keycloak_():
    Xuser="/html//input[@id='username']"
    Xpass="/html//input[@id='password']"
    xuserKey="//*[contains(text(), 'Users')]"
    addUserBtn="/html//a[@id='createUser']"
    newUserUsername="/html//input[@id='username']"
    console_damin="//*[contains(text(), 'Administration Console')]"
    save="//*[contains(text(), 'Save')]"
    credentials="//*[contains(text(), 'Credentials')]"
    rol_mapping="//*[contains(text(), 'Role Mappings')]"
    pass_one="/html//input[@id='newPas']"
    pass_two="/html//input[@id='confirmPas']"
    temporary="//div[@id='view']//form[@name='userForm']//span[@class='ng-isolate-scope ng-not-empty ng-valid']/div[@class='onoffswitch']/label[@class='onoffswitch-label']//span[.='ON']"
    setPass_two="//body/div[@role='dialog']/div[@class='modal-dialog']//div[@class='modal-footer ng-scope']/button[2]"
    setPass="//div[@id='view']/div[1]/form[@name='userForm']//div[@class='col-md-10 col-md-offset-2']/button[@class='btn btn-default ng-binding']"
    dialog="//body/div[@role='dialog']/div[@class='modal-dialog']//div[@class='modal-footer ng-scope']/button[2]"
    select_role="//select[#'available']"
    add_role="//*[contains(text(), 'Add selected')]"
    sysop="//select[@id='available']/option[@title='Sysop']"

    driver.get(f'{PROTOCOL}://{HOST}/auth')

    driver.find_element(By.XPATH,console_damin).click()

    wait=0.6

    time.sleep(wait)

    search_user = driver.find_element(By.XPATH,Xuser)

    search_user.send_keys('admin')

    search_pass= driver.find_element(By.XPATH,Xpass)

    search_pass.send_keys('admin')

    search_pass.submit()
    time.sleep(3)
    driver.find_element(By.XPATH,xuserKey).click()
    time.sleep(wait)
    driver.find_element(By.XPATH,addUserBtn).click()
    time.sleep(wait)
    try:
        username_input=driver.find_element(By.XPATH,newUserUsername)
        username_input.send_keys(user)
        driver.find_element(By.XPATH,save).click()
        time.sleep(wait)
    
        driver.find_element(By.XPATH,credentials).click()
    except:
        driver.find_element(By.XPATH,xuserKey).click()
        driver.find_element(By.XPATH,credentials).click()

    time.sleep(wait)

    pass_input=driver.find_element(By.XPATH,pass_one)
    pass_input.send_keys(password)
    pass_two_input=driver.find_element(By.XPATH,pass_two)
    pass_two_input.send_keys(password)
    driver.find_element(By.XPATH,temporary).click()
    time.sleep(0.1)

    driver.find_element(By.XPATH,setPass).click()
    time.sleep(0.01)
    driver.find_element(By.XPATH,setPass_two).click()

    time.sleep(0.4)

    time.sleep(wait)
    driver.find_element(By.XPATH,rol_mapping).click()
    time.sleep(wait)

    driver.find_element(By.XPATH,sysop).click()
    driver.find_element(By.XPATH,add_role).click()
    time.sleep(wait)

def deduplicationAndVersion(Xuser,Xpass):
    wait=0.5
    driver.get(f'{PROTOCOL}://{HOST}/home')
    time.sleep(wait)
    search_user = driver.find_element(By.XPATH,Xuser)

    search_user.send_keys(user)

    search_pass= driver.find_element(By.XPATH,Xpass)

    search_pass.send_keys(password)

    search_pass.submit()
    time.sleep(2)
    driver.find_element(By.XPATH,"//html//a[@id='settings-dropdown']").click()
    time.sleep(wait)
    version = driver.find_element(By.XPATH,"//div[@id='settings-submenu']/p").get_attribute("innerHTML")

    operationOnResult.setVersion(version)

    driver.get(f'{PROTOCOL}://{HOST}/GlobalSettings/SaveRecordingSettings?deduplication=false&crashRecordingsCount=100&recordingMode=4')

    driver.quit()



if operationOnConfigPython.getKeycloakActiv(idTest,idMod):
    keycloak_()
    Xuser="/html//input[@id='username']"
    Xpass="/html//input[@id='password']"
    deduplicationAndVersion(Xuser,Xpass)
else:
    Xuser="/html//input[@id='email']"
    Xpass="/html//input[@id='password']"
    deduplicationAndVersion(Xuser,Xpass)

