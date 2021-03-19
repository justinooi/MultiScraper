from abc import ABC, abstractmethod

class abstract_product_scraper(ABC):
    """Abstract class and method for the shoppee and amazon scraper. This class will allow both having common API methods to function accordingly to what the abstract method allows.

    Args:
        ABC (object): make the class an abstract class
    """

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