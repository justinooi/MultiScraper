from shopee_link_scraper import shopee_link_scraper
from shopee_review_scraper import shopee_review_scraper
from shopee_product_scraper import shopee_product_scraper

class Shopee_Scraper(shopee_product_scraper, shopee_link_scraper, shopee_review_scraper):

    def __init__(self):
        self.scraper = 'Shopee'

    def linkScrape(self):
        super().userInput()
        super().linkSearch()
        return super().storeUrl()

    def productScrape(self, url_file):
        shopee_product_scraper.__init__(self, url_file)
        shopee_product_scraper.get_product_links(self)
        shopee_product_scraper.asynchronousProcessing(self)
        return shopee_product_scraper.store_product_details(self)

    def reviewScrape(self, url):
        shopee_review_scraper.__init__(self, url)
        shopee_review_scraper.asynchronousProcessing(self)
        shopee_review_scraper.store_product_reviews(self)

    def reviewScrapeAll(self, url_file):
        with open(url_file) as file_reader:
            links = file_reader.read().splitlines()

        for i in range(len(links)):
            shopee_review_scraper.__init__(self, links[i])
            shopee_review_scraper.asynchronousProcessing(self)
            shopee_review_scraper.store_product_reviews(self)
