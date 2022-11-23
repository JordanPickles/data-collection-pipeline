from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time

class CoinMarketScraper:
    #Initialising the CoinMarketScraper Class, passing the parameters 
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://coinmarketcap.com/'
        self.page_links_list = [self.url]
        self.coin_link_list = []
        self.price_list = []
        self.market_cap_list = []
        self.coin_name_list = []
        self.daily_volume_list = []
        self.daily_low_list = []
        self.daily_high_list = []
        self.all_time_high_list = []
        self.data_dict = {}


    def load_page(self):
        page = self.driver.get(self.url)
        try:
            pop_up_button = self.driver.find_element(by=By.XPATH, value = '/html/body/div[3]/div/div/div/div/button[2]')
            pop_up_button.click()
        except NoSuchElementException:
            pass

    def get_page_links(self):
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        page_number_bar = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[1]/div[6]/div/ul')
        li_tags = page_number_bar.find_elements(by=By.XPATH, value = '//*[@class="page"]')
        for link in li_tags:
            a_tags = link.find_element(by=By.TAG_NAME, value = 'a')
            link = a_tags.get_attribute('href')
            self.page_links_list.append(link)

    def page_itteration(self):
        for page in self.page_links_list[:2]:
            self.driver.get(page)
            self.get_coin_links()

    def get_coin_links(self):
        delay = 20
        link_list = []
        ignored_exceptions= (StaleElementReferenceException)
        WebDriverWait(self.driver, delay,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[1]/div[5]/table')))
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        table = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[1]/div[5]/table/tbody')
        table_list = table.find_elements(by=By.XPATH, value = './tr')
        for coin in table_list:
            a_tag = coin.find_element(by=By.TAG_NAME, value = 'a')
            link = a_tag.get_attribute('href')
            link_list.append(link)
        self.coin_link_list.extend(link_list)

    

    def get_coin_name(self):
        try:
            coin_name = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/h2/span/span').text 
        except NoSuchElementException:
            try:
                coin_name = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[3]/div/div[1]/div[1]/h2/span/span').text  
            except NoSuchElementException:
                coin_name = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]/h2/span/span').text
        self.coin_name_list.append(coin_name)

    def get_coin_price(self):
        try:
            price = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[3]/div/div[2]/section/div/div[1]/table/tbody/tr[1]/td').text 
        except NoSuchElementException:
            try:
                price = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[3]/div/div[2]/div[1]/div/span').text 
            except:
                price = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div/span').text
        self.price_list.append(price)

    def get_coin_market_cap(self):
        try:
            market_cap = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[3]/div/div[2]/section/div/div[2]/table/tbody/tr[1]/td/span').text
        except NoSuchElementException:
            try:
                market_cap = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[3]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div').text 
            except NoSuchElementException:
                market_cap = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div').text
        self.market_cap_list.append(market_cap)
    
    def get_coin_daily_volume(self):
        try:
            daily_volume = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[3]/div/div[2]/section/div/div[1]/table/tbody/tr[4]/td/span').text
        except NoSuchElementException:
            try:
                daily_volume = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[3]/div/div[3]/div[1]/div[3]/div[1]/div[2]/div').text
            except NoSuchElementException:
                daily_volume = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/div[3]/div[1]/div[2]/div').text
        self.daily_volume_list.append(daily_volume)

    def get_coin_daily_low(self):
        try:
            daily_low = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[3]/div/div[2]/div[3]/div[1]/span[2]/span').text
        except NoSuchElementException:
            try:
                daily_low = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[3]/div/div[2]/div[3]/div[1]/span[2]/span').text
            except NoSuchElementException:
                daily_low = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[3]/div[1]/span[2]/span').text
        self.daily_low_list.append(daily_low)

    def get_coin_daily_high(self):
        try:
            daily_high = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div[3]/div[3]/span[2]/span').text
        except NoSuchElementException:
            try: 
                daily_high = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[3]/div/div[2]/div[3]/div[3]/span[2]/span').text
            except NoSuchElementException:
                daily_high = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[3]/div/div[2]/div[3]/div[3]/span[2]/span').text
        self.daily_high_list.append(daily_high)


                
    def get_data(self):
        delay = 20  
        for coin in self.coin_link_list:
            self.driver.get(coin)
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]')))
            try:
                self.get_coin_name()
                self.get_coin_price()
                self.get_coin_market_cap()
                self.get_coin_daily_volume()
                self.get_coin_daily_low()
                self.get_coin_daily_high()

            except NoSuchElementException:
                price3 = "NA"
                self.price_list.append(price3)
                market_cap3 = "NA"
                self.market_cap_list.append(market_cap3)
                daily_volume3 = "NA"
                self.daily_volume_list.append(daily_volume3)



    def dict_data_collect(self):
        self.data_dict = {"Coin name": self.coin_name_list, "Price": self.price_list, "Market Cap": self.market_cap_list, "24hr Volume": self.daily_volume_list, "24hr low": self.daily_low_list, "24hr High": self.daily_high_list}
        print(self.data_dict)



if __name__ == '__main__':
    scraper = CoinMarketScraper() #Creates an instance of the scraper class
    scraper.load_page()
    scraper.get_page_links()
    scraper.page_itteration()
    scraper.get_data()
    scraper.dict_data_collect()
