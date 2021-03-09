from abc import ABC, abstractclassmethod

class abstract_product_scraper(ABC):
    HEADERS = ({'User-Agent':
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 "
                    "Safari/537.36",
                'Accept-Language': 'en-US, en;q=0.5'})

    def get_product_links(self):
        pass

    def asynchronousProcessing(self):
        pass

    async def get_product_details(self, links, asession):
        pass

    def store_product_details(self):
        pass