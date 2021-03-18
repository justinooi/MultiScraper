from bs4 import BeautifulSoup
from abstract_link_scraper import abstract_link_scraper
import time
import requests


class shopee_link_scraper(abstract_link_scraper):
    identificationParams = []
    items_per_page = 50

    def linkSearch(self):

        try:
            url = 'https://shopee.sg/api/v2/search_items/?by=relevancy&keyword=' + self.searchParameters + '&limit=' + str(
                self.itemQuantity) + '&newest=' + str(
                self.items_per_page) + '&order=desc&page_type=search'  # Base URL
            print(url)
            r = requests.get(url, headers=self.HEADERS).json()
            for item in r['items']:  # Store name, price, stocks left and amount sold in respective lists
                self.identificationParams.append((item['shopid'], item['itemid']))
        except AttributeError:
            self.identificationParams = []

    def storeUrl(self):

        for x in range(len(self.identificationParams)):
            self.links_list.append(str(self.identificationParams[x][0]) + '.' + str(self.identificationParams[x][1]))
        print("Links created")
        with open('shopee_urls.txt', 'w') as url_storage:
            for link in self.links_list:
                url_storage.write(link + '\n')

        self.links_list.clear()
        return 'shopee_urls.txt'
