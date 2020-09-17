import sqlite3
from selenium.webdriver import Chrome, ChromeOptions
import bs4
import re
from time import sleep


class Predictions:

    WEB_LINKS = {
        "football": 'https://www.forebet.com/en/top-football-tips-and-predictions'
    }

    def scrape(self):
        # TO DO - CONNECT THE DATABASE
        connector = sqlite3.connect('games-db')
        cursor = connector.cursor()
        cursor.execute("DROP TABLE IF EXISTS Predictions")
        cursor.execute('CREATE TABLE Predictions(time TEXT, home_team TEXT, away_team TEXT,'
                       ' home_prob DECIMAL, draw_prob DECIMAL, away_prob DECIMAL, bet_sign DECIMAL,'
                       ' score_predict TEXT, avg_goals REAL, odds REAL, temp TEXT)')