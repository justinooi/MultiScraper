import csv
import re
from requests_html import AsyncHTMLSession
from abstract_product_scraper import abstract_product_scraper


class shopee_product_scraper(abstract_product_scraper):
    """This class functions to scrape all product data of the user requested pages from user requested website defined in the GUI. All function elements are also controlled by the abstract class.

    Args:
        abstract_product_scraper (Object): user define abstract class defining the properties of how the product scaper should function.

    Returns:
        [String]: File name of the file that all the details of the scraped product is stored.
    """

    ITEMS_PER_PAGE = 50

    def __init__(self, url_file):
        """Self defined variables for storage purposes

        Args:
            url_file (string): file path 
        """
        self.file = url_file
        self.links = []
        self.results = []
        self.attributes = []

    def get_product_links(self):
        """Gets and seperates all product links and preparing the links for scraping.
        """
        with open(self.file) as file_reader:
            self.links = file_reader.read().splitlines()

    def asynchronousProcessing(self):
        """Async file processes the links that are prepared and scrapes all the link in an async function awaiting request of 5 at a time.
                asession : creates a html session for the scarping of data
                NUMBER_OF_LAMBDA_FUNCTIONS : set the number of request calls wanted per cycle 
        """

        NUMBER_OF_LAMBDA_FUNCTIONS = 10
        asession = AsyncHTMLSession()
        print("Commencing asynchronous requests")
        print("Number of requesting processes set to 10")

        # If not multiple of 5s, add empty links that will not be processed by lambda function.
        remainder = len(self.links) % 5
        if remainder == 1:
            for i in range(9):
                self.links.append('IGNORE')
        if remainder == 2:
            for i in range(8):
                self.links.append('IGNORE')
        if remainder == 3:
            for i in range(7):
                self.links.append('IGNORE')
        if remainder == 4:
            for i in range(6):
                self.links.append('IGNORE')
        if remainder == 5:
            for i in range(5):
                self.links.append('IGNORE')
        if remainder == 6:
            for i in range(4):
                self.links.append('IGNORE')
        if remainder == 7:
            for i in range(3):
                self.links.append('IGNORE')
        if remainder == 8:
            for i in range(2):
                self.links.append('IGNORE')
        if remainder == 9:
            self.links.append('IGNORE')

        for i in range(0, len(self.links), NUMBER_OF_LAMBDA_FUNCTIONS):
            self.results.append(asession.run(  # Calls 10 requests (PROCESSES) in 1 go
                lambda: self.get_product_details(self.links[i], asession),
                lambda: self.get_product_details(self.links[i + 1], asession),
                lambda: self.get_product_details(self.links[i + 2], asession),
                lambda: self.get_product_details(self.links[i + 3], asession),
                lambda: self.get_product_details(self.links[i + 4], asession),
                lambda: self.get_product_details(self.links[i + 5], asession),
                lambda: self.get_product_details(self.links[i + 6], asession),
                lambda: self.get_product_details(self.links[i + 7], asession),
                lambda: self.get_product_details(self.links[i + 8], asession),
                lambda: self.get_product_details(self.links[i + 9], asession),
            ))
            print("Scraping ", i + NUMBER_OF_LAMBDA_FUNCTIONS, "/", len(self.links))
        for i in range(len(self.results)):
            for j in range(len(self.results[0])):
                self.attributes.append(self.results[i][j])

    async def get_product_details(self, links, asession):
        """Gets all product details after opening the prepared links in the async function 

        Args:
            link (Int): Contains the link that is prepared for scarping 
            asession (object): session created by the library for the html page that is opened 

        Returns:
            [Tuple]: Returns everything that is scraped such as price and name of product. Return of this type can contain different variable types 
        """

        items = [0] * 6
        items[0] = links  # Sets column 0 to links
        url = 'http://shopee.sg/load-i.' + links

        if 'IGNORE' in url:
            return ['IGNORE']

        webpage = await asession.get(url, headers=self.HEADERS)
        await webpage.html.arender(sleep=2, timeout=50, scrolldown=True)

        try:
            for item in webpage.html.xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]/span'):
                items[1] = item.text.replace(",", "")
            if items[1] == 0:
                for item in webpage.html.xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]'):
                    items[1] = item.text.replace(",", "")
        except:
            pass

        try:
            for item in webpage.html.xpath(
                    '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div[2]/div[1]'):
                items[2] = item.text.replace(",", "")
            if items[2] == 0:
                for item in webpage.html.xpath(
                        '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div/div'):
                    items[2] = item.text.replace(",", "")
            if '%' in items[2]:
                for item in webpage.html.xpath(
                        '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div[2]/div[1]'):
                    items[2] = item.text.replace(",", "")
        except:
            pass

        try:
            for item in webpage.html.xpath(
                    '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[1]'):
                items[3] = item.text
        except:
            pass

        try:
            for item in webpage.html.xpath(
                    '//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[2]/div[1]'):
                items[4] = item.text.replace(".", "").replace("k", "000")
        except:
            pass

        try:
            for item in webpage.html.xpath(
                    '//*[contains(concat( " ", @class, " " ), concat( " ", "flex items-center _90fTvx", ''" " ))]'):
                items[5] = re.sub('\D', '', str(item.text))
        except:
            pass

        if items[1] == 0:  # When GET fails
            items[1] = "FAILED TO GET"
        if items[2] == 0 or items[2] == '' or '%' in items[2]:
            items[2] = "FAILED TO GET"
        if items[3] is None:
            items[3] = "0"
        if items[4] is None:
            items[4] = "0"
        if items[5] is None:
            items[5] = "0"

        return tuple(items)

    def store_product_details(self):
        """Stores all the details of the scraped product from the get_product_details function into a csv file 

        Returns:
          [String]: File name of the file that all the details of the scraped product is stored.
        """
        file_name = 'shopee-scrape.csv'
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(self.attributes)

        return file_name
