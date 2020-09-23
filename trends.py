import sqlite3
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome, ChromeOptions
import bs4
import re
from time import sleep


class Trends:
    WEB_LINKS = ['https://m.forebet.com/en/football-tips-and-predictions-for-today/stat-trends?start=',
                 'https://m.forebet.com/en/football-tips-and-predictions-for-tomorrow/stat-trends?start=']

    REGEX = {
        "find_pages": '[r][t]\=(\d+)'
    }

    def scrape(self):
        driver = self.open_the_browser()

        all_trends_today = []
        for link in self.WEB_LINKS:
            driver.get(link)
            sleep(3)
            final_href_token = driver.find_element_by_link_text('End').get_attribute('href')
            final_href = re.search(self.REGEX['find_pages'], final_href_token).group(1)
            current_page_href = 0
            base_href = 'https://m.forebet.com/en/football-tips-and-predictions-for-today/stat-trends?start='
            while current_page_href <= int(final_href):
                current_href = base_href + str(current_page_href)
                print(current_href)
                driver.get(current_href)
                html = driver.execute_script('return document.documentElement.outerHTML;')
                soup = bs4.BeautifulSoup(html, 'html.parser')
                trends_tokens = soup.find_all(class_='short_trends')
                all_trends_today += [list(trend) for trend in trends_tokens]

                current_page_href += 35
            [print(trend) for trend in all_trends_today]
        driver.close()

    def open_the_browser(self):
        options = ChromeOptions()
        options.headless = False
        driver = Chrome(options=options, executable_path='C://Windows/chromedriver.exe')
        sleep(2)
        return driver


scrp = Trends()
scrp.scrape()
