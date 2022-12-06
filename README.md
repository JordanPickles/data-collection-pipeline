# Data Collection Pipeline
This project creates a webscraper for coinmarket.com using selenium in python. Coinmarket.com collates all of the registered cryptocurrencies and their details such as pricing, all time highs, market cap, daily trading volume which are all useful metrics for understanding the cyrptocurrency, it's history and current performance. Many people investing and trading with crypotcurrency utilise these metrics to make informed financial decisions.

## Milestone 1-4: Developing the web scraper
The project uses chromedriver to control the webpage. Using selenium, this milestone scrapes the links of each page on the webpage and then iterates through each webpage to scrape and collate all of the individual coin page links. These are then added to a list which will then be itterable for collecting data in later milestones.

The CoinMarketScraper class was initialised passing through attributes to be used throughout the scraper class by differing methods.

```
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
        
```
Calling the chromedriver, the coinmarket.com url was loaded and a list of the page url's containing cryptocurrency coins data and urls was collected.

```
def load_webpage(self): 
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

```
The create_list_of_coin_links method scrapes the url links of all the coins contained on each page, this method was then called in the web_page_links_iteration() method to collect these links on each of the pages loaded. The pages loaded are from the create_list_of_webpage_links() method above.
```
    def create_list_of_coin_links(self):
        """
        This method scrapes the page provided for the cryptocurrency coin links that are stored on that page.
        To do this, the method finds the table in the html code within which all of these links are stored in.
        Once the table is found, it is iterated through to find the links and then appends the links to the link list.
        The link list is a local variable list to this method, for the current page provided, all of the coin links on the page are added to this list.
        The link_list for that page is then added to the self.coin_link_list through .extend in which this list contains all of the coin links on all of
        the pages iterated through.
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
```
Once the list of the coin urls was collected the below methods were created to be called later in the script. The load_coin_webpage() method calls the chromedriver to load the url provided by the coin_link_iteration() method. The scrape_webpage_data uses locators within selenium to locate and scrape different data points on each page. The coinmarket.com site has a slightly different structure for coins listed 1-10, 11-25 and 25-100. Therefore the locators were chosen to most effectively scrape the data from coin pages in all 3 brackets/sections. The download_image_from_webpage() method downloads the image from the image src scraped on each page and stores it locally using a context manager.

```
    
    def load_coin_webpage(self, coin_link):
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

     
    def scrape_webpage_data(self): 
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

```
Finally the coin links previously collated were then iterated through calling the load_coin_page() and scrape_webpage_data() methods to collect the data from each coin_link and then dump that data into local directories in the form of .jpg and .json files.

```
    def coin_link_iteration(self):
        """
        This method iterates through each coin link collected in the create_list_of_coin_links method by loading the url through the WebDriver. 
        For each page iterated through, there is code to close the pop-up that appears.
        The scrape_webpage_data method is then called once the page structure has fully loaded
        The data dictionary returned by the scrape_webpage_data method is then appeneded to the self.coin_data list
        The self.coin_data_list data is then dumped into a JSON file in a raw_data folder, both created using the OS context manager
        
        """
        for coin_link in self.coin_link_list[0:3]: 
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
```

## Milestone 5: Creates a test suite to test the CoinMarketScraper class
Using the unittest package, tests are created for the publically available methods in the CoinMarketScraper.

The Majority of these unit tests only test that webpages have been loaded successfully by chromedriver, check that the data collected is in the correct type, in the correct data format. Finally tests are run to ensure the data and imagesare stored locally with the correct name.

```
class CoinMarketCapScraper(unittest.TestCase):
    """Test suite for CoinMarketScraper"""
    def setUp(self):
        self.scraper = CoinMarketScraper()
        self.scraper.load_webpage()

    def test_load_webpage(self):
        """Ensures the url is loaded correctly, taking in the 'The page loaded successfully' from the CoinMarketScraper class"""
        self.setUp()
        print("test_load_webpage setup")    
        self.assertEqual('The page was loaded successfully', self.scraper.load_webpage())
    
    def test_create_list_of_webpage_links(self):
        """Tests if the self.page_links_list, (where the page links are appended too) is a list, containing 11 links and that the links are stored as strings"""
        print("test_create_list_of_webpage_links setup")
        self.setUp()
        self.scraper.create_list_of_webpage_links()

        self.assertIsInstance(self.scraper.page_links_list, list)
        self.assertAlmostEqual(11, len(self.scraper.page_links_list))
        self.assertIsInstance(self.scraper.page_links_list[0], str) 

    def test_webpage_links_iteration(self):
        """Tests if the links collected in the create_list_of_webpage_links() method can be iterated through to collect a list of coin page links. With there being 100 coins 
        on each page and this iteration taking in the first 2 pages. It is tested that the len of the coin_link_list is 200, that it is a list and that the list contains urls as strings"""
        print("test_webpage_links_iteration")
        self.setUp()
        self.scraper.create_list_of_webpage_links()
        self.scraper.webpage_links_iteration()
        self.assertIsInstance(self.scraper.coin_link_list, list)
        self.assertAlmostEqual(200, len(self.scraper.coin_link_list))
        self.assertIsInstance(self.scraper.coin_link_list[0], str)
        
    def test_load_coin_webpage(self):
        self.setUp()
        self.scraper.create_list_of_webpage_links()
        self.scraper.webpage_links_iteration()
        self.assertEqual('The page was loaded successfully', self.scraper.load_coin_webpage(self.scraper.coin_link_list[0]))

    def test_scrape_webpage_data(self):
        """Tests that the scrape_webpage_data() method returns the self.data_dict and tests if this is a dict, a dict containing 8 k:v pairs and that the values are all stored as strings"""
        self.setUp()
        self.scraper.create_list_of_coin_links()
        self.scraper.load_coin_webpage(self.scraper.coin_link_list[0])
        self.scraper.scrape_webpage_data()
        
        self.assertIsInstance(self.scraper.data_dict, dict)
        self.assertAlmostEqual(8, len(self.scraper.data_dict))
        
        self.assertIsInstance(self.scraper.data_dict['Name'], str)
        self.assertIsInstance(self.scraper.data_dict['Price'], str)
        self.assertIsInstance(self.scraper.data_dict['Market Cap'], str)
        self.assertIsInstance(self.scraper.data_dict['24hr Trading Volume'], str)
        self.assertIsInstance(self.scraper.data_dict['24hr Price Low'], str)
        self.assertIsInstance(self.scraper.data_dict['24hr Price High'], str)
        self.assertIsInstance(self.scraper.data_dict['Image'], str)
        self.assertIsInstance(self.scraper.data_dict['Timestamp'], str)

    def test_download_image_from_webpage(self):
        """Tests that the download_image() method downloads and stores the images locally from the src link provided in the scrape_webpage_data() method. This checks a file with the expected name 
        and timestamps is stored in the expected directory"""
        self.setUp()
        self.scraper.create_list_of_coin_links()
        self.scraper.load_coin_webpage(self.scraper.coin_link_list[0])
        self.scraper.scrape_webpage_data()
        print(f"'./images/{self.scraper.data_dict['Name']}_{self.scraper.data_dict['Timestamp']}.jpg'")
        assert os.path.isfile('images/' + self.scraper.data_dict['Name'] + '_' + self.scraper.data_dict['Timestamp'] + '.jpg')

    def test_coin_link_iteration(self):
        """Tests the function responsible for iterating through the coin_links_list and scraping the required data before extending the data into coin_data. This method tests that coin_data is a list, 
        containing dicts. Whilst the number of dicts in the list is tested to equal the number of coin_links in the coin_link_list. The final test checks that the dat.json file is stored in the correct directory """
        self.setUp()
        self.scraper.create_list_of_webpage_links()
        self.scraper.webpage_links_iteration()
        self.scraper.coin_link_iteration()
        
        self.assertIsInstance(self.scraper.coin_data, list)
        self.assertIsInstance(self.scraper.coin_data[1], dict)
        self.assertEqual(len(self.scraper.coin_data), len(self.scraper.coin_link_list))
        assert os.path.isfile('./raw_data/data.json')


if __name__ == '__main__':
    unittest.main()
```
