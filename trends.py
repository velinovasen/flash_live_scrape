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

    }

    def scrape(self):
        driver = self.open_the_browser()
        trends_today = self.get_the_data(driver)
        self.find_all_trends(trends_today) # TO DO !!!
        while self.click_button(driver):
            pass

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
        trends_today = soup.find_all(class_='contain_trends')
        [print(list(trend)) for trend in trends_today]
        return trends_today

    @staticmethod
    def click_button(driver):
        element = driver.find_element_by_css_selector('#body-wrapper > div:nth-child(2) > div:nth-child(3)'
                                                      ' > div:nth-child(31) > div:nth-child(41) > div >'
                                                      ' center:nth-child(13) > div > div > a:nth-child(14)')
        if element.get_attribute('href'):
            ActionChains(driver).move_to_element(element).click(element).perform()
            sleep(3)
            return True
        return False


scrp = Trends()
scrp.scrape()
