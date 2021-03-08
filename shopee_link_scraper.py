from bs4 import BeautifulSoup
from abstract_link_scraper import abstract_link_scraper
import time
import requests


class shopee_link_scraper(abstract_link_scraper):
    identificationParams = []
    items_per_page = 50

    def linkSearch(self):

        try:
            for x in range(int(self.pages)):
                print("Getting item identification numbers from page:", x)
                time.sleep(1)
                url = 'https://shopee.sg/api/v2/search_items/?by=relevancy&keyword=' + self.searchParameters + '&limit=50&newest=' + str(
                    self.items_per_page) + '&order=desc&page_type=search'  # Base URL
                r = requests.get(url, headers=self.HEADERS).json()
                for item in r['items']:  # Store name, price, stocks left and amount sold in respective lists
                    self.identificationParams.append((item['shopid'], item['itemid']))
                self.items_per_page += 50
            time.sleep(1)
            print("Item identification numbers received")
            time.sleep(1)
        except AttributeError:
            self.identificationParams = []

    def storeUrl(self):
        for x in range(len(self.identificationParams)):
            self.links_list.append("http://shopee.sg/load-i." + str(self.identificationParams[x][0]) + '.' + str(
                self.identificationParams[x][1]))
        print("Links created")
        with open('shopee_urls.txt', 'a') as url_storage:
            for link in self.links_list:
                url_storage.write(link + '\n')

sls = shopee_link_scraper()
sls.userInput()
sls.linkSearch()
sls.storeUrl()
