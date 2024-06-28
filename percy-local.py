from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from dotenv import load_dotenv
import os, json, time
from browserstack.local import Local
from percy.snapshot import percy_snapshot


load_dotenv()
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY")
URL ="url"

bs_local = Local()
bs_local_args = { "key": BROWSERSTACK_ACCESS_KEY }
bs_local.start(**bs_local_args)

bstack_options = {
    "os" : "Windows",
    "osVersion" : "10",
    "browserName" : "Chrome",
    "buildName" : "browserstack-build-13",
    "sessionName" : "BStack local python",
    "userName": BROWSERSTACK_USERNAME,
    "accessKey": BROWSERSTACK_ACCESS_KEY,
    "local": "true"
}

bstack_options["source"] = "python:sample-main:v1.0"
options = ChromeOptions()
options.set_capability('bstack:options', bstack_options)

driver=webdriver.Remote(URL, options=options)
try:
    driver.get('http://127.0.0.1:5000/')
    percy_snapshot(driver, 'Homepage')
    time.sleep(5)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Successfully Verified!"}}')
except Exception as err:
    message = "Exception: " + str(err.__class__) + str(err.msg)
    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}')
driver.quit()