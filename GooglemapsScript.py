import json

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


class GoogleMapsScript:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.domain = ''
        self.driver.get(
            'https://www.google.com/travel/?dest_src=ut&tcfs=UgA&ved=2ahUKEwjEuq2jkvv0AhVy_9UKHYYVCGAQyJABegQIABAQ&ictx=2')

    def fill_form(self, search_argument):
        '''Finds all the input tags in form and makes a POST requests.'''
        search_field = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, 'oA4zhb')))
        search_field.send_keys(search_argument)
        time.sleep(1)
        search_field.send_keys(Keys.RETURN)

        # We look for the search button and click it
        search_field.click();

    def scroll_down(self):
        scroll_pause_time = 1  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
        screen_height = self.driver.execute_script("return window.screen.height;")  # get the screen height of the web
        i = 1

        while True:
            # scroll one screen height each time
            self.driver.execute_script(
                "window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
            i += 1
            time.sleep(scroll_pause_time)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break

    def scrape_accommodation_data(self):
        '''Visits an accommodation page and extracts the data.'''
        accommodation_fields = dict()
        # Get the accommodation name
        title = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.fZscne")));
        accommodation_fields['name'] = title.text
        score = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.iDqPh")));
        accommodation_fields['score'] = score.text
        location = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.K4nuhf")));
        accommodation_fields['location'] = location.text
        accommodation_fields['popular_facilities'] = list()
        facilities = self.driver.find_element(By.CSS_SELECTOR, 'ul.ZxecAf')

        for facility in facilities.find_elements_by_tag_name('li'):
            accommodation_fields['popular_facilities'].append(facility.text)
            print(facility.text);
        self.driver.find_element(By.ID, "reviews").click()
        time.sleep(4)
        for i in range(10): self.scroll_down();

        accommodation_fields['comments'] = list();

        comment_list = self.driver.find_element(By.CSS_SELECTOR, "div.RJysl").find_elements(By.CSS_SELECTOR,
                                                                                            "div.kVathc");
        for comment in comment_list:
            accommodation_fields['comments'].append(comment.text)
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.PAGE_UP)
        self.driver.quit();
        return accommodation_fields


if __name__ == '__main__':
    scriptboocking = GoogleMapsScript();
    scriptboocking.fill_form("wazo");
    accommodations_data=scriptboocking.scrape_accommodation_data()
    with open("google.json", 'w') as f:
        json.dump(accommodations_data, f)

