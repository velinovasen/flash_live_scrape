import sqlite3
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome, ChromeOptions
import bs4
import re
from time import sleep


class Trends:
    WEB_LINKS = {
        "trends": "https://www.forebet.com/en/trends"
    }

    REGEX = {
        "find_pages": '[r][t]\=(\d+)'
    }

    def scrape(self):
        driver = self.open_the_browser()

        #trends_today = self.get_the_data(driver)

        all_trends_today = []

        final_href_token = driver.find_element_by_link_text('End').get_attribute('href')
        final_href = re.search(self.REGEX['find_pages'], final_href_token).group(1)
        current_page_href = 0
        base_href = 'https://www.forebet.com/en/trends?start='
        while current_page_href <= int(final_href):
            current_href = base_href + str(current_page_href)
            print(current_href)
            driver.get(current_href)
            html = driver.execute_script('return document.documentElement.outerHTML;')
            soup = bs4.BeautifulSoup(html, 'html.parser')
            trends_tokens = soup.find_all(class_='short_trends')
            all_trends_today += [print(list(trend)) for trend in trends_tokens]

            current_page_href += 35
        driver.close()

    def open_the_browser(self):
        options = ChromeOptions()
        options.headless = False
        driver = Chrome(options=options, executable_path='C://Windows/chromedriver.exe')
        driver.get(self.WEB_LINKS['trends'])
        sleep(5)
        return driver

    @staticmethod
    def find_all_trends(trends_today):
        pass

    @staticmethod
    def get_the_data(driver):
        html = driver.execute_script('return document.documentElement.outerHTML;')
        soup = bs4.BeautifulSoup(html, 'html.parser')
        trends_today = soup.find_all(class_='short_trends')
        [print(list(trend)) for trend in trends_today]
        return trends_today

    @staticmethod
    def click_button(driver):
        try:
            element = driver.find_element_by_link_text('Next')
            return element
        except Exception:
            return False

scrp = Trends()
scrp.scrape()
