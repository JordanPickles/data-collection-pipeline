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


# This CoinMarket scraper scrapes data from the top 200 cryptocurrencies. Cryptocurrency adotpion is ever growing with coin utility to solve real-life problems being ever growing. There are however a vast some of coins, this class provides code that has the ability to automate the coinmarket webpage and pull the requested data. 
class CoinMarketScraper:
    #Initialising the CoinMarketScraper Class and passing the parameters 
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://coinmarketcap.com/'
        self.page_links_list = [self.url]
        self.coin_link_list = []
        self.data_dict = {}
        self.coin_data = []


    def load_webpage(self): # This method calls the chromedriver to load the webpage 
        page = self.driver.get(self.url)
        # This block closes a potential pop-up on the site
        try:
            pop_up_button = self.driver.find_element(by=By.XPATH, value = '/html/body/div[3]/div/div/div/div/button[2]')
            pop_up_button.click()
        except NoSuchElementException:
            pass

        # This method scrapes the links for the pages on the website
    def create_list_of_webpage_links(self): 
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # This code scrolls the webdriver to the bottom of the current page
        page_number_bar = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[6]/div[1]/div/ul') # Locates the page number bar at the bottom of the page, within this tree, the links to the next pages are contained
        li_tags = page_number_bar.find_elements(by=By.XPATH, value = '//*[@class="page"]') # finds all of the li_tags within the tree, these tags contain atags which include the href link for each page allowing page itteraiton
        
        for link in li_tags: # Itterates through the li_tags to 
            a_tags = link.find_element(by=By.TAG_NAME, value = 'a')# finds the a-tags 
            link = a_tags.get_attribute('href') # finds the href link for the next page
            self.page_links_list.append(link) # appends the href to a list containing all the hrefs

    def webpage_links_iteration(self):
        for page in self.page_links_list[:1]: # Iterates through the first 2 pages of the code
            self.driver.get(page) # uses the get function to load the the webpage next in the self.link_list
            self.get_coin_links() #calls the method to scrape all of the coin links on the page

    # This method scrapes the page provided for the coin links
    def get_coin_links(self):
        delay = 20
        link_list = [] # provides a local empty list to append individual links to from each webpage
        ignored_exceptions= (StaleElementReferenceException)
        WebDriverWait(self.driver, delay,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]'))) # Allows the page to load and stops the code running until the page is loaded
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scrolls to the bottom of the page to load all of the coin links
        time.sleep(1) # Allows page to load and ensures the page doesn't assume this is a script
        table = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody') # finds the table containing all of the coin links and assigns it
        table_list = table.find_elements(by=By.XPATH, value = './tr') # finds all of the table rows in the table previosuly assigned above
        for coin in table_list: # Iterates through the table rows containing the data
            a_tag = coin.find_element(by=By.TAG_NAME, value = 'a') # finds the a tags in the 
            link = a_tag.get_attribute('href') # gets the href in the a_tag
            link_list.append(link) # appends the links to a local list
        self.coin_link_list.extend(link_list) # extends the self.coin_list with the local link list containing each indivudal pages links. The self.coin_link_list contains all of the pages links
        print(self.coin_link_list)

    
    # The following method scrapes the desired metric and value for the coin page provided. Each metric has 3 find_element options as different coin pages have differing code structures. 
    # These 3 find_element lines of code cover all of the differing structures, should none of these be found in the webpage, "NA" is added to the list for that page itteration


    def get_data(self):
        data_dict = {} # Provides a local empty dictionary for every coin that is itterated

        # Scrapes the required data from eeach page
        coin_name = self.driver.find_element(by=By.XPATH, value = '//*[@class="sc-aba8b85a-0 gmYubB h1"]/span/span').text
        price = self.driver.find_element(by=By.CLASS_NAME, value = 'priceValue ').text
        market_cap = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div[2]/div').text
        daily_volume = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[3]/div[1]/div[3]/div[1]/div[2]/div').text
        daily_low = self.driver.find_element(by=By.XPATH, value = '//*[@class="sc-aef7b723-0 kIYhSM"]/span/span').text
        daily_high = self.driver.find_element(by=By.XPATH, value = '//*[@class = "sc-aef7b723-0 gjeJMv"]/span/span').text
        
        # Scrapes the image link (src) and then downloads the image by calling the download image function and passing the src through as an argument
        coin_img_src = self.driver.find_element(by=By.TAG_NAME, value = 'img').get_attribute('src')
        self.download_image_from_webpage(coin_img_src, f"images/{coin_name}_{datetime.now()}.jpg")
        
        str_time_stamp = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime("%d-%m-%Y, %H:%M:%S") # Provides a time stamp for each page that is scraped
        
        
        data_dict['Name'] = coin_name
        data_dict['Price'] = price
        data_dict['Market Cap'] = market_cap
        data_dict['24hr Trading Volume'] = daily_volume
        data_dict['24hr Price Low'] = daily_low
        data_dict['24hr Price High'] = daily_high
        data_dict['Image'] = coin_img_src
        data_dict['Timestamp'] = str_time_stamp
        return data_dict 
        
    # This method calls the coin image src and the filepath set in the get data method to download the image stored on each coin page
    def download_image_from_webpage(self, coin_img_src, fp):
        if os.path.exists("images") == False: # Checks to see if a folder named images currently exists
            os.makedirs("images") # If the above statement is false, a directory is created 
        coin_img_data = requests.get(coin_img_src).content # requests the content from the link provided for the image
        with open(fp, 'wb') as handler: # Opens up the image and stores the contents collected from the image link above
            handler.write(coin_img_data) 



    def coin_link_iteration(self):
        delay = 20  
        coin_data = []
        for coin_link in self.coin_link_list[0:3]: # Iterates through each coin link
            try:
                pop_up_button = self.driver.find_element(by=By.XPATH, value = '/html/body/div[3]/div/div/div/div/button[2]')
                pop_up_button.click()
            except NoSuchElementException:
                pass

            self.driver.get(coin_link) # loads each coin page
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]'))) # Ensures each page is loaded before continuing the code
            self.coin_data.append(self.get_data()) # Calls the get data method for each coin and appends the data to self.coin_data
        print(self.coin_data)

        if os.path.exists("raw_data") == False: # Checks to see if a raw data directory has been created
            os.makedirs("raw_data") # Creates a directory for the raw data if the above statement is false
            
        with open("raw_data/data.json", "w") as file: # creates a JSON file in the raw_data directory just created
            json.dump(self.coin_data, file,indent=8) # Dumps the data in the JSON file just created



if __name__ == '__main__': # Ensures the file is only run when the file is run directly
    scraper = CoinMarketScraper() #Creates an instance of the scraper class
    scraper.load_webpage()
    scraper.create_list_of_webpage_links()
    scraper.webpage_links_iteration()
    scraper.coin_link_iteration()