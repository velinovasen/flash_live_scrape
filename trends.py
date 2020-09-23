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

        all_trends = self.get_the_trends(driver)

        for trend in all_trends:
            trend = str(trend)
            print(str(trend))
            clean_words = []
            open_sentence_tokens = trend.split('>')
            print(open_sentence_tokens)
            open_sentence = [x for x in open_sentence_tokens]
            print(open_sentence)
            for el in open_sentence:
                clean_words += el.split('<')[0]
            # print(len(clean_words))
            # print(clean_words)

        driver.close()

    def get_the_trends(self, driver):
        # NOW WE SCRAPE THE TRENDS ONLY FOR TODAY AND TOMORROW, BUT WE CAN EASILY ADD
        # OTHER DAYS(Weekend, Serie A, Premier League, etc.) BY JUST ADDING THEIR
        # LINKS INTO WEB_LINKS

        all_trends = []
        for link in self.WEB_LINKS:
            driver.get(link)
            sleep(3)
            final_href_token = driver.find_element_by_link_text('End').get_attribute('href')
            final_href = re.search(self.REGEX['find_pages'], final_href_token).group(1)
            current_page_href = 0
            base_href = link
            while current_page_href <= int(final_href):
                current_href = base_href + str(current_page_href)
                print(current_href)
                driver.get(current_href)
                sleep(2)
                html = driver.execute_script('return document.documentElement.outerHTML;')
                soup = bs4.BeautifulSoup(html, 'html.parser')
                trends_tokens = soup.find_all(class_='short_trends')
                all_trends += [list(trend) for trend in trends_tokens]

                current_page_href += 35
        [print(trend) for trend in all_trends]
        return all_trends

    def open_the_browser(self):
        options = ChromeOptions()
        options.headless = False
        driver = Chrome(options=options, executable_path='C://Windows/chromedriver.exe')
        sleep(2)
        return driver


scrp = Trends()
scrp.scrape()
