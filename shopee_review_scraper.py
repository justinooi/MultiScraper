import csv
from requests_html import AsyncHTMLSession


class shopee_review_scraper:
    HEADERS = ({'User-Agent':
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 "
                    "Safari/537.36",
                'Accept-Language': 'en-US, en;q=0.5'})

    def __init__(self, link):
        self.link = link
        self.reviews = [[],[],[],[],[]]

    def asynchronousProcessing(self):
        NUMBER_OF_LAMBDA_FUNCTIONS = 5
        asession = AsyncHTMLSession()
        print("Commencing asynchronous requests")
        print("Number of requesting processes set to 5")

        asession.run(  # Calls 5 requests (PROCESSES) in 1 go
            lambda: self.get_product_reviews(self.link, asession, 5),
            lambda: self.get_product_reviews(self.link, asession, 4),
            lambda: self.get_product_reviews(self.link, asession, 3),
            lambda: self.get_product_reviews(self.link, asession, 2),
            lambda: self.get_product_reviews(self.link, asession, 1),
        )

    async def get_product_reviews(self, links, asession, rating):

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

        fieldnames = ['Rating', 'Review']
        with open('shopee-reviews.csv', 'a', encoding="utf-8", newline='') as filewriter:
            writer = csv.DictWriter(filewriter, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(self.reviews)):
                for j in range(len(self.reviews[i])):
                    writer.writerow({'Rating': str(i+1), 'Review': str(self.reviews[i][j])})

if __name__ == '__main__':
    srs = shopee_review_scraper('79840464.3819155989')
    srs.asynchronousProcessing()
    srs.store_product_reviews()