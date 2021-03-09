import requests
import csv
import re
from requests_html import AsyncHTMLSession
from abstract_product_scraper import abstract_product_scraper

class shopee_product_scraper(abstract_product_scraper):

    ITEMS_PER_PAGE = 50

    def __init__(self, url_file):
        self.file = url_file
        self.links = []
        self.results = []
        self.attributes = []

    def get_product_links(self):
        with open(self.file) as file_reader:
            self.links = file_reader.read().splitlines()

    def asynchronousProcessing(self):
        NUMBER_OF_LAMBDA_FUNCTIONS = 5
        asession = AsyncHTMLSession()
        print("Commencing asynchronous requests")
        print("Number of requesting processes set to 5")

        # If not multiple of 5s, add empty links that will not be processed by lambda function.
        remainder = len(self.links) % 5
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

    async def get_product_details(self, links, asession):

        items = [None] * 6
        items[0] = links
        url = 'http://shopee.sg/load-i.' + links

        if 'IGNORE' in url:
            return ['IGNORE']

        webpage = await asession.get(url, headers=self.HEADERS)
        await webpage.html.arender(sleep=1, timeout=50)

        for item in webpage.html.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_3ZV7fL", " " ))]//span'):
            items[1] = item.text.replace(",", "")
        for item in webpage.html.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "AJyN7v", " " ))]'):
            items[2] = item.text
        for item in webpage.html.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_22cC7R", " " ))]'):
            items[3] = item.text
        for item in webpage.html.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "_3WXigY", ''" " ))]'):
            items[4] = item.text
        for item in webpage.html.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "flex items-center _2_ItKR", ''" " ))]'):
            items[5] = re.sub('\D', '', str(item.text))

        if items[1] is None:  # When GET fails
            items[1] = "FAILED TO GET"
        if items[2] is None:
            items[2] = "FAILED TO GET"
        if items[3] is None:
            items[3] = "0"
        if items[4] is None:
            items[4] = "0"
        if items[5] is None:
            items[5] = "0"

        return tuple(items)

    def store_product_details(self):
        with open('output-shopee.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(self.attributes)