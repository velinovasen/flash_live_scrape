import json
from json import dump, dumps

from selenium.webdriver import ChromeOptions, Chrome
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import sleep
import re
from datetime import datetime, timedelta, date


def get_yesterday_date(for_key=False):
    datetime.today().strftime('%Y-%m-%d')
    tomorrow_date = (datetime.today() - timedelta(hours=24)).strftime('%Y-%m-%d')
    if for_key:                                     # CHECK IF ITS FOR KEY IN THE JSON OR NOT
        return "-".join(tomorrow_date.split('-'))
    else:
        return "".join(tomorrow_date.split('-'))


class Results:
    WEB_LINKS = {
        "today": 'https://www.oddsportal.com/matches/',
        "yesterday": 'https://www.oddsportal.com/matches/soccer/' + get_yesterday_date(),
    }

    REGEX = {
        "score": r'[t][a][b][l][e]\-[s][c][o][r][e]\"\>(\d{1,2}\:\d{1,2})\<\/',
        "both_teams_draw": r'\/\"\>([A-z0-9].{1,40})[ ]\-[ ]([A-z0-9].{1,40})\<\/[a]',
        "home_won": r'[s][p][a][n][ ][c][l][a][s][s]\=\"[b][o][l][d]\"\>([A-z0-9].{1,40})\<\/[s][p][a][n]',
        "home_loosing": r'\/\"\>([A-z0-9].{1,40})[ ]\-[ ]',
        "away_winning": r'[c][l][a][s][s]\=\"[b][o][l][d]\"\>([A-z0-9].{1,40})\<\/[s][p]',
        "away_loosing": r'\<\/[s][p][a][n]\>[ ]\-[ ]([A-z0-9].{1,40})\<\/[a]',
        "time": r'[0]\"\>(\d{1,2}[:]\d{1,2})\<\/[t][d]',
        "odds": r'(\"\>|\=\")(\d{1,2}[.]\d{1,2})(\<\/[a]|\"[ ])',
        "result": r'([c][o][r][e]\"\>(\d{1,2}[:]\d{1,2})([ ][p][e][n]|\<\/[t][d])|[p][o][s][t][p])'
    }

    def scrape(self):
        all_data = {}
        for link in self.WEB_LINKS.keys():
            # OPEN THE BROWSER
            driver = self.open_the_browser(link)

            # GET THE DATA
            all_games = self.get_the_data(driver)

            # CLEAN DATA
            data = self.clean_data(all_games)

            if link == 'today':
                key = str(date.today())
            else:
                key = str(get_yesterday_date(for_key=True))

            all_data[key] = data
        return all_data

    def open_the_browser(self, link):
        # OPEN THE BROWSER
        options = ChromeOptions()
        options.headless = True  # IF YOU WANT TO SEE THE BROWSER -> FALSE
        driver = Chrome(options=options, executable_path=ChromeDriverManager().install())
        driver.get(self.WEB_LINKS[link])
        sleep(4)
        return driver

    def get_the_data(self, driver):
        # GET THE DATA
        html = driver.execute_script('return document.documentElement.outerHTML;')
        soup = BeautifulSoup(html, 'html.parser')
        driver.close()
        games = soup.find_all('tr')
        return games

    def clean_data(self, games):
        # CLEAN THE DATA
        the_bulk = {}
        for game in games:
            # print(game)
            score = re.search(self.REGEX['score'], str(game))
            try:
                if score:
                    score = score.group(1)
                    [home_score, away_score] = score.split(':')
                    home_team, away_team = '', ''
                    time = re.search(self.REGEX['time'], str(game)).group(1)

                    if home_score > away_score:
                        home_team = re.search(self.REGEX['home_won'], str(game)).group(1)
                        away_team = re.search(self.REGEX['away_loosing'], str(game)).group(1)
                        print(f'{home_team} {score} {away_team}')
                    elif home_score == away_score:
                        tokens = re.search(self.REGEX['both_teams_draw'], str(game))
                        home_team, away_team = tokens.group(1), tokens.group(2)
                        print(f'{home_team} {score} {away_team}')
                    else:
                        home_team = re.search(self.REGEX['home_loosing'], str(game)).group(1)
                        away_team = re.search(self.REGEX['away_winning'], str(game)).group(1)
                        print(f'{home_team} {score} {away_team}')

                    key = time + home_team
                    the_bulk[key] = score
            except Exception as e:
                print(e)

        return the_bulk


res = Results()
results_data = res.scrape()

print(results_data)

with open('oddsportal_data.json', 'r') as json_data:
    games = json.load(json_data)

print(games)

today_date = str(date.today())
yesterday_date = str(get_yesterday_date(for_key=True))

today_results = results_data[today_date]
yesterday_results = results_data[yesterday_date]
finished = []
for key in today_results.keys():
    try:
        tokens = today_results[key].split(':')
        home_sc, away_sc = int(tokens[0]), int(tokens[1])
        winner = ''
        if home_sc > away_sc:
            winner = 1
        elif home_sc < away_sc:
            winner = 2
        else:
            winner = 0

        games[today_date][key]['score'] = today_results[key]
        games[today_date][key]['status'] = 'finished'
        games[today_date][key]['winner'] = winner

        finished.append(games[today_date][key])

    except KeyError:
        pass

for key in yesterday_results.keys():
    try:
        tokens = yesterday_results[key].split(':')
        home_sc, away_sc = int(tokens[0]), int(tokens[1])
        winner = ''
        if home_sc > away_sc:
            winner = 1
        elif home_sc < away_sc:
            winner = 2
        else:
            winner = 0

        games[yesterday_date][key]['score'] = today_results[key]
        games[yesterday_date][key]['status'] = 'finished'
        games[yesterday_date][key]['winner'] = winner

        finished.append(games[yesterday_date][key])

    except KeyError:
        pass

print(games)
with open('oddsportal_data.json', 'w') as file:
    json.dump(games, file, indent=2)

