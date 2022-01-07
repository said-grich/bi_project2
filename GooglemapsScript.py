import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


class GoogleMapsScript:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
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
        """A method for scrolling the page."""

        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

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
        comment_list = self.driver.find_elements(By.CLASS_NAME,"Svr5cf")
        self.scroll_down()

        # for i in range(10):
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        #     self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight-100)")
        #     time.sleep(3)
        #     comment_list = self.driver.find_elements(By.CSS_SELECTOR, "div.Svr5cf.bKhjM")
        accommodation_fields['comments'] = list();
        actions = ActionChains(self.driver)
        htmlstring = self.driver.page_source
        afterstring = ""
        key1=actions.click(Keys.PAGE_DOWN);
        key1.perform()
        self.driver.quit();



if __name__ == '__main__':
    scriptboocking = GoogleMapsScript();
    scriptboocking.fill_form("wazo");
    accommodations_data=scriptboocking.scrape_accommodation_data()
    with open("google.json", 'w') as f:
        json.dump(accommodations_data, f)

