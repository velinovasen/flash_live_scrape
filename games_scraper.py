import bs4
from selenium.webdriver import Firefox, FirefoxOptions
import sqlite3
import re
from time import sleep


class Scraper:

    WEB_LINKS = {
        "flashscore": "https://www.soccer24.com/"
    }

    def scrape(self):
        # CONNECT THE DATABASE
        connector = sqlite3.connect('games-db')
        cursor = connector.cursor()
        cursor.execute('DROP TABLE IF EXISTS allGames')
        cursor.execute('CREATE TABLE allGames(time TEXT, home_team TEXT, away_team TEXT, home_odd REAL, draw_odd REAL, '
                       'away_odd REAL, top100 TEXT, home_amount REAL, draw_amount REAL, away_amount REAL)')

        # OPEN THE WEBSITE AND GET THE DATA
        options = FirefoxOptions()
        options.headless = True
        driver = Firefox(options=options, executable_path='C://Windows/geckodriver.exe')
        driver.get(self.WEB_LINKS["flashscore"])
        sleep(2)
        html = driver.execute_script("return document.documentElement.outerHTML;")

        # WORK WITH THE DATA AND GET THE GAMES
        soup = bs4.BeautifulSoup(html, 'html.parser')
        matches = soup.find_all(class_=re.compile("event__match"))
        all_games = [list(game) for game in matches if 'event__match--scheduled' in str(game)]

        # INSERT THE GAMES INTO THE DATABASE
        for game in all_games:
            game = game[1:]
            game.pop(3)
            items = {"time": "", "home": "", "away": "", "home_odd": "",
                     "draw_odd": "", "away_odd": ""}
            for element in game:
                if "event__time" in str(element):
                    pattern = r'(\d+[:]\d{2})'
                    time = re.search(pattern, str(element))
                    items["time"] = time.group()

                elif "participant--home" in str(element):
                    pattern = r'\"\>([A-z]+.+)\<\/'
                    home_team = re.search(pattern, str(element))
                    items["home"] = home_team.group(1)

                elif "participant--away" in str(element):
                    pattern = r'\"\>([A-z]+.+)\<\/'
                    away_team = re.search(pattern, str(element))
                    items["away"] = away_team.group(1)

                elif "o_1" in str(element):
                    pattern = r'\"\>(\d{1,2}\.\d{2})\<\/[s]'
                    try:
                        home_odd = re.search(pattern, str(element))
                        items["home_odd"] = home_odd.group(1)
                    except AttributeError:
                        items["home_odd"] = "1.00"

                elif "o_0" in str(element):
                    pattern = r'\"\>(\d{1,2}\.\d{2})\<\/[s]'
                    try:
                        draw_odd = re.search(pattern, str(element))
                        items["draw_odd"] = draw_odd.group(1)
                    except AttributeError:
                        items["draw_odd"] = "1.00"

                elif "o_2" in str(element):
                    pattern = r'\"\>(\d{1,2}\.\d{2})\<\/[s]'
                    try:
                        away_odd = re.search(pattern, str(element))
                        items["away_odd"] = away_odd.group(1)
                    except AttributeError:
                        items["away_odd"] = "1.00"
            cursor.execute('INSERT INTO allGames(time, home_team, away_team, home_odd, draw_odd, away_odd) '
                           'VALUES (?, ?, ?, ?, ?, ?)', (items["time"], items["home"], items["away"],
                                                         items["home_odd"], items["draw_odd"], items["away_odd"]))
            connector.commit()

        driver.close()