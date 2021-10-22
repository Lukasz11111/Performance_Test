import time

from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import sys
import json

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

JSON_CONFIG_PATH=sys.argv[1]+"/.config"

with open(JSON_CONFIG_PATH) as f:
    json_config = json.load(f)

HOST=json_config['server_rdb']
PROTOCOL=json_config['protocol']

driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=options)  

driver.get(f'{PROTOCOL}://{HOST}')

search_user = driver.find_element(By.XPATH,"/html//input[@id='email']")

search_user.send_keys(os.environ['LC_RDB_LOGIN'])

search_pass= driver.find_element(By.XPATH,"/html//input[@id='password']")

search_pass.send_keys(os.environ['LC_RDB_PASS'])

search_pass.submit()

driver.get(f'{PROTOCOL}://{HOST}/GlobalSettings/SaveRecordingSettings?deduplication=false&crashRecordingsCount=100&recordingMode=4')

driver.quit()

