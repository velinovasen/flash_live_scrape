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
        cursor.execute('CREATE TABLE VolumeGames(time TEXT, home_team TEXT, '
                       'away_team TEXT, bet_sign INTEGER, odd REAL, volume REAL)')

        days_numbered = {
            1: "Pts,", 2: "Sal,", 3: "Çar,", 4: "Per,",
            5: "Cum,", 6: "Cts,", 7: "Pzr,"
        }

        days = {
            "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4,
            "Friday": 5, "Saturday": 6, "Sunday": 7
        }
        now = datetime.datetime.now().strftime("%A")
        today_tr = days_numbered[days[now]]
        tomorrow_tr = days_numbered[days[now] + 1]

        # TO ADD A FUNCTION THAT TAKES THE NEXT DAY TOO
        # WE WANT TO BE ABLE TO CHECK FOR TODAY AND TOMORROWS VALUES

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
            if today_tr or tomorrow_tr in str(elements[1]):
                # GET THE TIME
                time_tokens = str(elements[1])
                time_pattern = r'[ ](\d+[:]\d+)\<\/'
                time_raw = re.search(time_pattern, time_tokens)
                time = time_raw.group(1)

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

                cursor.execute('INSERT INTO VolumeGames(time, home_team, away_team, bet_sign,'
                               ' odd, volume) VALUES (?, ?, ?, ?, ?, ?)',
                               (time, home_team, away_team, final_bet, odds, total_amount))
        connector.commit()
        connector.close()
