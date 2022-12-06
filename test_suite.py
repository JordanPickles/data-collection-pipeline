import unittest
from unittest.mock import patch
import requests
from CoinMarketCapScraper import CoinMarketScraper
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import time
import os



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