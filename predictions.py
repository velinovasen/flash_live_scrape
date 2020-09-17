import sqlite3
from selenium.webdriver import Chrome, ChromeOptions
import bs4
import re
from time import sleep


class Predictions:

    WEB_LINKS = {
        'football_today': 'https://m.forebet.com/en/football-tips-and-predictions-for-today',
        'football_tomorrow': 'https://m.forebet.com/en/football-tips-and-predictions-for-tomorrow'
    }

    REGEX = {
        "both_teams": r'[t]\=\"(.{1,60})[ ][v][s][ ](.{1,60})\"[ ]'
    }

    def scrape(self):
        # TO DO - CONNECT THE DATABASE
        connector = sqlite3.connect('games-db')
        cursor = connector.cursor()
        cursor.execute("DROP TABLE IF EXISTS Predictions")
        cursor.execute('CREATE TABLE Predictions(time TEXT, home_team TEXT, away_team TEXT,'
                       ' home_prob DECIMAL, draw_prob DECIMAL, away_prob DECIMAL, bet_sign DECIMAL,'
                       ' score_predict TEXT, avg_goals REAL, odds REAL, temp TEXT)')

        # OPEN THE WEBSITE AND WORK WITH IT
        options = ChromeOptions()
        options.headless = True   # IF YOU WANT TO SEE THE BROWSER -> FALSE
        driver = Chrome(options=options, executable_path='C://Windows/chromedriver.exe')
        driver_tomorrow = Chrome(options=options, executable_path='C://Windows/chromedriver.exe')
        driver.get(self.WEB_LINKS['football_today'])
        driver_tomorrow.get(self.WEB_LINKS['football_tomorrow'])
        sleep(3)

        # PRESS [MORE] BUTTON ON THE BOTTOM UNTIL DISAPPEAR

        # PROBLEM WITH IT - > IT'S NOT PRESSING ALWAYS
        while True:
            try:
                sleep(5)
                driver.find_element_by_css_selector('/html/body/div[1]/div[2]/div[2]/div[2]/table/tbody/tr[47]/td/span').click()
                driver_tomorrow.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/table/tbody/tr[47]/td/span').click()
            except Exception:
                sleep(3)
                break

        # GET THE DATA
        html_today = driver.execute_script('return document.documentElement.outerHTML;')
        html_tomorrow = driver_tomorrow.execute_script('return document.documentElement.outerHTML;')

        # CLOSE THE BROWSERS
        driver_tomorrow.close()
        driver.close()

        # WORK WITH THE DATA
        today_soup = bs4.BeautifulSoup(html_today, 'html.parser')
        tomorrow_soup = bs4.BeautifulSoup(html_tomorrow, 'html.parser')
        matches_one_today = today_soup.find_all(class_=re.compile('tr_0'))
        matches_two_today = today_soup.find_all(class_=re.compile('tr_1'))
        matches_one_tomorrow = tomorrow_soup.find_all(class_=re.compile('tr_0'))
        matches_two_tomorrow = tomorrow_soup.find_all(class_=re.compile('tr_1'))
        all_games = []
        all_games += [list(game) for game in matches_one_today]
        all_games += [list(game) for game in matches_two_today]
        all_games += [list(game) for game in matches_one_tomorrow]
        all_games += [list(game) for game in matches_two_tomorrow]

        # SEARCH THE DATA WE NEED
        for game in all_games:
            # FIND THE TEAMS
            both_teams = re.search(self.REGEX["both_teams"], str(game))
            print(both_teams)
            # home_team = both_teams.group(1)
            # away_team = both_teams.group(2)
            # print(f"{home_team} - {away_team}")

        cursor.close()


scraper = Predictions()
scraper.scrape()