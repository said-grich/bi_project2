from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import time


class BookingScript:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.headless=True
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe")
        self.domain = 'https://www.booking.com'
        self.driver.get('https://www.booking.com')

    def fill_form(self, search_argument):
        '''Finds all the input tags in form and makes a POST requests.'''
        search_field = self.driver.find_element_by_id('ss')
        search_field.send_keys(search_argument)
        # We look for the search button and click it
        self.driver.find_element_by_class_name('sb-searchbox__button') \
            .click()
        time.sleep(5)
        wait = WebDriverWait(self.driver, timeout=10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH,
                 '//*[@id="search_results_table"]/div[1]/div/div/div/div[5]/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a/div[1]')))
        self.driver.find_elements_by_xpath(
            '//*[@id="search_results_table"]/div[1]/div/div/div/div[5]/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/div/h3/a/div[1]')[
            0].click()

    def scrape_results(self, n_results):
        '''Returns the data from n_results amount of results.'''

        accommodations_urls = list()
        accommodations_data = list()

        for accomodation_title in self.driver.find_elements_by_class_name('sr-hotel__title'):
            accommodations_urls.append(accomodation_title.find_element_by_class_name(
                'hotel_name_link').get_attribute('href'))

        for url in range(0, n_results):
            if url == n_results:
                break
            url_data = self.scrape_accommodation_data(self.driver, accommodations_urls[url])
            accommodations_data.append(url_data)

        return accommodations_data

    def scrape_accommodation_data(self):
        '''Visits an accommodation page and extracts the data.'''
        accommodation_fields = dict()

        # Get the accommodation name
        self.driver.switch_to.active_element
        self.driver.switch_to.window(self.driver.window_handles[1])
        title = self.driver.find_element_by_xpath("//*[@id=\"breadcrumb\"]/ol/li[5]/div/div/h1");
        accommodation_fields['name'] = title.text
        # Get the accommodation score
        accommodation_fields['score'] = self.driver.find_element_by_xpath(
            "//*[@id=\"js--hp-gallery-scorecard\"]/a/div/div/div/div/div[1]").text

        # Get the accommodation location
        accommodation_fields['location'] = self.driver.find_element_by_id('showMap2') \
            .find_element_by_class_name('hp_address_subtitle').text

        # Get the most popular facilities
        accommodation_fields['popular_facilities'] = list()
        facilities = self.driver.find_element_by_class_name('hp_desc_important_facilities')

        for facility in facilities.find_elements_by_class_name('important_facility'):
            accommodation_fields['popular_facilities'].append(facility.text)
        self.driver.find_element_by_xpath('//*[@id="show_reviews_tab"]').click();
        self.driver.implicitly_wait(2);
        accommodation_fields['Categories_score'] = list();
        categories_list = self.driver.find_element_by_xpath("//*[@id=\"review_list_score\"]/div[4]/div/div/ul")
        i = 0;
        for child in categories_list.find_elements_by_tag_name('span'):
            if not child.text: continue;
            accommodation_fields['Categories_score'].append(child.text)
        accommodation_fields['comments'] = list();
        personne_comment = '';
        number_of_page = self.driver.find_element_by_xpath(
            '//*[@id="review_list_page_container"]/div[4]/div/div[1]/div/div[2]/div/div[7]/a/span[1]').text;
        number_of_page = int(number_of_page)
        myElem = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.pagenext')))
        comments_list = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"review_list_page_container\"]/ul")));
        li_list = comments_list.find_elements_by_tag_name("li");
        for i in range(6):
            try:
                time.sleep(1)
                myElem = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.pagenext')))
                comments_list = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id=\"review_list_page_container\"]/ul")));
                li_list = comments_list.find_elements_by_tag_name("li");
                for child in li_list:
                    for span in child.find_elements_by_tag_name("p"):
                        if not span.text: continue;
                        accommodation_fields['comments'].append(span.text)

                myElem.click()
                print
                "Page is ready!"
            except StaleElementReferenceException:
                print
                "Loading took too much time!"
        return accommodation_fields