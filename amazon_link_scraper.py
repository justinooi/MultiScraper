from bs4 import BeautifulSoup
import requests
from abstract_link_scraper import abstract_link_scraper


class amazon_link_scraper(abstract_link_scraper):

    def linkSearch(self):

        URL = "https://www.amazon.com/s?k=" + self.searchParameters

        # Making the HTTP Request
        webpage = requests.get(URL, headers=self.HEADERS)

        # Creating the Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "lxml")

        # Retrieve all product links
        try:
            search_results = soup.find_all('a', attrs={'class': 'a-link-normal a-text-normal'})

            # Loop for extracting links from Tag Objects
            for link in search_results:
                self.links_list.append(link.get('href'))

        except AttributeError:
            links = []

    def storeUrl(self):
        with open('amazon_urls.txt', 'a') as url_storage:
            for link in self.links_list:
                url_storage.write(link + '\n')