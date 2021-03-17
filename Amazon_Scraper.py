from amazon_link_scraper import amazon_link_scraper
from amazon_review_scraper import amazon_review_scraper
from amazon_product_scraper import amazon_product_scraper

class Amazon_Scraper(amazon_product_scraper, amazon_link_scraper, amazon_review_scraper):

    def __init__(self):
        self.scraper = 'Amazon'

    def linkScrape(self, searchParameter):
        super().userInput(searchParameter)
        super().linkSearch()
        return super().storeUrl()

    def productScrape(self, url_file):
        amazon_product_scraper.__init__(self, url_file)
        amazon_product_scraper.get_product_links(self)
        amazon_product_scraper.asynchronousProcessing(self)
        return amazon_product_scraper.store_product_details(self)

    def reviewScrape(self, url):
        amazon_review_scraper.__init__(self, url)
        amazon_review_scraper.asynchronousProcessing(self)
        amazon_review_scraper.store_product_reviews(self)

    def reviewScrapeAll(self, url_file):
        with open(url_file) as file_reader:
            links = file_reader.read().splitlines()

        for i in range(len(links)):
            self.reviewScrape(links[i])