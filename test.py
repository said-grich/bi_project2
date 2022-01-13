import random
import re
import time
import pychrome
import requests as r
import json
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pandas import pd


class GoogleMap:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--remote-debugging-port=8000")
        #options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-notifications")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        self.proxy_list = [];
        self.randomIpformList = "";
        self.search_argument = ""
        self.target_url = []
        self.changeIpRequest();
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
        self.driver = webdriver.Chrome(chrome_options=options)
        self.list = []
        self.comment_number = 0;
        self.dev_tools = pychrome.Browser(url="http://localhost:8000")

        self.tab = self.dev_tools.list_tab()[-1]
        self.tab.start()
        start = time.time()

        self.driver.get(
            "https://www.google.com/maps/")
        print(int(time.time() - start))

    def output_on_start(self, **kwargs):
        self.list.append(kwargs['request']['url'])

    def output_on_end(**kwargs):
        print("FINISHED ", kwargs)

    def changeIpRequest(self):
        url = "https://proxylist.geonode.com/api/proxy-list"
        req = r.get(url);
        proxy_list1 = req.json();
        self.proxy_list=proxy_list1["data"];
        randomIpformList_tmp=random.choice(self.proxy_list);
        self.randomIpformList=randomIpformList_tmp["ip"]+":"+randomIpformList_tmp["port"]


    def goTopage(self, search_argument):
        time.sleep(10)
        self.search_argument = search_argument;
        search_field = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.ID, 'searchboxinput')))
        search_field.send_keys(search_argument)
        time.sleep(1)
        search_field.send_keys(Keys.RETURN)
        # We look for the search button and click it
        search_field.click();

        self.tab.call_method("Network.emulateNetworkConditions",
                             offline=False,
                             latency=100,
                             downloadThroughput=9375,
                             uploadThroughput=3125)

    def setLessnnerOnTab(self):
        time.sleep(5)
        self.tab.call_method("Network.enable", _timeout=20)
        self.tab.set_listener("Network.requestWillBeSent", self.output_on_start)
        start = time.time()
        time.sleep(10)
        rev_button=WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable,
                                                      (By.CSS_SELECTOR, 'button.Yr7JMd-pane-hSRGPd'));
        rev_button=self.driver.find_element(By.CSS_SELECTOR,"button.Yr7JMd-pane-hSRGPd")
        self.driver.execute_script("arguments[0].click();", rev_button)
        WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]')))
        r=self.driver.find_element(By.XPATH,'//*[@id="pane"]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[2]');
        text=r.text

        time.sleep(10)
        x = re.findall('[0-9]+', text)
        self.comment_number = int(str(x[0]) + str(x[1]))
        x = re.findall('[0-9]+', text)
        self.comment_number = int(str(x[0]) + str(x[1]))
        print(x)
        time.sleep(5)
        review = self.driver.find_element(By.CSS_SELECTOR, "div.id-content-container")
        webdriver.ActionChains(self.driver).move_to_element(review).perform()
        time.sleep(10)
        self.driver.execute_script(
            'document.getElementsByClassName("siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc")[0].scroll(0,500)')
        time.sleep(5)
        self.driver.execute_script(
            'document.getElementsByClassName("siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc")[0].scroll(0,1000)')
        time.sleep(30)
        print(int(time.time() - start))

        sub_url = "https://www.google.com/maps/preview/review/listentitiesreviews";

        for url in self.list:
            if sub_url in url:
                self.target_url.append(url);
        print(self.target_url)

        return self.target_url[0];

    def getCommentUsingUrl(self):
        url_fragmment = self.target_url[0].split('!')
        up_pages = url_fragmment[5];
        number_com_per_page = "2i100"
        url_part1 = url_fragmment[0] + "!" + url_fragmment[1] + "!" + url_fragmment[2] + "!" + url_fragmment[3] + "!" + \
                    url_fragmment[4] + "!"
        url_part2 = url_fragmment[7] + "!" + url_fragmment[8] + "!" + url_fragmment[9] + "!" + url_fragmment[10] + "!" + \
                    url_fragmment[11] + "!" + url_fragmment[12] + "!" + url_fragmment[13] + "!" + url_fragmment[
                        14] + "!" + url_fragmment[15] + "!" + url_fragmment[16]
        if len(url_fragmment)>16: print(url_fragmment[17]) ; url_part2=url_part2+"!"+url_fragmment[17]
        print(url_part1 + url_fragmment[5] + "!" + url_fragmment[6] + "!" + url_part2)
        list_date_text = [];
        for i in range(0, self.comment_number + 100, 100):
            up_pages = "1i" + str(i);
            new_url = url_part1 + up_pages + "!" + number_com_per_page + "!" + url_part2;
            req = r.get(new_url);
            print(req.status_code)
            data = req.text
            data = data.split('\n')[1];
            datajson = json.loads(data)
            list_comment = datajson[2];
            if list_comment:
                for i in range(len(list_comment)):
                    comment = dict()
                    comment["date"] = "";
                    comment["text"] = "";
                    date = list_comment[i][1];
                    text = list_comment[i][3]
                    comment["date"] = date;
                    comment["text"] = text;
                    list_date_text.append(comment);
            else:
                continue
            print("------------------------------------->" + str(len(list_date_text)))
        with open(self.search_argument + "GoogleMapApi.json", 'w') as f:
            json.dump(list_date_text, f)
        time.sleep(10)


if __name__ == '__main__':

    def lopOnHotles(search):
       try:
           test = GoogleMap();
           test.goTopage(search + " hotel morocco");
           test.setLessnnerOnTab();
           test.getCommentUsingUrl()
       finally:
           print(search+ "Done !")


    list_hotel = [ "savoy", "Palm plaza"]
    for ho in list_hotel:
        lopOnHotles(ho)
        time.sleep(60);

