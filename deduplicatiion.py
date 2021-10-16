import time

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-xss-auditor")
options.add_argument("disable-web-security")
options.add_argument("allow-running-insecure-content")
options.add_argument("no-sandbox")
options.add_argument("disable-setuid-sandbox")
options.add_argument("disable-webgl")
options.add_argument("disable-popup-blocking")

import os
import sys

HOST="20.188.58.169"
PROTOCOL="http"

driver = webdriver.Chrome('/usr/bin/chromedriver',options=options)  

driver.get(f'{PROTOCOL}://{HOST}')

search_user = driver.find_element(By.XPATH,"/html//input[@id='email']")

search_user.send_keys(os.environ['LC_RDB_LOGIN'])

search_pass= driver.find_element(By.XPATH,"/html//input[@id='password']")

search_pass.send_keys(os.environ['LC_RDB_PASS'])

search_pass.submit()

driver.get(f'{PROTOCOL}://{HOST}/GlobalSettings/SaveRecordingSettings?deduplication=false&crashRecordingsCount=100&recordingMode=4')

driver.quit()

