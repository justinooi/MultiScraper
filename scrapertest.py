import unittest
from Shopee_Scraper import Shopee_Scraper
from Amazon_Scraper import Amazon_Scraper
from multiScraperGUI import multiScraperGUI
from shopee_link_scraper import shopee_link_scraper
from amazon_link_scraper import amazon_link_scraper

class scrapertest(unittest.TestCase):
    """This class trials different scenarios and their outcomes for the program using the unittest framework.

    Args:
        unittest.TestCase: An object for testing, which implements the TestCase class to drive the test methods and report failures.
    """

    def setUp(self):
        """This function is called before each test to declare initialization of the Objects
        """
        self.ShopeeTest = Shopee_Scraper()
        self.AmazonTest = Amazon_Scraper()
        self.CrawlerTest = multiScraperGUI()

    def test_scrape_from_input_Shopee_True(self): #Test input for shopee link scraper
        """This function tests for a valid Shopee product which can be obtained from the linkscrape function.
        """
        link = Shopee_Scraper().linkScrape("sample_shopee_product",10)
        self.assertTrue(link, "Invalid input")

    def test_scrape_from_input_Amazon_True(self): #Test user input for amazon link scraper
        """This function tests for a valid Amazon product which can be obtained from the linkscrape function.
        """
        link = Amazon_Scraper().linkScrape("sample_amazon_product",10)
        self.assertTrue(link, "Invalid input")

    def test_invalid_URL_Shopee_False(self): #Test URL format for shopee if empty
        """This function tests for an invalid Shopee URL format in the product catalogue(Symbolic search parameters)
        """
        shopee_link_scraper.searchParameters="product123$%^%^#^$^$##@!@"
        self.assertTrue(shopee_link_scraper().linkSearch(), "Invalid URL Format")
    
    def test_invalid_URL_Amazon_False(self): #Test URL format for amazon if empty
        """This function tests for an invalid Amazon URL format in the product catalogue(Empty search parameter)
        """
        amazon_link_scraper.searchParameters=""
        self.assertTrue(amazon_link_scraper().linkSearch(), "Invalid URL Format")
    
    def test_valid_URL_Amazon_True(self): #Test URL format for amazon if not empty
        """This function tests for a valid Amazon URL format in the product catalogue
        """
        amazon_link_scraper.searchParameters="sample_search_results" 
        self.assertIsNotNone(amazon_link_scraper.searchParameters, "Invalid URL Format")
        
    def test_empty_parameter_False(self): #Check for empty parameter in GUI
        """This function tests for an invalid crawl input from the user in the GUI
        """
        empty_search = CrawlerTest.search_parameter = ""
        self.assertTrue(empty_search,"Empty User Input")
    
    def test_valid_search_parameter_True(self): #Check for valid search input in GUI
        """This function tests for a valid crawl input from the user in the GUI 
        """
        valid_search = CrawlerTest.search_parameter = "Product"
        self.assertTrue(valid_search,"Invalid input")
    
    def test_valid_shopee_txt_file_True(self): #Check whether there is a txt file for shopee URLS
        """This function checks for a valid-readable Shopee txt file containing a list of stored product IDs.
        """
        try:
            with open('shopee_urls.txt') as file:
                file.read()
        except FileNotFoundError as fnf_error:
            self.assertFalse(fnf_error,"Failed due to file not found")
    
    def test_valid_amazon_txt_file_True(self): #Check whether there is a txt file for amazon URLS
        """This function checks for a valid-readable Amazon txt file containing a list of stored product IDs.
        """
        try:
            with open('shopee_urls.txt') as file:
                file.read()
        except FileNotFoundError as fnf_error:
            self.assertFalse(fnf_error,"Failed due to file not found")
    
    def test_valid_shopee_csv_file_True(self): #Check for shopee-csv file
        """This function checks for a valid-readable Shopee CSV file containing a list of stored product information(ID,Name,Ratings,Etc).
        """
        try:
            with open('shopee-scrape.csv') as file:
                file.read()
        except FileNotFoundError as fnf_error:
            self.assertFalse(fnf_error,"Failed due to file not found")

if __name__ == '__main__':
    ShopeeTest = Shopee_Scraper()
    AmazonTest = Amazon_Scraper()
    CrawlerTest = multiScraperGUI()
    unittest.main()