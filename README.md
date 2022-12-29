# Data Collection Pipeline Project
Project descripton: "An implementation of an industry grade data collection pipeline that runs scalably in the cloud. It uses Python code to automatically control your browser, extract information from a website, and containerise the application in a docker image. The system conforms to industry best practices such as being containerised in Docker and running automated tests."

This project formulates project 3 of the Ai Core data career accelerator, this project will aim to develop a webscraper to collate data from the website, 'coinmarketcap.com'.

CoinMarketCap is the world's most-referenced price-tracking website for cryptoassets in the rapidly growing cryptocurrency space. Its mission is to make crypto discoverable and efficient globally by empowering retail users with unbiased, high quality and accurate information for drawing their own informed conclusions. This website collates all of the registered cryptocurrencies and their details such as pricing, all time highs, market cap, daily trading volume and many more metrics which are all useful for understanding cyrptocurrencies. Many people investing and trading with crypotcurrencies utilise these metrics to make informed investment / trading decisions.


## Milestone 1-4: Developing the web scraper
The project uses chromedriver to control the webpage. Using selenium, this milestone scrapes the links of each page on the webpage and then iterates through each webpage to scrape and collate all of the individual coin page links. These are then added to a list which will then be itterable for collecting data in later milestones.


The CoinMarketScraper class was initialised passing through attributes to be used throughout the scraper class by differing methods.
```
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

        self.num_coins: Object
            This argument provides a namespace object detailing that data should be collected for the top n coins, default is set at 200
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
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--num-coins', type=int, default = 200)
        args = parser.parse_args()
        self.num_coins = args.num_coins
        
```
Calling the chromedriver, the coinmarketcap.com url was loaded and a list of the page url's containing cryptocurrency coins data and urls was collected.

```
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
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[6]/div[1]/div/ul')))
        
        page_number_bar = self.driver.find_element(by=By.XPATH, value = '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[6]/div[1]/div/ul') 
        li_tags = page_number_bar.find_elements(by=By.XPATH, value = '//*[@class="page"]') 
        
        for link in li_tags: 
            link = link.find_element(by=By.TAG_NAME, value = 'a').get_attribute('href')
            self.page_links_list.append(link)

```

The create_list_of_coin_links() method scrapes the url links of all the coins contained on each page, this method was then called in the web_page_links_iteration() method to collect these links on each of the pages loaded. The pages loaded are from the create_list_of_webpage_links() method above.
```
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
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody')))
        table = self.driver.find_element(by=By.XPATH, value='//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[4]/table/tbody') 
        table_rows = table.find_elements(by=By.XPATH, value = './tr') 
        for coin in table_rows: 
            link = coin.find_element(by=By.TAG_NAME, value = 'a').get_attribute('href') 
            link_list.append(link) 
        self.coin_link_list.extend(link_list) 
        

    def webpage_links_iteration(self): 
        """This method iterates through the page_links_list created in the create_list_of_webpage_links() method and calls the create_list_of_coin_links() after each new page is loaded."""

        for page in self.page_links_list[:2]:
            self.driver.get(page)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body'))) 
            self.create_list_of_coin_links()
```
Once the list of the coin urls was collected the below methods were created to be called later in the script. The scrape_webpage_data calls the chromedriver to load the url provided by the coin_link_iteration() method and then proceed to use locators within selenium to locate and scrape different data points on each page. The coinmarketcap.com site has a slightly different structure for coins listed 1-10, 11-25 and 25-100. Therefore the locators were chosen to most effectively scrape the data from coin pages in all 3 brackets/sections. The download_image_from_webpage() method downloads the image from the image src scraped on each page and stores it locally using a context manager.

```
    def __scrape_webpage_data(self, coin_link) -> dict: 
        """
        This private method scrapes the data for the desired metric for the coin page loaded. The data is added to the self.data_dict.
        Input: 
            coin_link: str
                url of the webpage for the coin to be iterated through
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
        Input: 
            coin_img_src: string
                Image url link collected in the _scrape_webpage_data() method
        -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        coin_img_data: .jpg file
            Downloads the image using requests.get
        """
        if os.path.exists("raw_data/images") == False: 
            os.makedirs("raw_data/images") 
        coin_img_data = requests.get(coin_img_src).content 

        with open(fp, 'wb') as handler: 
            handler.write(coin_img_data) 


```
Finally the coin links previously collated were then iterated through calling the load_coin_page() and scrape_webpage_data() methods to collect the data from each coin_link and then dump that data into local directories in the form of .jpg and .json files.

```
   def coin_link_iteration(self):
        """This public method iterates through the number of coin links specificed by the args.parse function when running the script (default = top 200 coins) and calls the private method, scrape_webpage_data() for each coin. 
        The data from each coin link is appended to the self.coin_data list and this data is dumped into a .json file and stored locally."""
        coin_link_list = []
        
        for i in range(self.num_coins):
            coin_link_list.append(self.coin_link_list.pop(0))


        for coin_link in coin_link_list: 
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
```

## Milestone 5: Creates a test suite to test the CoinMarketScraper class
Using the unittest package, tests are created for the publically available methods in the CoinMarketScraper.

```
class CoinMarketCapScraper(unittest.TestCase):
    """Test suite for the public methods CoinMarketScraper"""
    def setUp(self):
        self.scraper = CoinMarketScraper()
        self.scraper.load_webpage()

    def test_load_webpage(self):
        """Ensures the url is loaded correctly, taking in the 'The page loaded successfully' from the CoinMarketScraper class"""
        print("test_load_webpage setup")    
        self.assertEqual('The page was loaded successfully', self.scraper.load_webpage())
    
    def test_create_list_of_webpage_links(self):
        """Tests if the self.page_links_list, (where the page links are appended too) is a list, containing 11 links and that the links are stored as strings"""
        print("test_create_list_of_webpage_links setup")
        self.scraper.create_list_of_webpage_links()

        self.assertIsInstance(self.scraper.page_links_list, list)
        self.assertAlmostEqual(11, len(self.scraper.page_links_list))
        self.assertIsInstance(self.scraper.page_links_list[0], str) 

    def test_webpage_links_iteration(self):
        """Tests if the links collected in the create_list_of_webpage_links() method can be iterated through to collect a list of coin page links. With there being 100 coins 
        on each page and this iteration taking in the first 2 pages. It is tested that the len of the coin_link_list is 200, that it is a list and that the list contains urls as strings"""
        print("test_webpage_links_iteration")
        self.scraper.create_list_of_webpage_links()
        self.scraper.webpage_links_iteration()
        self.assertIsInstance(self.scraper.coin_link_list, list)
        self.assertAlmostEqual(200, len(self.scraper.coin_link_list))
        self.assertIsInstance(self.scraper.coin_link_list[0], str)

    def test_coin_link_iteration(self): 
        """Tests the function responsible for iterating through the coin_links_list and scraping the required data before extending the data into coin_data. This method tests that coin_data is a list, 
        containing dicts. Whilst the number of dicts in the list is tested to equal the number of coin_links in the coin_link_list. The final test checks that the dat.json file is stored in the correct directory.
        
        This test method also tests the outputs from the private methods self.__scrape_webpage_data() and self.__download_image_from_webpage(). This checks that the data is stored in the correct type and as expected"""
        self.scraper.create_list_of_webpage_links()
        self.scraper.webpage_links_iteration()
        self.scraper.coin_link_iteration()
        
        self.assertIsInstance(self.scraper.coin_data[0]['Name'], str)
        self.assertIsInstance(self.scraper.coin_data[0]['Price'], str)
        self.assertIsInstance(self.scraper.coin_data[0]['Market Cap'], str)
        self.assertIsInstance(self.scraper.coin_data[0]['24hr Trading Volume'], str)
        self.assertIsInstance(self.scraper.coin_data[0]['24hr Price Low'], str)
        self.assertIsInstance(self.scraper.coin_data[0]['24hr Price High'], str)
        self.assertIsInstance(self.scraper.coin_data[0]['Image'], str)
        self.assertIsInstance(self.scraper.coin_data[0]['Timestamp'], str)

        assert os.path.isfile('raw_data/images/' + self.scraper.coin_data[0]['Name'] + '_' + self.scraper.coin_data[0]['Timestamp'] + '.jpg')

        self.assertIsInstance(self.scraper.coin_data, list)
        self.assertIsInstance(self.scraper.coin_data[0], dict)
        self.assertAlmostEqual(8, len(self.scraper.coin_data[0]))
        self.assertEqual(len(self.scraper.coin_data), len(self.scraper.coin_link_list))
        assert os.path.isfile('./raw_data/data.json')


if __name__ == '__main__':
    unittest.main()
```

## Milestone 6: Containerising in Docker
The full Coin Market Cap scrper was containerised as a docker image. To run the scraper in docker, WebDriverManager was required to be installed and chromedriver needed to be set to run in headless mode, therefore the webpage will not be loaded. Several options were passed into the chromedriver options.

```
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-setuid-sandbox") 
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options = chrome_options)
```

To have the data stored locally on your machine a volume should be created in the command line detailing the path in which the data should be stoed locally (see below).

``` docker run --rm --name <name the container> -v <local file path for data to be saved in>:/scraper/raw_data coin_market_scraper_python_img --num-coins=<number of coins you wish to scrape data for>```


## Milestone 7: CI/CD Pipeline for the Docker image
A github action was created to push all of the updates in the source code to the Docker image. Every time a commit is to be made to the main branch, a workflow is triggered to rebuild the image. To provide access to the docker hub account, github secrets were created detailing the docker account name and a personal access token (PAT).

