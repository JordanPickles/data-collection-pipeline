
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException


import time
from datetime import datetime
import json
import os
import requests


class CoinMarketScraper:
    """This class automates the coinmarketcap.com and navigates through the webpage to collect desired data regarding each cryptocurrency coin within the desired page range"""     
    
    def __init__(self):
        """
        This method initialises the class and passes the following attributes.
        ----------------------------------------------------------------------
        chrome_options:Variable
            Provides a variable to store the arguments passed into the chromedriver

        driver: WebDriver.Chrome()
            This webdriver is used to load and naviagte the webpage allowing the data to be collected
        
        url: string
            The url for the coinmarketcap.com landing page

        page_links_list: List
            A list for all of the pages of the webpage in which cryptocurrencies are presented. From here the next page etc url's are stored. 
            This allows for urls for all the individual coins to be collected from each page

        coin_link_list: List
            A list of all the cryptocurrency coin page links whoch can then be iterated through to collect data on each coin
        
        coin_data: List
            A list of all of the dictionaries collected on each cryptocurrency coin page
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-setuid-sandbox") 
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = chrome_options)
        self.url = 'https://coinmarketcap.com/'
        self.page_links_list = [self.url]
        self.coin_link_list = []
        self.coin_data = []


    def load_webpage(self) -> str: 
        """This public emthod loads the webpage using chromedriver"""
        try:
            self.driver.get(self.url)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body')))
            return 'The page was loaded successfully'
        except TimeoutException:
            "The page was not loaded successfully"

    
    def create_list_of_webpage_links(self):
        """
        This public method collates links for following pages on coinmarketcap.com and appends them to a list.
        ------------------------------------------------------------------------------------------------------
        page_number_bar: HTML Tree
            Locates the HTML tree in which the page urls are found
        li_tags: HTML tags
            Locates all of the li tags stored witin the page_number_bar tree. Within these tags, all of the page urls are stored.
        """  
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(3)
        
        page_number_bar = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[6]/div[1]/div/ul') 
        li_tags = page_number_bar.find_elements(by=By.XPATH, value = '//*[@class="page"]') 
        
        for link in li_tags: 
            link = link.find_element(by=By.TAG_NAME, value = 'a').get_attribute('href')
            self.page_links_list.append(link)
        
        
    def create_list_of_coin_links(self):
        """
        This public method scrapes the page provided for the cryptocurrency coin links that are stored on that page. The links on each page are added to the self.coin_link_list
        --------------------------------------------------------------------------------------------------------
        link_list: List
            Local list to this method used store the coin page urls on each page before being extended to the bigger self.coin_link_list

        table: HTML Tree
            Locates the HTML tree containing the table in which urls are stored

        table_rows: HTML table rows
            Locates the table rows containing the information for each coin, including the page urls for each coin

        link: String
            Extracts the page link from the table row
        """ 
        link_list = [] 
        ignored_exceptions= (StaleElementReferenceException)
        WebDriverWait(self.driver, 20,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]'))) 

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(2)
        table = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody') 
        table_rows = table.find_elements(by=By.XPATH, value = './tr') 
        for coin in table_rows: 
            link = coin.find_element(by=By.TAG_NAME, value = 'a').get_attribute('href') 
            link_list.append(link) 
        self.coin_link_list.extend(link_list) 
        

    def webpage_links_iteration(self): 
        """This method iterates through the page_links_list created in the create_list_of_webpage_links() method and calls the create_list_of_coin_links() after each new page is loaded."""

        for page in self.page_links_list[:2]: #
            self.driver.get(page)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body'))) 
            self.create_list_of_coin_links()
        
     
    def __scrape_webpage_data(self, coin_link) -> dict: 
        """
        This private method scrapes the data for the desired metric for the coin page loaded. The data is added to the self.data_dict.
        ---------------------------------------------------------------------------------------------------------------------
        coin_dict: Dict
            Provides an empty local dictionary for each coin link provided, the data collected for each coin is stored here, once the dictionary is completed, it is added to the self.coin_data list.
        Name: String
            Cryptocurrency Coin Name
        Price: String
            Cryptocurrency Coin Price
        Market cap: String
            Crytpocurrency Coin Market Cap
        24 Hour trading volume: String
            Cryptocurrency Coin 24 Hour Trading Volume
        24 Hour price low: String
            Cryptocurrency Coin 24 Hour Price Low
        24 Hour pricee high: String
            Cryptocurrency Coin 24 Hour Price Low
        Image url: String
            Cyrptocurrency Coin Image URL's
        Timestamp: String
            Timestamp of when Cryptocurrency Coin Data is Scraped

        Returns: coin_dict is returned at the end of the method containing the data scraped from each Cryptocurrency Coin page.
        """
        coin_dict = {}
        self.driver.get(coin_link)
        try:
            pop_up_button = self.driver.find_element(by=By.XPATH, value = '/html/body/div[3]/div/div/div/div/button[2]')
            pop_up_button.click()
        except NoSuchElementException:
            pass
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@class="main-content"]')))

        coin_name = self.driver.find_element(by=By.XPATH, value = '//*[@class="sc-aba8b85a-0 gmYubB h1"]/span/span').text
        price = self.driver.find_element(by=By.XPATH, value = '//*[@class="sc-aef7b723-0 dDQUel priceTitle"]/div').text          
        market_cap = self.driver.find_element(by=By.XPATH, value = '//*[@class="sc-aef7b723-0 eslelo statsSection"]/div[1]/div[1]/div[1]/div[2]/div').text
        daily_volume = self.driver.find_element(by=By.XPATH, value = '//*[@class="sc-aef7b723-0 eslelo statsSection"]/div[1]/div[3]/div[1]/div[2]/div').text
        daily_low = self.driver.find_element(by=By.XPATH, value = '//*[@class="sc-aef7b723-0 kIYhSM"]/span/span').text
        daily_high = self.driver.find_element(by=By.XPATH, value = '//*[@class = "sc-aef7b723-0 gjeJMv"]/span/span').text
        str_time_stamp = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime("%d-%m-%Y, %H:%M:%S")
        coin_img_src = self.driver.find_element(by=By.TAG_NAME, value = 'img').get_attribute('src')
        self.__download_image_from_webpage(coin_img_src, f"raw_data/images/{coin_name}_{str_time_stamp}.jpg")
                
        coin_dict['Name'] = coin_name
        coin_dict['Price'] = price
        coin_dict['Market Cap'] = market_cap
        coin_dict['24hr Trading Volume'] = daily_volume
        coin_dict['24hr Price Low'] = daily_low
        coin_dict['24hr Price High'] = daily_high
        coin_dict['Image'] = coin_img_src
        coin_dict['Timestamp'] = str_time_stamp
        
        return coin_dict
    
    def __download_image_from_webpage(self, coin_img_src, fp):

        """
        This private method is called during the scrape_webpage_data() method. This method downloads the image from the the image URL and stores this locally using the os context manager
        -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        coin_img_data: .jpg file
            Downloads the image using requests.get
        """
        if os.path.exists("raw_data/images") == False: 
            os.makedirs("raw_data/images") 
        coin_img_data = requests.get(coin_img_src).content 

        with open(fp, 'wb') as handler: 
            handler.write(coin_img_data) 


    def coin_link_iteration(self):
        """This public method iterates through each coin link collected in the create_list_of_coin_links() and calls the private method, scrape_webpage_data() methods. The data from each coin link is appended to the self.coin_data list and this list is placed into a .json file and stored locally."""

        for coin_link in self.coin_link_list: 
            self.coin_data.append(self.__scrape_webpage_data(coin_link)) 
            
        if os.path.exists("raw_data") == False: 
            os.makedirs("raw_data") 
            
        with open("raw_data/data.json", "w") as file: 
            json.dump(self.coin_data, file,indent=8) 


if __name__ == '__main__': 
    scraper = CoinMarketScraper() 
    scraper.load_webpage()
    scraper.create_list_of_webpage_links()
    scraper.webpage_links_iteration()
    scraper.coin_link_iteration()
