from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import re
import csv

class amazon_review_scraper:
    """This class scraps the reviews of the user selected product that is scraped and stored as well.
    """
    HEADERS = ({'User-Agent':
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.2403.157 "
                    "Safari/537.36",
                'Accept-Language': 'en-US, en;q=0.5'})

    def __init__(self, link):
        """This function is for self defined parameters for storage purposes
        """
        self.link = link
        self.reviews = [[],[],[],[],[]]

    def asynchronousProcessing(self):
        """This function waits and scraps all the review of the selected product fron the GUI.
                asession : creates a html session for the scarping of data
        """
        asession = AsyncHTMLSession()

        asession.run(  # Calls 5 requests (PROCESSES) in 1 go
            lambda: self.get_product_reviews(self.link, asession, 5),
            lambda: self.get_product_reviews(self.link, asession, 4),
            lambda: self.get_product_reviews(self.link, asession, 3),
            lambda: self.get_product_reviews(self.link, asession, 2),
            lambda: self.get_product_reviews(self.link, asession, 1),
        )

    async def get_product_reviews(self, links, asession, rating):
        """This function scraps the link of the product that the user has specified and extract all the reviews from that particular link.

        Args:
            links ([Int]): Unique ID of the product.
            asession ([object]): Parse a session for the html page.
            rating ([string]): Rating from the reviews that are scraped.
        """

        # Simple function to determine number of pages to scrape.
        def review_pages(string):
            n = int(string)
            a = (n // 10)

            if a > 5:
                a = 5
            if a == 0:
                a = 1

            return a

        # Determine star setting for scraping.
        if rating == 5:
            star = 'five_star'
        elif rating == 4:
            star = 'four_star'
        elif rating == 3:
            star = 'three_star'
        elif rating == 2:
            star = 'two_star'
        elif rating == 1:
            star = 'one_star'

        pagenumber = 1
        url = 'https://www.amazon.com/product-reviews/' + links + '/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(pagenumber) + '&sortBy=recent&filterByStar=' + star

        # Request the URL using the session.
        webpage = await asession.get(url, headers=self.HEADERS)
        await webpage.html.arender(sleep=1, timeout=50)
        soup = BeautifulSoup(webpage.content, "lxml")

        # Find available number of pages to scrape.
        count = soup.find('div', attrs={'class':'a-row a-spacing-base a-size-base'})
        rating_count = count.text.split('|')
        real_count = review_pages(re.sub('\D', '', str(rating_count[1])))

        # For loop for scraping reviews.
        for i in range(1, real_count+1):

            # Sort by star setting and recent.
            url = 'https://www.amazon.com/product-reviews/' + links + '/ref=cm_cr_arp_d_viewopt_sr?ie=UTF8&reviewerType=all_reviews&pageNumber=' + str(i) + '&sortBy=recent&filterByStar=' + star

            webpage_scrape = await asession.get(url, headers=self.HEADERS)
            await webpage_scrape.html.arender(sleep=1, timeout=50)
            soup = BeautifulSoup(webpage_scrape.content, "lxml")

            reviews_scrape = soup.find_all('span', attrs={'class': 'a-size-base review-text review-text-content'})

            # Parse all reviews through text cleaning.
            for r in reviews_scrape:
                review_stripped = re.sub('\s{2,}', ' ', r.text)
                self.reviews[rating-1].append(review_stripped)

    def store_product_reviews(self):
        """This function stores all the details such as comment and stars including the product ID of the scraped review into a file. 
        """
        file_name = str('reviews/'+self.link + '.csv')
        fieldnames = ['Rating', 'Reviews']
        with open(file_name, 'a', encoding="utf-8", newline='') as filewriter:
            writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(self.reviews)):
                for j in range(len(self.reviews[i])):
                    writer.writerow({'Rating': str(i + 1), 'Reviews': str(self.reviews[i][j]).replace(',','')})
        print("Review scrape completed for " + str(self.link) + " saved as " + file_name)
