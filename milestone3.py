
# This imports the packages required to run the code below. This code leverages the selenium packages.
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time


# This CoinMarket scraper scrapes data from the top 200 cryptocurrencies. Cryptocurrency adotpion is ever growing with coin utility to solve real-life problems being ever growing. There are however a vast some of coins, this class provides code that has the ability to automate the coinmarket webpage and pull the requested data. 
class CoinMarketScraper:
    #Initialising the CoinMarketScraper Class and passing the parameters within the code
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = 'https://coinmarketcap.com/'
        self.page_links_list = [self.url] # a list to append the page links to, the url is already included as the data on this page is needed to be scraped
        self.coin_link_list = []

    def load_page(self): # This method calls the chromedriver to load the webpage 
        page = self.driver.get(self.url)
        # This block closes a potential pop-up on the site
        try:
            pop_up_button = self.driver.find_element(by=By.XPATH, value = '/html/body/div[3]/div/div/div/div/button[2]')
            pop_up_button.click()
        except NoSuchElementException:
            pass

        # This method scrapes the links for the pages on the website
    def get_page_links(self): 
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # This code scrolls the webdriver to the bottom of the current page
        page_number_bar = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[1]/div[6]/div/ul') # Locates the page number bar at the bottom of the page, within this tree, the links to the next pages are contained
        li_tags = page_number_bar.find_elements(by=By.XPATH, value = '//*[@class="page"]') # finds all of the li_tags within the tree, these tags contain atags which include the href link for each page allowing page itteraiton
        
        for link in li_tags: # Itterates through the li_tags to 
            a_tags = link.find_element(by=By.TAG_NAME, value = 'a')# finds the a-tags 
            link = a_tags.get_attribute('href') # finds the href link for the next page
            self.page_links_list.append(link) # appends the href to a list containing all the hrefs

    def page_itteration(self):
        for page in self.page_links_list[:2]: # Itterates through the first 2 pages of the code
            self.driver.get(page) # uses the get function to load the the webpage next in the self.link_list
            self.get_coin_links() #calls the method to scrape all of the coin links on the page

    # This method scrapes the page provided for the coin links
    def get_coin_links(self):
        delay = 20
        link_list = [] # provides a local empty list to append individual links to from each webpage
        ignored_exceptions= (StaleElementReferenceException)
        WebDriverWait(self.driver, delay,ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[1]/div[5]/table'))) # Allows the page to load and stops the code running until the page is loaded
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scrolls to the bottom of the page to load all of the coin links
        time.sleep(1) # Allows page to load and ensures the page doesn't assume this is a script
        table = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div[1]/div[1]/div[2]/div/div[1]/div[5]/table/tbody') # finds the table containing all of the coin links and assigns it
        table_list = table.find_elements(by=By.XPATH, value = './tr') # finds all of the table rows in the table previosuly assigned above
        for coin in table_list: # Itterates through the table rows containing the data
            a_tag = coin.find_element(by=By.TAG_NAME, value = 'a') # finds the a tags in the 
            link = a_tag.get_attribute('href') # gets the href in the a_tag
            link_list.append(link) # appends the links to a local list
        self.coin_link_list.extend(link_list) # extends the self.coin_list with the local link list containing each indivudal pages links. The self.coin_link_list contains all of the pages links


if __name__ == '__main__':
    scraper = CoinMarketScraper() #Creates an instance of the scraper class
    scraper.load_page() # calls the methods in the isntance
    scraper.get_page_links()
    scraper.page_itteration()