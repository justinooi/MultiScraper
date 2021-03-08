import requests
import time
from requests_html import AsyncHTMLSession
from abstract_product_scraper import abstract_product_scraper
from bs4 import BeautifulSoup

class amazon_product_scraper(abstract_product_scraper):

    def __init__(self, url_file):
        self.file = url_file
        self.product_links = []
        self.results = []

    def get_product_links(self):
        with open(self.file) as file_reader:
            links = file_reader.read().splitlines()
            self.product_links = ["https://amazon.com/dp/" + s for s in links]

    def asynchronousProcessing(self):
        pass

    async def get_product_details(self, link, asession):
        pass


if __name__ == '__main__':
    aps = amazon_product_scraper('test.txt')
    aps.get_product_links()
    aps.asynchronousProcessing()