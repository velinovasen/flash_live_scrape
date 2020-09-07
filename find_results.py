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
        connector = sqlite3.connect('games-db')
        cursor = connector.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS allResults(win TEXT,'
                       ' home_team TEXT, away_team TEXT, home_score DECIMAL,'
                       ' away_score DECIMAL, home_odd REAL,'
                       ' draw_odd REAL, away_odd REAL)')
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
        all_games = [list(game)[2:] for game in matches if 'Finished' in str(game)]

        # WORK WITH THE DATA
        for game in all_games:
            items = {"home_team": "", "away_team": "", "home_score": "",
                     "away_score": "", "home_odd": "", "draw_odd": "", "away_odd": ""}
            for element in game:
                if 'participant--home' in str(element):
                    pattern = r'\"\>([A-z0-9]+.+)\<\/'
                    home_team = re.search(pattern, str(element))
                    items["home_team"] = home_team.group(1)
                elif 'participant--away' in str(element):
                    pattern = r'\"\>([A-z0-9]+.+)\<\/'
                    away_team = re.search(pattern, str(element))
                    items["away_team"] = away_team.group(1)
                elif 'event__scores' in str(element):
                    pattern = r'[n]\>(\d+)\<\/'
                    tokens = re.findall(pattern, str(element))
                    items["home_score"] = int(tokens[0])
                    items["away_score"] = int(tokens[1])
                elif 'o_1' in str(element):
                    pattern = r'\"\>(\d{1,2}\.\d{2})\<\/[s]'
                    try:
                        home_odd = re.search(pattern, str(element))
                        items["home_odd"] = home_odd.group(1)
                    except AttributeError:
                        items["home_odd"] = "1.00"
                elif 'o_0' in str(element):
                    pattern = r'\"\>(\d{1,2}\.\d{2})\<\/[s]'
                    try:
                        draw_odd = re.search(pattern, str(element))
                        items["draw_odd"] = draw_odd.group(1)
                    except AttributeError:
                        items["draw_odd"] = "1.00"
                elif 'o_2' in str(element):
                    pattern = r'\"\>(\d{1,2}\.\d{2})\<\/[s]'
                    try:
                        away_odd = re.search(pattern, str(element))
                        items["away_odd"] = away_odd.group(1)
                    except AttributeError:
                        items["away_odd"] = "1.00"
            print(items)

        # INSERT THE DATA INTO THE DATABASE

        driver.close()


scrp = FindResults()
scrp.find()
