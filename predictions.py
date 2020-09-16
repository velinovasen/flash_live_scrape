import sqlite3
from selenium.webdriver import Chrome, ChromeOptions
import bs4
import re
from time import sleep


class Predictions:

    WEB_LINKS = {
        "football": 'https://www.forebet.com/en/top-football-tips-and-predictions'
    }
