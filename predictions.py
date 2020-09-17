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

    def scrape(self):
        # TO DO - CONNECT THE DATABASE
        connector = sqlite3.connect('games-db')
        cursor = connector.cursor()
        cursor.execute("DROP TABLE IF EXISTS Predictions")
        cursor.execute('CREATE TABLE Predictions(time TEXT, home_team TEXT, away_team TEXT,'
                       ' home_prob DECIMAL, draw_prob DECIMAL, away_prob DECIMAL, bet_sign DECIMAL,'
                       ' score_predict TEXT, avg_goals REAL, odds REAL, temp TEXT)')

        # OPEN THE WEBSITE AND GET THE DATA
        options = ChromeOptions()
        options.headless = False   # IF YOU WANT TO SEE THE BROWSER -> FALSE
        driver = Chrome(options=options, executable_path='C://Windows/chromedriver.exe')
        driver_tomorrow = Chrome(options=options, executable_path='C://Windows/chromedriver.exe')
        driver.get(self.WEB_LINKS['football_today'])
        driver_tomorrow.get(self.WEB_LINKS['football_tomorrow'])
        sleep(2)
        # TO DO - > PRESS [MORE] BUTTON ON THE BOTTOM UNTIL DISAPPEAR
        html_today = driver.execute_script('return document.documentElement.outerHTML;')
        html_tomorrow = driver_tomorrow.execute_script('return document.documentElement.outerHTML;')

        # WORK WITH THE DATA
        today_soup = bs4.BeautifulSoup(html_today, 'html.parser')
        tomorrow_soup = bs4.BeautifulSoup(html_tomorrow, 'html.parser')
        matches_one_today = today_soup.find_all(class_=re.compile('tr_0'))
        matches_two_today = today_soup.find_all(class_=re.compile('tr_1'))
        matches_one_tomorrow = tomorrow_soup.find_all(class_=re.compile('tr_0'))
        matches_two_tomorrow = tomorrow_soup.find_all(class_=re.compile('tr_1'))
        [print(game) for game in matches_one_today]
        [print(game) for game in matches_two_today]
        [print(game) for game in matches_one_tomorrow]
        [print(game) for game in matches_two_tomorrow]
        driver.close()
        cursor.close()


scraper = Predictions()
scraper.scrape()