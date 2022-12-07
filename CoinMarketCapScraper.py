# This imports the packages required to run the code below. This code leverages the selenium packages.
from selenium import webdriver 
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
        This method initialisess the CoinMarketScraper Class and passing the attributes
        Attributes passed through into the class below
        ----------------------------------------------
        driver: WebDriver
            This webdriver is used to load and naviagte the webpage allowing the data to be collected
        
        url: string
            The url for the coinmarketcap.com landing page

        page_links_list: List
            A list for all of the pages of the webpage in which cryptocurrencies are presented. From here the next page etc url's are stored. 
            This allows for urls for all the individual coins to be collected from each page

        coin_link_list: List
            A list of all the cryptocurrency coin page links whoch can then be iterated through to collect data on each coin
        """
        self.driver = webdriver.Chrome()
        self.url = 'https://coinmarketcap.com/'
        self.page_links_list = [self.url]
        self.coin_link_list = []
        self.data_dict = {}
        self.coin_data = []


    def load_webpage(self) -> str: 
        """
        This method calls the chromedriver to load the webpage and performs a check to ensure the webpage has loaded successfully or not. 
        If the pop up does not occure then the argument is passed
        """
        try:
            page = self.driver.get(self.url)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body')))
            return 'The page was loaded successfully'
        except TimeoutException:
            "The page was not loaded successfully"

    
    def create_list_of_webpage_links(self):
        """
        This method scrapes the webpage links for the following pages on the coinmarketcap.com site. 
        This method then appends the links to self.page_links_list which can then be accessed at another time.

        To do this, the method identifies the li tags which are present for each page of the website.
        Within the li tags, all of the a tags are stored, the a tags contain the desired urls for each page.
        """  
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(3)
        
        page_number_bar = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[6]/div[1]/div/ul') 
        li_tags = page_number_bar.find_elements(by=By.XPATH, value = '//*[@class="page"]') 
        
        for link in li_tags: 
            link = link.find_element(by=By.TAG_NAME, value = 'a').get_attribute('href')
            self.page_links_list.append(link)
        
        
    def create_list_of_coin_links(self) -> list:
        """
        This method scrapes the page provided for the cryptocurrency coin links that are stored on that page.
        To do this, the method finds the table in the html code within which all of these links are stored in.
        Once the table is found, it is iterated through to find the links and then appends the links to the link list.
        The link list is a local variable list to this method, for the current page provided, all of the coin links on the page are added to this list.
        The link_list for that page is then added to the self.coin_link_list through .extend in which this list contains all of the coin links on all of the pages iterated through.
        """ 
        link_list = [] 
        ignored_exceptions= (StaleElementReferenceException)
        WebDriverWait(self.driver, 20,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]'))) 

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(2)
        table = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody') 
        table_list = table.find_elements(by=By.XPATH, value = './tr') 
        for coin in table_list: 
            link = coin.find_element(by=By.TAG_NAME, value = 'a').get_attribute('href') 
            link_list.append(link) 
        self.coin_link_list.extend(link_list) 
        return self.coin_link_list
        

    def webpage_links_iteration(self): 
        """
        This method iterates through the page_links_list created in the create_list_of_webpage_links function above.
        The driver attribute is called to load each page.
        Once each page has been loaded, the create_list_of_coin_links function is called
        """

        for page in self.page_links_list[:2]: #
            self.driver.get(page)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body'))) 
            self.create_list_of_coin_links()
        

    def load_coin_webpage(self, coin_link) -> str:
        "Loads the url provided during the coin_link_iteration() method when called"
        self.driver.get(coin_link)
        try:
            pop_up_button = self.driver.find_element(by=By.XPATH, value = '/html/body/div[3]/div/div/div/div/button[2]')
            pop_up_button.click()
        except NoSuchElementException:
            pass
        
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@class="main-content"]'))) 
            return "The page was loaded successfully"
        except TimeoutException:
            return "The page was not loaded successfully"

     
    def scrape_webpage_data(self) -> dict: 
        """
        The following method scrapes the data for the desired metric for the coin page provided.
        Using the .find_element function along with locators within selenium, the location of the desired metric is sourced.

        Metrics scraped for each coin:
        Name
        Price
        Market cap
        24 Hour trading volume
        24 Hour price low
        24 Hour pricee high
        Image url: The urls for the images are found, the download_image_from_webpage method is then called to download the image to the local device
        Timestamp of the data scrape

        The data collected is then added to the local webpage_data_dict ditcionary.

        The dictionary is returned at the end of the method.       
        
        """
        coin_name = self.driver.find_element(by=By.XPATH, value = '//*[@class="sc-aba8b85a-0 gmYubB h1"]/span/span').text
        price = self.driver.find_element(by=By.XPATH, value = '//*[@class="priceValue "]').text                                                          
        market_cap = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div').text
        daily_volume = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/div[3]/div[1]/div[2]/div').text
        daily_low = self.driver.find_element(by=By.XPATH, value = '//*[@class="sc-aef7b723-0 kIYhSM"]/span/span').text
        daily_high = self.driver.find_element(by=By.XPATH, value = '//*[@class = "sc-aef7b723-0 gjeJMv"]/span/span').text
        str_time_stamp = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime("%d-%m-%Y, %H:%M:%S")
        coin_img_src = self.driver.find_element(by=By.TAG_NAME, value = 'img').get_attribute('src')
        self.download_image_from_webpage(coin_img_src, f"images/{coin_name}_{str_time_stamp}.jpg")
                
        self.data_dict['Name'] = coin_name
        self.data_dict['Price'] = price
        self.data_dict['Market Cap'] = market_cap
        self.data_dict['24hr Trading Volume'] = daily_volume
        self.data_dict['24hr Price Low'] = daily_low
        self.data_dict['24hr Price High'] = daily_high
        self.data_dict['Image'] = coin_img_src
        self.data_dict['Timestamp'] = str_time_stamp
        
        return self.data_dict 
    
    def download_image_from_webpage(self, coin_img_src, fp):

        """
        This method calls the coin image src and the filepath set in the get data method to download the image stored on each coin page.
        Using a the os context manager a folder is created in the repository to store the images in, should there not alreadt be a folder with this name created
        Using the driver and calling the coin_image_src located earlier, the content of the link (the image) is collected
        The image is then stored with in the folder created and is named using the coin name and timestamp data in the scrape_webpage_data method
        """

        if os.path.exists("images") == False: 
            os.makedirs("images") 

        coin_img_data = requests.get(coin_img_src).content 

        with open(fp, 'wb') as handler: 
            handler.write(coin_img_data) 


    def coin_link_iteration(self):
        """
        This method iterates through each coin link collected in the create_list_of_coin_links method by loading the url through the WebDriver. 
        For each page iterated through, there is code to close the pop-up that appears.
        The scrape_webpage_data method is then called once the page structure has fully loaded
        The data dictionary returned by the scrape_webpage_data method is then appeneded to the self.coin_data list
        The self.coin_data_list data is then dumped into a JSON file in a raw_data folder, both created using the OS context manager
        
        """
        for coin_link in self.coin_link_list: 
            self.load_coin_webpage(coin_link)
            self.coin_data.append(self.scrape_webpage_data()) 
            

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
