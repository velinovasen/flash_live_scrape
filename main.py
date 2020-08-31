import bs4
from selenium.webdriver import Firefox, FirefoxOptions
import sqlite3
import re
from contextlib import suppress
from time import sleep


WEB_LINKS = {
    "flashscore": "https://www.soccer24.com/"
}

#
#
#          TO CONNECT THE DATABASE LATER
#
#


options = FirefoxOptions()
options.headless = False
driver = Firefox(options=options, executable_path='C://Windows/geckodriver.exe')
driver.get(WEB_LINKS["flashscore"])

while True:
    with suppress(Exception):
        driver.find_element_by_css_selector('.calendar__direction--tomorrow').click()
        break

sleep(2)
html = driver.execute_script("return document.documentElement.outerHTML;")

