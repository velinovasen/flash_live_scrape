import sqlite3
from selenium.webdriver import Chrome, ChromeOptions
import bs4
import re
from time import sleep
import datetime


class Volume:

    WEB_LINKS = {
        "football": "https://www.bahisanaliz14.com/avrupa-en-cok-oynanan-maclar/"
    }

    def get_volume(self):

        # CONNECTING THE DATABASE
        connector = sqlite3.connect('games-db')
        cursor = connector.cursor()
        cursor.execute('DROP TABLE IF EXISTS VolumeGames')
        cursor.execute('CREATE TABLE VolumeGames(day TEXT, time TEXT, home_team TEXT,'
                       ' away_team TEXT, bet_sign INTEGER, odd REAL, volume REAL)')

        days_numbered = {
            "Pts": "Monday", "Sal": "Tuesday", "Çar": "Wednesday", "Per": "Thursday",
            "Cum": "Friday", "Cts": "Saturday", "Pzr": "Sunday"
        }

        # OPEN THE WEBSITE AND GET THE DATA
        options = ChromeOptions()
        options.headless = True
        options.add_argument("--lang=en")
        driver = Chrome(executable_path='C://Windows/chromedriver.exe', options=options)
        driver.get(self.WEB_LINKS["football"])
        sleep(2)
        html = driver.execute_script("return document.documentElement.outerHTML;")
        driver.close()

        # WORK WITH THE DATA AND GO THROUGH VOLUMES
        soup = bs4.BeautifulSoup(html, 'html.parser')
        matches = soup.find_all(class_=re.compile('IH2Satir'))

        for game in matches:
            elements = list(game)
            #print(elements)

            # GET THE TIME
            time_tokens = str(elements[1])
            time_pattern = r'[ ](\d+[:]\d+)\<\/'
            day_pattern = r'\;\"\>(.{3})\,'
            time_raw = re.search(time_pattern, time_tokens)
            day_raw = re.search(day_pattern, time_tokens)
            time = time_raw.group(1)
            day = days_numbered[day_raw.group(1)]
            #print(days_numbered[day])

            # GET THE TEAMS
            team_tokens = str(elements[2])
            teams_pattern = r'[o][n][g]\>(.+)\<\/[s][t][r]'
            teams = re.search(teams_pattern, team_tokens)
            home_team, away_team = teams.group(1).split(' - ')

            # GET THE BET POSITION
            position_token = str(elements[3])
            position_pattern = r'[s][p][a][n]\>[ ](\d{1})\<\/[d][i]'
            position = re.search(position_pattern, position_token)
            final_bet = position.group(1)

            # GET THE ODD
            odds_token = str(elements[4])
            odds_pattern = r'[a][n]\>(\d+\.\d+)\<\/'
            odds_raw = re.search(odds_pattern, odds_token)
            odds = odds_raw.group(1)

            # GET THE AMOUNT
            amount_token = str(elements[5])
            amount_pattern = r'[o][n][g]\>(.+)[ ][A-z]+'
            amount = re.search(amount_pattern, amount_token)
            total_amount = amount.group(1)

            cursor.execute('INSERT INTO VolumeGames(day, time, home_team, away_team, bet_sign,'
                           ' odd, volume) VALUES (?, ?, ?, ?, ?, ?, ?)',
                           (day, time, home_team, away_team, final_bet, odds, total_amount))
        connector.commit()
        connector.close()


scraper = Volume()
scraper.get_volume()