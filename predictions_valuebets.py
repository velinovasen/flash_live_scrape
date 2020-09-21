import sqlite3
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome, ChromeOptions
import bs4
import re
from time import sleep


class ValueBets:
    WEB_LINKS = {
        "football": "https://m.forebet.com/en/value-bets"
    }

    REGEX = {
        "home": r'[e][T][e][a][m]\"\>\<[s][p][a][n]\>(.{1,60})\<\/[s][p][a][n]\>\<\/',
        "away": r'[y][T][e][a][m]\"\>\<[s][p][a][n]\>(.{1,60})\<\/[s][p][a][n]\>\<\/[s]',
        "date_and_time": r'\"\>(\d{2}\/\d{1,2}\/\d{4})[ ](\d{1,2}\:\d{1,2})\<\/',
        "probabilities": r'\>(\d{1,2})\<\/([t]|[b])',
        "prediction": r'[t]\"\>([A-z0-9])\<\/',
        "odd_for_prediction": r'\;\"\>(\d{1,3}\.\d{1,2})\<\/',
        "value_percent": r'[b]\>(\d{1,3}\%)',
        "all_odds": r'[n]\>(\d{1,3}\.\d{1,2})\<\/',
    }

    def scrape(self):
    #     # OPEN THE BROWSER
    #     driver = self.open_the_browser()
    #
    #     # GET THE HTML DATA
    #     all_games = self.get_the_data(driver)

        # GET THE GAMES FROM THE DATA
        self.clean_data(self.get_the_data(self.open_the_browser()))

    def open_the_browser(self):
        options = ChromeOptions()
        options.headless = False  # -> FALSE IF YOU WANT TO SEE THE BROWSER BROWSING
        driver = Chrome(options=options, executable_path='C://Windows/chromedriver.exe')
        driver.get(self.WEB_LINKS["football"])
        sleep(3)
        #driver.find_element_by_css_selector('#close-cc-bar').click()
        return driver

    def get_the_data(self, driver):
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

    def clean_data(self, all_games):

        for game in all_games:
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
                items["home_odds"] = odds[0]
                items["draw_odds"] = odds[1]
                items["away_odds"] = odds[2]
            except AttributeError:
                pass

            print(items)



scpr = ValueBets()
scpr.scrape()