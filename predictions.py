import sqlite3
from selenium.webdriver.common.action_chains import ActionChains
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
        "both_teams": r'[t]\=\"(.{1,60})[ ][v][s][ ](.{1,60})\"[ ]',
        "date_and_time": r'\"\>(\d{2}\/\d{1,2}\/\d{4})[ ](\d{1,2}\:\d{1,2})\<\/',
        "probabilities": r'\>(\d{1,2})\<\/([t]|[b])',
        "prediction": r'[r]\"\>([A-z0-9])\<\/',
        "score_prediction": r'\"\>(\d{1,2}[ ]\-[ ]\d{1,2})\<\/',
        "average_goals": r'[y]\"\>(\d{1,3}\.\d{1,2})\<\/',
        "temperature": r'[s]\"\>(\d{1,2}.{1})\<\/',
        "odds_for_prediction": r'\;\"\>(\d{1,2}\.\d{1,2})\<\/',
        "all_odds": r'[n]\>(\d{1,3}\.\d{1,2})\<\/'
    }

    def connect_the_database(self):
        # CONNECT THE DATABASE
        connector = sqlite3.connect('games-db')
        cursor = connector.cursor()
        cursor.execute("DROP TABLE IF EXISTS Predictions")
        cursor.execute('CREATE TABLE Predictions(time TEXT, home_team TEXT, away_team TEXT,'
                       ' home_prob DECIMAL, draw_prob DECIMAL, away_prob DECIMAL, bet_sign DECIMAL,'
                       ' score_predict TEXT, avg_goals REAL, odds REAL, temp TEXT)')
        return connector, cursor

    def open_the_browsers(self):
        # OPEN THE WEBSITE AND WORK WITH IT
        options = ChromeOptions()
        options.headless = True  # IF YOU WANT TO SEE THE BROWSER -> FALSE
        driver = Chrome(options=options, executable_path='C://Windows/chromedriver.exe')
        driver_tomorrow = Chrome(options=options, executable_path='C://Windows/chromedriver.exe')
        driver.get(self.WEB_LINKS['football_today'])
        driver_tomorrow.get(self.WEB_LINKS['football_tomorrow'])
        sleep(3)
        return driver, driver_tomorrow

    def click_on_buttons(self, driver, driver_tomorrow):
        while True:
            try:
                sleep(3)
                driver.find_element_by_css_selector('#close-cc-bar').click()
                today_token = driver.find_element_by_css_selector('#mrows > td > span')
                ActionChains(driver).move_to_element(today_token).click(today_token).perform()

                driver_tomorrow.find_element_by_css_selector('#close-cc-bar').click()
                tomorrow_token = driver_tomorrow.find_element_by_css_selector('#mrows > td > span')
                ActionChains(driver_tomorrow).move_to_element(tomorrow_token).click(tomorrow_token).perform()
            except Exception:
                sleep(3)
                break

    def get_all_games(self, driver, driver_tomorrow):
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
        all_games += [list(game) for game in matches_one_today] + [list(game) for game in matches_two_today]
        all_games += [list(game) for game in matches_one_tomorrow] + [list(game) for game in matches_two_tomorrow]
        return all_games

    def clean_data(self, all_games):
        # SEARCH THE DATA WE NEED
        for game in all_games:
            items = {}

            # FIND THE TEAMS
            both_teams = re.search(self.REGEX["both_teams"], str(game))
            try:
                items['home_team'] = both_teams.group(1)
                items['away_team'] = both_teams.group(2)
                print(f"{items['home_team']} - {items['away_team']}")
            except AttributeError:
                continue

            # FIND THE TIME
            date_and_time = re.search(self.REGEX["date_and_time"], str(game))
            try:
                items['date'] = date_and_time.group(1)
                items['time'] = date_and_time.group(2)
                print(f"{items['date']} - {items['time']}")
            except AttributeError:
                pass

            # PROBABILITIES
            probabilities = re.findall(self.REGEX["probabilities"], str(game))
            items['home_prob'], items['draw_prob'], items['away_prob'] = probabilities[0][0], probabilities[1][0],\
                                                                         probabilities[2][0]
            print(f"{items['home_prob']} _ {items['draw_prob']} _ {items['away_prob']}")

            # PREDICTION SIGN
            items['prediction_sign'] = re.search(self.REGEX["prediction"], str(game)).group(1)
            print(f"{items['prediction_sign']}")

            # SCORE PREDICTION
            items['score_prediction'] = re.search(self.REGEX["score_prediction"], str(game)).group(1)
            print(f"{items['score_prediction']}")

            # FIND AVERAGE GOALS PER GAME
            items['average_goals'] = re.search(self.REGEX["average_goals"], str(game)).group(1)
            print(f"{items['average_goals']}")

            # GET THE WEATHER TEMPERATURE
            try:
                items['temperature'] = re.search(self.REGEX["temperature"], str(game)).group(1)
                print(items['temperature'])
            except AttributeError:
                pass

            # GET THE ODDS
            try:
                items['odds_for_prediction'] = re.search(self.REGEX["odds_for_prediction"], str(game)).group(1)
                all_odds_token = re.findall(self.REGEX["all_odds"], str(game))
                # IF YOU WANT TO TAKE THE LIVE ODDS (IF LIVE) -> THEY ARE AVAILABLE IN THE FULL all_odds_token
                items["home_odd"], items["draw_odd"], items["away_odd"] = all_odds_token[:3]
                print(f"---[{items['home_odd']} _ {items['draw_odd']} _ {items['away_odd']}]---")
                print(items['odds_for_prediction'])
            except AttributeError:
                pass


    def scrape(self):

        # CONNECT THE DATABASE
        connector, cursor = self.connect_the_database()

        # OPEN THE BROWSERS
        driver, driver_tomorrow = self.open_the_browsers()

        # PRESS [MORE] BUTTON ON THE BOTTOM UNTIL DISAPPEAR
        self.click_on_buttons(driver, driver_tomorrow)

        # GET ALL GAMES
        all_games = self.get_all_games(driver, driver_tomorrow)

        # CLEAN DATA
        self.clean_data(all_games)

        cursor.close()


scraper = Predictions()
scraper.scrape()
