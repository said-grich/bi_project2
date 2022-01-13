import copy
import json
import os
import logging


import pychrome
from numpy import equal
from selenium import webdriver
from selenium.webdriver import ActionChains, DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import pandas as pd
import time


class GetHotll_list:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('https://www.booking.com/searchresults.fr.html?label=gog235jc-1DCAEoggI46AdIDVgDaIwBiAEBmAENuAEXyAEM2AED6AEB-AECiAIBqAIDuAKyu_KOBsACAdICJDc0M2MxODNjLWE3NzAtNGFmMi1iNTIxLTg4MGNjZjZjZDkxNtgCBOACAQ&sid=683fac077b0993bc1f289d9041519b98&aid=397594&lang=fr&sb=1&sb_lp=1&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.fr.html%3Faid%3D397594%3Blabel%3Dgog235jc-1DCAEoggI46AdIDVgDaIwBiAEBmAENuAEXyAEM2AED6AEB-AECiAIBqAIDuAKyu_KOBsACAdICJDc0M2MxODNjLWE3NzAtNGFmMi1iNTIxLTg4MGNjZjZjZDkxNtgCBOACAQ%3Bsid%3D683fac077b0993bc1f289d9041519b98%3Bclick_from_hp_logo%3D1%3Bsb_price_type%3Dtotal%3Bsrpvid%3D7c9c93600eb505de%26%3B&ss=Marrakech%2C+Maroc&is_ski_area=&checkin_year=&checkin_month=&checkout_year=&checkout_month=&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&dest_id=-38833&dest_type=city&search_pageview_id=53ad9247ed550219&search_selected=true&order=upsort_bh')
        self.driver.maximize_window()


    def getHotel_list(self):
        list=[];
        for i in range(40):
            time.sleep(5)
            h2_list = self.driver.find_elements(By.CSS_SELECTOR, "div.fde444d7ef._c445487e2");
            next_butt = self.driver.find_elements(By.CSS_SELECTOR, 'span._3ae5d40db._6c58bf014._4b9c5f3e8')
            time.sleep(5)
            for h2 in h2_list:
                list.append(h2.text);
            time.sleep(10)
            next_butt[1].click();
            return list;


if __name__ == '__main__':
    get_hotel=GetHotll_list()
    data=get_hotel.getHotel_list()
    with open("kech_hotels.json", 'w') as outfile:
        json.dump(data, outfile)


