import sqlite3
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome, ChromeOptions
import bs4
import re
from time import sleep

from webdriver_manager.chrome import ChromeDriverManager


class Trends:
    WEB_LINKS = ['https://m.forebet.com/en/football-tips-and-predictions-for-today/stat-trends?start=',
                 'https://m.forebet.com/en/football-tips-and-predictions-for-tomorrow/stat-trends?start=']

    REGEX = {
        "find_pages": r'[r][t]\=(\d+)',
        "find_prediction": r'[P][r][e][d][i][c][t][i][o][n]\<\/[s][t][r][o][n][g]\>\:[ ](.{1,30})\<\/[p]\>\<'
    }

    def scrape(self):
        driver = self.open_the_browser()

        all_trends = self.get_the_trends(driver)

        driver.close()

    def get_the_trends(self, driver):
        # NOW WE SCRAPE THE TRENDS ONLY FOR TODAY AND TOMORROW, BUT WE CAN EASILY ADD
        # OTHER DAYS(Weekend, Serie A, Premier League, etc.) BY JUST ADDING THEIR
        # LINKS INTO WEB_LINKS

        full_trends_list = []
        all_events = []
        all_predictions = []
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
                all_events += [trend.text for trend in trends_tokens]
                current_page_href += 35


                # div_trends = soup.find_all(class_='contain_trends')
                # for div in div_trends:
                #     prediction = re.search(self.REGEX['find_prediction'], str(div))
                #     if prediction:
                #         all_predictions.append(prediction.group(1))
                # all_predictions = []
                # counter = 5
                # while counter < 100:
                #     try:
                #         selector = f'#body-wrapper > div:nth-child(2) > div:nth-child(3) > div:nth-child({counter}) > p'
                #         #selector2 = f'#body-wrapper > div:nth-child(2) > div:nth-child(3) > div:nth-child(21) > p'
                #         prediction_tokens = soup.select(selector)
                #         if 'Prediction' in str(prediction_tokens):
                #         #prediction_tokens2 = soup.select(selector2)
                #         #if prediction_tokens:
                #             all_predictions.append(prediction_tokens)
                #         # elif prediction_tokens2:
                #         #     all_predictions.append(prediction_tokens2)
                #
                #     except Exception:
                #         pass
                #     counter += 1
                #
                # print([ev for ev in all_predictions if all_predictions.index(ev) % 2 != 0])

        for event in all_events:
            print(event)
            all_trends = re.split(r'[a-z][A-Z]+', event)
            all_separators = re.finditer(r'[a-z][A-Z]+', event)
            counter = 0
            for match in all_separators:
                last_letter, first_letter = match.group(0)[0], match.group(0)[1]
                try:
                    all_trends[counter] += last_letter
                    all_trends[counter + 1] = first_letter + all_trends[counter + 1]
                except IndexError:
                    pass
                counter += 1
            full_trends_list += [all_trends]
        [print(game) for game in full_trends_list]
        return full_trends_list

    def open_the_browser(self):
        options = ChromeOptions()
        options.headless = False
        driver = Chrome(options=options, executable_path=ChromeDriverManager().install())
        sleep(2)
        return driver


scrp = Trends()
scrp.scrape()
