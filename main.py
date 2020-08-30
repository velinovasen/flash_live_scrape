import bs4
from selenium.webdriver import Firefox, FirefoxOptions
import sqlite3
import re
from contextlib import suppress
from time import sleep


WEB_LINKS = {
    "flashscore": "https://www.flashscore.com/"
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
        driver.find_element_by_css_selector('#live-table > div.tabs > div.tabs__group > div:nth-child(2) > div.tabs__text.tabs__text--long').click()
        sleep(4)