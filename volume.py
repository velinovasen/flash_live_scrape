import sqlite3
from selenium.webdriver import Chrome, ChromeOptions
import bs4
from translate import translator
import re
from time import sleep
import datetime
from games_scraper import Scraper


WEB_LINKS = {
    "football": "https://www.bahisanaliz14.com/avrupa-en-cok-oynanan-maclar/"
}


DAYS = {
    "Monday": "Pts,", "Tuesday": "Sal,", "Wednesday": "Çar,", "Thursday": "Per,",
    "Friday": "Cum,", "Saturday": "Cts,", "Sunday": "Pzr,"
}
now = datetime.datetime.now().strftime("%A")
today_tr = DAYS[now]


# UPDATE THE DATABASE WITH THE MOST RECENT GAMES
# games_scraper = Scraper()
# games_scraper.scrape()



#
#
#
# TO CONNECT THE DATABASE
#
#
#

# OPEN THE WEBSITE AND GET THE DATA
options = ChromeOptions()
options.headless = False
options.add_argument("--lang=en")
driver = Chrome(executable_path='C://Windows/chromedriver.exe', options=options)
driver.get(WEB_LINKS["football"])
sleep(2)
html = driver.execute_script("return document.documentElement.outerHTML;")

# WORK WITH THE DATA AND GO THROUGH VOLUMES
soup = bs4.BeautifulSoup(html, 'html.parser')
matches = soup.find_all(class_=re.compile('IH2Satir'))

for game in matches:
    elements = list(game)
    if today_tr in str(elements[1]):
        # GET THE TEAMS
        tokens = str(elements[2])
        teams_pattern = r'[o][n][g]\>(.+)\<\/[s][t][r]'
        teams = re.search(teams_pattern, tokens)
        home_team, away_team = teams.group(1).split(' - ')

        #GET THE BET POSITION
        position_token = str(elements[3])
        position_pattern = r'[s][p][a][n]\>[ ](\d{1})\<\/[d][i]'
        position = re.search(position_pattern, position_token)
        final_bet = position.group(1)

        # GET THE AMOUNT
        amount_token = str(elements[5])
        amount_pattern = r'[o][n][g]\>(.+)[ ][A-z]+'
        amount = re.search(amount_pattern, amount_token)
        print(amount.group(1))

driver.close()
