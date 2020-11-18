import sqlite3
from selenium.webdriver import Chrome, ChromeOptions
import bs4
import re
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager


class ValueBets:
    WEB_LINKS = {
        "football": "https://m.forebet.com/en/value-bets"
    }

    REGEX = {
        "home": r'[e][T][e][a][m]\"\>\<[s][p][a][n]\>(.{1,60})\<\/[s][p][a][n]\>\<\/[s][p][a][n]\>\<[s]',
        "away": r'[y][T][e][a][m]\"\>\<[s][p][a][n]\>(.{1,60})\<\/[s][p][a][n]\>\<\/[s][p][a][n]\>\<\/[a]',
        "date_and_time": r'\"\>(\d{1,2}\/\d{1,2}\/\d{4})[ ](\d{1,2}\:\d{1,2})\<\/',
        "probabilities": r'\>(\d{1,2})\<\/([t]|[b])',
        "prediction": r'[t]\"\>([A-z0-9])\<\/',
        "odd_for_prediction": r'\;\"\>(\d{1,3}\.\d{1,2})\<\/',
        "value_percent": r'[b]\>(\d{1,3})\%',
        "all_odds": r'[n]\>(\d{1,3}\.\d{1,2})\<\/',
    }

    def scrape(self):
        # CONNECT THE DATABASE
        connector, cursor = self.connect_the_database()

        # OPEN THE BROWSER
        driver = self.open_the_browser()

        # GET THE HTML DATA
        all_games = self.get_the_data(driver)

        # GET THE GAMES FROM THE DATA
        self.clean_data(all_games, cursor)

        connector.commit()
        cursor.close()
        connector.close()

    def open_the_browser(self):
        options = ChromeOptions()
        options.headless = False  # -> FALSE IF YOU WANT TO SEE THE BROWSER BROWSING
        driver = Chrome(options=options, executable_path=ChromeDriverManager().install())
        driver.get(self.WEB_LINKS["football"])
        sleep(3)
        driver.find_element_by_css_selector('#close-cc-bar').click()
        return driver

    def clean_data(self, all_games, cursor):
        for game in all_games:
            print(game)
            # STORE ALL THE ITEMS
            items = {}

            # FIND THE TEAMS
            try:
                items["home"] = re.search(self.REGEX["home"], str(game)).group(1)
                items["away"] = re.search(self.REGEX["away"], str(game)).group(1)
            except AttributeError:
                continue

            # FIND DATE AND TIME
            try:
                date_and_time = re.search(self.REGEX["date_and_time"], str(game))
                items["date"] = date_and_time.group(1)
                items["time"] = date_and_time.group(2)
            except AttributeError:
                pass

            # FIND THE PROBABILITIES
            probabilities = re.findall(self.REGEX["probabilities"], str(game))
            items["home_prob"] = probabilities[0][0]
            items["draw_prob"] = probabilities[1][0]
            items["away_prob"] = probabilities[2][0]

            # FIND THE PREDICTION
            items["prediction"] = re.search(self.REGEX["prediction"], str(game)).group(1)

            # FIND THE ODD
            items["odd_for_prediction"] = re.search(self.REGEX["odd_for_prediction"], str(game)).group(1)

            # FIND THE VALUE PERCENT
            items["value_percent"] = re.search(self.REGEX["value_percent"], str(game)).group(1)

            # FIND THE ODDS
            try:
                odds = re.findall(self.REGEX["all_odds"], str(game))
                items["home_odd"] = odds[0]
                items["draw_odd"] = odds[1]
                items["away_odd"] = odds[2]
            except AttributeError:
                items["home_odd"], items["draw_odd"], items["away_odd"] = ['-', '-', '-']

            self.database_append(cursor, items)
            #print(items)

    @staticmethod
    def get_the_data(driver):
        # GET THE HTML
        html = driver.execute_script('return document.documentElement.outerHTML;')

        # CLOSE THE BROWSER
        driver.close()

        # WORK WITH THE DATA
        soup = bs4.BeautifulSoup(html, 'html.parser')
        matches_one = soup.find_all(class_='tr_1')
        matches_two = soup.find_all(class_=re.compile('tr_0'))
        all_games = []
        all_games += [list(game) for game in matches_one]
        all_games += [list(game) for game in matches_two]
        return all_games

    @staticmethod
    def connect_the_database():
        # CONNECT THE DATABASE
        connector = sqlite3.connect('games-db')
        cursor = connector.cursor()
        cursor.execute("DROP TABLE IF EXISTS ValueBets")
        cursor.execute('CREATE TABLE ValueBets(date TEXT, time TEXT, home_team TEXT, away_team TEXT,'
                       ' home_prob DECIMAL, draw_prob DECIMAL, away_prob DECIMAL, prediction TEXT,'
                       ' odds_for_prediction REAL, home_odd REAL, draw_odd REAL, away_odd REAL, value_percent DECIMAL)')
        return connector, cursor

    @staticmethod
    def database_append(cursor, items):

        cursor.execute('INSERT INTO ValueBets(date, time, home_team, away_team, home_prob, draw_prob,'
                       ' away_prob, prediction, odds_for_prediction, home_odd, draw_odd,'
                       ' away_odd, value_percent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?)',
                       (items["date"], items["time"], items["home"], items["away"],
                        items["home_prob"], items["draw_prob"], items["away_prob"],
                        items["prediction"], items["odd_for_prediction"],
                        items["home_odd"], items["draw_odd"],
                        items["away_odd"], items["value_percent"]))


vb = ValueBets()
vb.scrape()