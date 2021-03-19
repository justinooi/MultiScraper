from bs4 import BeautifulSoup
import requests
from abstract_link_scraper import abstract_link_scraper
import time
import re

class amazon_link_scraper(abstract_link_scraper):
    """Link scraper gets all the Unique ID of the product search that is specified in the GUI by the user and store it to a file.

    Args:
        abstract_product_scraper (Object): user define abstract class defining the properties of how the product scaper should function.
    """

    def linkSearch(self):
        """extracts all the unique id from the URL which will be the product ID to scrape from.
        """
        # Retrieve all product ASIN (unique product ID)
        try:
            for x in range(1):
                URL = "https://www.amazon.com/s?k=" + self.searchParameters + "&page=" + str(x)
                print(URL)
                webpage = requests.get(URL, headers=self.HEADERS)
                soup = BeautifulSoup(webpage.content, "lxml")
                search_results = soup.find_all('a', attrs={'class': 'a-link-normal a-text-normal'})
                counter = 0

                # Loop for extracting links from Tag Objects
                for link in search_results:
                    link = link.get('href')

                    if '/gp/slredirect/' in link:
                        continue
                    else:
                        asin = re.search(r'/[dg]p/([^/]+)', link, flags=re.IGNORECASE).group(1)
                        self.links_list.append(asin)
                    counter=counter+1
                    if counter == self.itemQuantity:
                        break



            self.storeUrl()

        except AttributeError:
            links = []

    def storeUrl(self):
        """Stores all the unique ID to a file into the specified directory

        Returns:
            [String]: return the file name that the data is stored in.
        """
        with open('amazon_urls.txt', 'w') as url_storage:
            for link in self.links_list:
                url_storage.write(link + '\n')
        self.links_list.clear()
        return 'amazon_urls.txt'
