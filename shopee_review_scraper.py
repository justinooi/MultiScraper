import csv
from requests_html import AsyncHTMLSession

class shopee_review_scraper:
    """This class scraps the reviews of the user selected product that is scraped and stored as well.
    """
    HEADERS = ({'User-Agent':
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 "
                    "Safari/537.36",
                'Accept-Language': 'en-US, en;q=0.5'})

    def __init__(self, link):
        """User define parameters for storage purposes
        """
        self.link = link
        self.reviews = [[],[],[],[],[]]

    def asynchronousProcessing(self):
        """Aynsc function that waits scraps all the review of the selected product fron the GUI.
                asession : creates a html session for the scarping of data
                NUMBER_OF_LAMBDA_FUNCTIONS : set the limit of request calls wanted per cycle 
        """
        NUMBER_OF_LAMBDA_FUNCTIONS = 5
        asession = AsyncHTMLSession()

        asession.run(  # Calls 5 requests (PROCESSES) in 1 go
            lambda: self.get_product_reviews(self.link, asession, 5),
            lambda: self.get_product_reviews(self.link, asession, 4),
            lambda: self.get_product_reviews(self.link, asession, 3),
            lambda: self.get_product_reviews(self.link, asession, 2),
            lambda: self.get_product_reviews(self.link, asession, 1),
        )

    async def get_product_reviews(self, links, asession, rating):
        """Scraps the link of the product that the user has specified and extract all the reviews from that particular link.

        Args:
            links ([Int]): Unique ID of the product.
            asession ([object]): Create a session for the html page.
            rating ([string]): Rating from the reviews that are scraped.
            comment ([string]) : comment of the reviews that are scraped 
        """
        ids = links.split('.')
        shop_id = ids[0]
        product_id = ids[1]

        url = "https://shopee.sg/api/v2/item/get_ratings?filter=0&flag=1&itemid=" + \
              product_id + "&limit=59&offset=0&shopid=" + shop_id + '&type=' + str(rating)

        webpage = await asession.get(url, headers=self.HEADERS)
        webpage = webpage.json()

        for item in webpage['data']['ratings']:
            if item['comment'] == '':
                if item['rating_star'] == '':
                    continue
                else:
                    review_str = item['rating_star']
                    self.reviews[rating - 1].append(review_str)
            else:
                review_str = item['comment']
                self.reviews[rating - 1].append(review_str)

    def store_product_reviews(self):
        """Stores all the details such as comment and stars including the product ID of the scraped review into a file. 
        """
        file_name = str('reviews/'+self.link + '.csv')
        fieldnames = ['Rating', 'Reviews']
        with open(file_name, 'w', encoding="utf-8", newline='') as filewriter:
            writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(self.reviews)):
                for j in range(len(self.reviews[i])):
                    writer.writerow({'Rating': str(i+1), 'Reviews': str(self.reviews[i][j]).replace('\n',"").replace(',',"")})
        print("Review scrape completed for " + str(self.link) + " saved as " + file_name)