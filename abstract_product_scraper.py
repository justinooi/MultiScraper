from abc import ABC, abstractmethod

class abstract_product_scraper(ABC):
    HEADERS = ({'User-Agent':
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.2403.157 "
                    "Safari/537.36",
                'Accept-Language': 'en-US, en;q=0.5'})

    @abstractmethod
    def get_product_links(self):
        pass

    @abstractmethod
    def asynchronousProcessing(self):
        pass

    @abstractmethod
    async def get_product_details(self, links, asession):
        pass

    @abstractmethod
    def store_product_details(self):
        pass