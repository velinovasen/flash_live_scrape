from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome, ChromeOptions
import bs4
import re
from time import sleep


class OddsPortal:
    WEB_LINKS = {
        "oddsportal": "https://www.oddsportal.com/matches/"
    }

    REGEX = {

    }

    options = ChromeOptions()
    options.headless = False
    driver = Chrome(options=options, executable_path='C://Windows/chromedriver.exe')
    driver.get(WEB_LINKS['oddsportal'])
    sleep(6)

    html = driver.execute_script('return document.documentElement.outerHTML;')
    driver.close()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    matches_today = soup.find_all(class_='table-main')
    print(matches_today)


scraper = OddsPortal()
