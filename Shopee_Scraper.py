from shopee_link_scraper import shopee_link_scraper
from shopee_review_scraper import shopee_review_scraper
from shopee_product_scraper import shopee_product_scraper

class Shopee_Scraper(shopee_product_scraper, shopee_link_scraper, shopee_review_scraper):
    """This class inherits all abstract classes and methods for the functions of GUI 

    Args:
        shopee_product_scraper (subclass): child class which allows access to all methods in the class
        shopee_link_scraper (subclass): child class which allows access to all methods in the class
        shopee_review_scraper (subclass): child class which allows access to all methods in the class
    """

    def __init__(self):
        self.scraper = 'Shopee'

    def linkScrape(self, searchParameter, itemQuantity):
        """This function is called upon clicking the submit button, managing the calling of various functions in the base class, 
           userInput(): to pass in searchParameter and itemQuantity for encapsulation
           linkSearch(): to retrieve the unique identifier of products 

        Args:
            searchParameter (str): name of product user searched for
            itemQuantity (int): number of items

        Returns:
            function -> str: calls the function storeUrl() 
        """

        super().userInput(searchParameter, itemQuantity)
        super().linkSearch()
        return super().storeUrl()

    def productScrape(self, url_file):
        """This function is called upon clicking the submit button, managing the calling of various functions in other sub classes, 
           shopee_product_scraper class:
                init class with file, links, results and attributes
                get_product_links(): to get and store the links of the products
                asynchronousProcessing(): to wait for a specified number of tasks to complete before continuing                             

        Args:
            url_file (str): text file that was returned from linkScrape()

        Returns:
            function : calls the function store_product_details() 
        """

        shopee_product_scraper.__init__(self, url_file)
        shopee_product_scraper.get_product_links(self)
        shopee_product_scraper.asynchronousProcessing(self)
        return shopee_product_scraper.store_product_details(self)
        
    def reviewScrape(self, url):
        """This function is called upon clicking the submit button, managing the calling of various functions in other sub classes,
           shoppee_review_scraper class:
                init class with file, links, results and attributes
                asynchronousProcessing(): to wait for a specified number of tasks to complete before continuing the review scaping and store it to a text file     
                store_product_reviews: Get all stored scraped review

        Args:
            url (Int): get url(Product ID) from the main page selected product by ther user.
        """
        shopee_review_scraper.__init__(self, url)
        shopee_review_scraper.asynchronousProcessing(self)
        shopee_review_scraper.store_product_reviews(self)

    def reviewScrapeAll(self, url_file):
        """This function opens the saved data file of products that is scraped and saved by the user.

        Args:
            url_file (String): The file path of the saved data file of the user scraped data 
        """
        with open(url_file) as file_reader:
            links = file_reader.read().splitlines()

        for i in range(len(links)):
            shopee_review_scraper.__init__(self, links[i])
            shopee_review_scraper.asynchronousProcessing(self)
            shopee_review_scraper.store_product_reviews(self)
