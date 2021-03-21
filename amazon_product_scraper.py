import csv
from requests_html import AsyncHTMLSession
from abstract_product_scraper import abstract_product_scraper
from bs4 import BeautifulSoup
import time

class amazon_product_scraper(abstract_product_scraper):
    """This class functions to scrape all product data of the user requested pages from user requested website defined in the GUI. All function elements are also controlled by the abstract class.

    Args:
        abstract_product_scraper (Object): user define abstract class defining the properties of how the product scaper should function.
    """

    def __init__(self, url_file):
        """This function is for self defined variables for storage purposes

        Args:
            url_file (string): file path 
        """
        self.file = url_file
        self.links = []
        self.results = []
        self.attributes = []

    def get_product_links(self):
        """This function gets and seperates all product links and preparing the links for scraping.
        """
        with open(self.file) as file_reader:
            self.links = file_reader.read().splitlines()

    def asynchronousProcessing(self):
        """This function processes the links that are prepared and scrapes all the link in an async function awaiting request of 5 at a time.
                asession : creates a html session for the scarping of data
                NUMBER_OF_LAMBDA_FUNCTIONS : set the number of request calls wanted per cycle 
        """
        NUMBER_OF_LAMBDA_FUNCTIONS = 5
        asession = AsyncHTMLSession()
        print("Commencing asynchronous requests")
        print("Number of requesting processes set to 5")

        # If not multiple of 5s, add empty links that will not be processed by lambda function.
        remainder = len(self.links)%5
        if remainder == 1:
            for i in range(4):
                self.links.append('IGNORE')
        if remainder == 2:
            for i in range(3):
                self.links.append('IGNORE')
        if remainder == 3:
            for i in range(2):
                self.links.append('IGNORE')
        if remainder == 4:
            self.links.append('IGNORE')

        for i in range(0, len(self.links), NUMBER_OF_LAMBDA_FUNCTIONS):
            self.results.append(asession.run(  # Calls 5 requests (PROCESSES) in 1 go
                lambda: self.get_product_details(self.links[i], asession),
                lambda: self.get_product_details(self.links[i + 1], asession),
                lambda: self.get_product_details(self.links[i + 2], asession),
                lambda: self.get_product_details(self.links[i + 3], asession),
                lambda: self.get_product_details(self.links[i + 4], asession),
            ))
            print("Scraping ", i + NUMBER_OF_LAMBDA_FUNCTIONS, "/", len(self.links))
        for i in range(len(self.results)):
            for j in range(len(self.results[0])):
                self.attributes.append(self.results[i][j])

    async def get_product_details(self, link, asession):
        """This function gets all product details after opening the prepared links in the async function 

        Args:
            link (Int): Contains the link that is prepared for scarping 
            asession (object): session created by the library for the html page that is opened 

        Returns:
            [Tuple]: Returns everything that is scraped such as price and name of product. Return of this type can contain different variable types 
        """
        items = [None] * 6
        items[0] = link
        url = "https://amazon.com/dp/" + link

        if 'IGNORE' in url:
            return ['IGNORE']

        webpage = await asession.get(url, headers=self.HEADERS)
        try:
            await webpage.html.arender(sleep=2, timeout=30)
        except:
            pass
        soup = BeautifulSoup(webpage.content, "lxml")

        # Get Product Title
        try:
            title = soup.find("span", attrs={"id": 'productTitle'})
            items[1] = title.string.strip().replace(',', '')
        except AttributeError:
            items[1] = 'N/A'

        # Get Product Price
        try:
            items[2] = soup.find("span", attrs={'id': 'priceblock_ourprice'}).string.strip().replace(',', '')
        except AttributeError:
            items[2] = 'N/A'

        # Get Product Rating
        try:
            items[3] = soup.find("i", attrs={
                'class': 'a-icon a-icon-star a-star-4-5'}).string.strip().replace(',', '')
            if 'Previous page of related Sponsored Products' in items[3]:
                items[3] = 'N/A'
        except AttributeError:
            try:
                items[3] = soup.find(
                    "span", attrs={'class': 'a-icon-alt'}).string.strip().replace(',', '')
                if 'Previous page of related Sponsored Products' in items[3]:
                    items[3] = 'N/A'
            except:
                items[3] = "N/A"

        # Get Product Review Count
        try:
            items[4] = soup.find(
                "span", attrs={'id': 'acrCustomerReviewText'}).string.strip().replace(',', '')
        except AttributeError:
            items[4] = "N/A"

        # Get Product Availability
        try:
            available = soup.find("div", attrs={'id': 'availability'})
            items[5] = available.find("span").string.strip().replace(',', '')
        except AttributeError:
            items[5] = "N/A"

        return tuple(items)

    def store_product_details(self):
        """This function stores all the details of the scraped product from the get_product_details function into a csv file 
        """
        file_name = 'output-amazon.csv'
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(self.attributes)
