from bs4 import BeautifulSoup
import requests
from abstract_link_scraper import abstract_link_scraper
import time
import re

class amazon_link_scraper(abstract_link_scraper):

    def linkSearch(self):

        # Retrieve all product ASIN (unique product ID)
        try:
            for x in range(1, int(self.pages)+1):
                URL = "https://www.amazon.com/s?k=" + self.searchParameters + "&page=" + str(x)
                print(URL)
                webpage = requests.get(URL, headers=self.HEADERS)
                soup = BeautifulSoup(webpage.content, "lxml")
                search_results = soup.find_all('a', attrs={'class': 'a-link-normal a-text-normal'})

                # Loop for extracting links from Tag Objects
                for link in search_results:
                    link = link.get('href')
                    if '/gp/slredirect/' in link:
                        continue
                    else:
                        asin = re.search(r'/[dg]p/([^/]+)', link, flags=re.IGNORECASE).group(1)
                        self.links_list.append(asin)

            self.storeUrl()

        except AttributeError:
            links = []

    def storeUrl(self):
        with open('test.txt', 'a') as url_storage:
            for link in self.links_list:
                url_storage.write(link + '\n')


if __name__ == '__main__':
    ALS = amazon_link_scraper()
    ALS.userInput()
    ALS.linkSearch()