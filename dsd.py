from datetime import datetime
import sqlite3
from dateutil.parser import parse
import json
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import requests
import bs4
import re
from time import sleep


class TomorrowGames:
    WEB_LINKS = {"oddsportal": 'https://www.oddsportal.com/matches/soccer/20201019/'}

    REGEX = {
        "home_away_scheduled": r'(\/\"\>([A-z0-9].+)[ ]\-|[d]\"\>([A-z0-9].+)\<\/[s][p][a])[ ]([A-z0-9].{1,40})\<\/[a]',
        "time": r'[0]\"\>(\d{1,2}[:]\d{1,2})\<\/[t][d]',
        "odds": r'(\"\>|\=\")(\d{1,2}[.]\d{1,2})(\<\/[a]|\"[ ])',
        "result": r'([c][o][r][e]\"\>(\d{1,2}[:]\d{1,2})([ ][p][e][n]|\<\/[t][d])|[p][o][s][t][p])'
    }

    def open_the_browser(self):
        # OPEN THE BROWSER
        options = ChromeOptions()
        options.headless = True  # IF YOU WANT TO SEE THE BROWSER -> FALSE
        driver = Chrome(options=options, executable_path=ChromeDriverManager().install())

        driver.get(self.WEB_LINKS['oddsportal'])
        sleep(4)
        return driver

    def get_the_data(self, driver):
        # GET THE DATA
        html = driver.execute_script('return document.documentElement.outerHTML;')
        driver.close()
        soup = bs4.BeautifulSoup(html, 'html.parser')
        games = soup.find_all('tr')
        return games

    def clean_data(self, games):
        # CLEAN THE DATA
        for game in games:
            items = []
            # FIND THE TIME
            try:
                both_teams = re.search(self.REGEX["home_away_scheduled"], str(game))
                home_team = both_teams.group(2)
                away_team = both_teams.group(4)
                if 'Group' in away_team or 'III' in home_team or 'PFL' in home_team:
                    continue
                else:
                    time = re.search(self.REGEX["time"], str(game)).group(1)
                    try:
                        odds = re.findall(self.REGEX["odds"], str(game))
                        [home_odd, draw_odd, away_odd] = [odds[0][1], odds[2][1], odds[4][1]]
                        print(f"{time} _ {home_team} --- {away_team} __ {home_odd} {draw_odd} {away_odd}")

                    except ValueError:
                        print('Most likely, we got missing odds')
            except AttributeError:
                continue

