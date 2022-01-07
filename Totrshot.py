import json
from csv import DictWriter

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests as r
import time


class Trustpilot:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        self.number_of_page = 0;
        self.driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(self.driver, 30)
        action = ActionChains(self.driver)
        self.domain = 'https://uk.trustpilot.com/review/www.little-mouse.co.uk?page=3'
        self.driver.get('https://uk.trustpilot.com/review/www.little-mouse.co.uk?page=3')
        self.revews_url_part1 = "https://uk.trustpilot.com/_next/data/businessunitprofile-consumersite-2005/review/www.little-mouse.co.uk.json?page=";
        self.revews_url_part2 = "&businessUnit=www.little-mouse.co.uk";
        self.finel_list = []

    def get_content(self):
        accept_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")));
        accept_button.click();
        last_page = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.NAME, "pagination-button-last")));
        self.number_of_page = int(last_page.text);
        print(last_page.text)
        page1_url = "https://uk.trustpilot.com/_next/data/businessunitprofile-consumersite-2005/review/www.little-mouse.co.uk.json?businessUnit=www.little-mouse.co.uk"
        for i in range(1, self.number_of_page):
            if i == 1:
                rq = r.get(page1_url);
                data = rq.json();
                data = data["pageProps"]["reviews"]
                for rev in data:
                    self.finel_list.append({"Name": rev['consumer']['displayName'], "Review title": rev['title'],
                                            "Review content": rev['text'],
                                            "Date of review": rev['dates']['publishedDate']})

            else:
                rq = r.get(self.revews_url_part1 + str(i) + self.revews_url_part2);
                data = rq.json();
                data = data["pageProps"]["reviews"]
                for rev in data:
                    self.finel_list.append(
                        {"Name": rev['consumer']['displayName'], "Review title": rev['title'],
                         "Review content": rev['text'],
                         "Date of review": rev['dates']['publishedDate']})
        df = pd.DataFrame.from_dict(self.finel_list)
        print(df)
        df.to_excel('Tottshot.xlsx')


if __name__ == '__main__':
    trustpilot = Trustpilot();
    trustpilot.get_content();
