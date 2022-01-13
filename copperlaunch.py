import json
from csv import DictWriter

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests as r
import time


class Twitter:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        self.number_of_page = 0;
        self.driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(self.driver, 30)
        action = ActionChains(self.driver)
        self.driver.get('https://twitter.com/search')


    def get_content(self,search):
        WebDriverWait(self.driver,30).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input.r-30o5oe")))
        search_fiald=self.driver.find_element(By.CSS_SELECTOR,'input.r-30o5oe')
        search_fiald.send_keys(search+" hotel")
        search_fiald.click()
        search_fiald.send_keys(Keys.RETURN)
        latest_butt=self.driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[2]/nav/div/div[2]/div/div[2]/a')
        latest_butt.click()
        # Get scroll height after first time page load
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(2)
            self.driver.implicitly_wait(30)
            twitte_list = self.driver.find_element(By.XPATH,
                                                   '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/section/div')
            print(twitte_list)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height




if __name__ == '__main__':
    twitter= Twitter();
    twitter.get_content("wazo")
