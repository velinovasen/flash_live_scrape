import bs4
from selenium.webdriver import Firefox, FirefoxOptions
import sqlite3
import re
from contextlib import suppress
from time import sleep


WEB_LINKS = {
    "flashscore": "https://www.soccer24.com/"
}

connector = sqlite3.connect('games-db')
cursor = connector.cursor()
cursor.execute('DROP TABLE IF EXISTS allGames')
cursor.execute('CREATE TABLE allGames(time TEXT, home_team TEXT, away_team TEXT,'
               ' home_odd REAL, draw_odd REAL, away_odd REAL, over_betting TEXT,'
               ' bet TEXT, amount REAL)')

options = FirefoxOptions()
options.headless = True
driver = Firefox(options=options, executable_path='C://Windows/geckodriver.exe')
driver.get(WEB_LINKS["flashscore"])

# while True:
#     with suppress(Exception):
#         driver.find_element_by_css_selector('.calendar__direction--tomorrow').click()
#         break

sleep(2)


html = driver.execute_script("return document.documentElement.outerHTML;")
soup = bs4.BeautifulSoup(html, 'html.parser')
matches = soup.find_all(class_=re.compile("event__match"))
# [print(match) for match in matches]
all_games = [list(game) for game in matches if 'event__match--scheduled' in str(game)]
[print(x) for x in all_games]

driver.close()
