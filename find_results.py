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
        cursor.execute('DROP TABLE allResults')
        cursor.execute('CREATE TABLE allResults(win TEXT,'
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

        # CLOSE THE BROWSER
        driver.close()

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
                    pattern = r'(\"\>([A-z0-9]+.+)\<[s][v][g][ ]|\"\>[A-z0-9].+\<\/[d][i])'
                    home_team = re.search(pattern, str(element))
                    home_team_token = home_team.group(1)[2:].split('<')
                    items["home_team"] = home_team_token[0]
                elif 'participant--away' in str(element):
                    pattern = r'(\"\>([A-z0-9]+.+)\<[s][v][g][ ]|\"\>[A-z0-9].+\<\/[d][i])'
                    away_team = re.search(pattern, str(element))
                    team_away_token = away_team.group(1)[2:].split('<')
                    items["away_team"] = team_away_token[0]
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

        # INSERT THE DATA INTO THE DATABASE
            cursor.execute('INSERT INTO allResults(home_team, away_team, home_score,'
                           ' away_score, home_odd, draw_odd, away_odd) VALUES'
                           ' (?, ?, ?, ?, ?, ?, ?)', (items["home_team"], items["away_team"],
                                                      items["home_score"], items["away_score"],
                                                      items["home_odd"], items["draw_odd"],
                                                      items["away_odd"]))
        connector.commit()
        connector.close()


scrp = FindResults()
scrp.find()
