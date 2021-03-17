import requests
import csv
import time
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

        items = [None] * 6
        items[0] = links #Sets column 0 to links
        url = 'http://shopee.sg/load-i.' + links

        if 'IGNORE' in url:
            return ['IGNORE']

        webpage = await asession.get(url, headers=self.HEADERS)
        await webpage.html.arender(sleep=2, timeout=50, scrolldown=True)

        for item in webpage.html.xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[1]/span'):
            items[1] = item.text.replace(",", "")
        for item in webpage.html.xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[3]/div/div/div/div/div/div[1]'):
            items[2] = item.text
        for item in webpage.html.xpath('/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[1]/div[1]'):
            items[3] = item.text
        for item in webpage.html.xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[2]/div[2]/div[1]'):
            items[4] = item.text
        for item in webpage.html.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "aPKXeO", " " )) and (((count(preceding-sibling::*) + 1) = 3) and parent::*)]//div'):
            items[5] = re.sub('\D', '', str(item.text))
        if items[5] is None:
            for item in webpage.html.xpath('//*[@id="main"]/div/div[2]/div[2]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div'):
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
        #file_name = 'shopee-scrape-' + str(time.time()) + '.csv'
        file_name = 'shopee-scrape.csv'
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(self.attributes)

        return file_name