from bs4 import BeautifulSoup
import requests
from abstract_link_scraper import abstract_link_scraper
import time


class amazon_link_scraper(abstract_link_scraper):

    def linkSearch(self):

        # Retrieve all product links
        try:
            for x in range(1, int(self.pages)+1):
                URL = "https://www.amazon.com/s?k=" + self.searchParameters + "&page=" + str(x)
                print(URL)
                webpage = requests.get(URL, headers=self.HEADERS)
                soup = BeautifulSoup(webpage.content, "lxml")
                search_results = soup.find_all('a', attrs={'class': 'a-link-normal a-text-normal'})

                # Loop for extracting links from Tag Objects
                for link in search_results:
                    self.links_list.append(link.get('href'))

                # Time delay to prevent bot detection
                time.sleep(1)

        except AttributeError:
            links = []

    def storeUrl(self):
        with open('amazon_urls.txt', 'a') as url_storage:
            for link in self.links_list:
                url_storage.write(link + '\n')