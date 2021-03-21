from amazon_link_scraper import amazon_link_scraper
from amazon_review_scraper import amazon_review_scraper
from amazon_product_scraper import amazon_product_scraper

class Amazon_Scraper(amazon_product_scraper, amazon_link_scraper, amazon_review_scraper):
    """This class inherits all abstract classes
    Args:
        amazon_product_scraper (subclass): child class which allows access to all methods in the class
        amazon_link_scraper (subclass): child class which allows access to all methods in the class
        amazon_review_scraper (subclass): child class which allows access to all methods in the class
    """

    def __init__(self):
        self.scraper = 'Amazon'

    def linkScrape(self, searchParameter, itemQuantity):
        """This method is called upon clicking the submit button, managing the calling of various methods in the base class, 
           userInput(): to pass in searchParameter and itemQuantity for encapsulation
           linkSearch(): to retrieve the unique identifier of products 

        Args:
            searchParameter (str): name of product user searched for
            itemQuantity (int): number of items

        Returns:
            method -> str: calls the method storeUrl() 
        """
        super().userInput(searchParameter, itemQuantity)
        super().linkSearch()
        return super().storeUrl()

    def productScrape(self, url_file):
        """This method is called upon clicking the submit button, managing the calling of various methods in other sub classes, 
           amazon_product_scraper class:
                init class with file, links, results and attributes
                get_product_links(): to get and store the links of the products
                asynchronousProcessing(): to wait for a specified number of tasks to complete before continuing                             

        Args:
            url_file (str): text file that was returned from linkScrape()

        Returns:
            method : calls the method store_product_details() 
        """
        amazon_product_scraper.__init__(self, url_file)
        amazon_product_scraper.get_product_links(self)
        amazon_product_scraper.asynchronousProcessing(self)
        return amazon_product_scraper.store_product_details(self)

    def reviewScrape(self, url):
        """This method is called upon clicking the submit button, managing the calling of various methods in other sub classes,
                Amazon_review_scraper class:
                init class with file, links, results and attributes
                asynchronousProcessing(): to wait for a specified number of tasks to complete before continuing the review scaping and store it to a text file   
                store_product_reviews: Get all stored scraped review
        Args:
            url (Int): get url(Product ID) from the main page selected product by ther user.
        """
        amazon_review_scraper.__init__(self, url)
        amazon_review_scraper.asynchronousProcessing(self)
        amazon_review_scraper.store_product_reviews(self)

    def reviewScrapeAll(self, url_file):
        """This method opens the saved data file of products that is scraped and saved by the user.

        Args:
            url_file (String): The file path of the saved data file of the user scraped data 
        """
        with open(url_file) as file_reader:
            links = file_reader.read().splitlines()

        for i in range(len(links)):
            self.reviewScrape(links[i])
