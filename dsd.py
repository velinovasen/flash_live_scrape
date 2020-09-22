import sqlite3
import requests
import bs4
import re
from time import sleep

driver = requests.get('https://www.bet365.com/#/IP/B1')
print(driver.status_code)
sleep(3)
# html = driver.execute_script('return document.documentElement.outerHTML;')
# sleep(20)
# driver.close()
# soup = bs4.BeautifulSoup(html, 'html.parser')

print(driver.content)
