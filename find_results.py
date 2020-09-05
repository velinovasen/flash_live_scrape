import bs4
from selenium.webdriver import FirefoxOptions, Firefox
import sqlite3
import re
import time


class FindResults:

    WEB_LINKS = {
        "football": "https://www.soccer24.com/"
    }

    def find(self):

        # CONNECT THE DATABASE

        # SET UP THE DRIVER
        options = FirefoxOptions()
        options.headless = True
        driver = Firefox(options=options, executable_path='C://Windows/geckodriver.exe')
        driver.get(self.WEB_LINKS["football"])
        time.sleep(1)
        driver.find_element_by_css_selector('#live-table > div.tabs > div.calendar > div:nth-child(1) > div').click()
        time.sleep(1)
        html = driver.execute_script('return document.documentElement.outerHTML;')

        # GET THE DATA
        soup = bs4.BeautifulSoup(html, 'html.parser')
        matches = soup.find_all(class_=re.compile('event__match'))
        all_games = [print(list(game)) for game in matches if 'Finished' in str(game)]

        # WORK WITH THE DATA

        # INSERT THE DATA INTO THE DATABASE

        driver.close()

scrp = FindResults()
scrp.find()