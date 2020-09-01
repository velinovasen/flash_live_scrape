import sqlite3
from selenium.webdriver import Firefox, FirefoxOptions
import bs4
import re
from time import sleep
from games_scraper import Scraper

print('volume file')
# UPDATE THE DATABASE WITH THE MOST RECENT GAMES
games_scraper = Scraper()
games_scraper.scrape()


WEB_LINKS = {
    "football": "https://www.bahisanaliz14.com/avrupa-en-cok-oynanan-maclar/"
}

DAYS = {
    "Monday": "Pts,", "Tuesday": "Sal,", "Wednesday": "Çar,", "Thursday": "Per,",
    "Friday": "Cum,", "Saturday": "Cts,", "Sunday": "Pzr,"
}

#
#
#
# TO CONNECT THE DATABASE
#
#
#

# OPEN THE WEBSITE AND GET THE DATA
options = FirefoxOptions()
options.headless = True
driver = Firefox(options=options, executable_path='C://Windows/geckodriver.exe')
driver.get(WEB_LINKS["football"])
sleep(2)
html = driver.execute_script("return document.documentElement.outerHTML;")

# WORK WITH THE DATA AND GO THROUGH VOLUMES
soup = bs4.BeautifulSoup(html, 'html.parser')
matches = soup.find_all(class_=re.compile('IH2Satir'))
all_games = [list(game) for game in matches]
print('success')

driver.close()
