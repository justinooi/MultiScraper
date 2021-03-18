from abc import ABC, abstractclassmethod

# Abstract class for scraping links
class abstract_link_scraper(ABC):

    searchParameters = ""
    pages = 0
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
    links_list = []

    def userInput(self, searchParameters):
        self.searchParameters = searchParameters
        self.pages = 1

    def linkSearch(self):
        pass

    def storeUrl(self):
        pass
