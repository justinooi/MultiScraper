import csv
import ctypes
from Shopee_Scraper import Shopee_Scraper
from Amazon_Scraper import Amazon_Scraper
from Sentiment_Analysis import Sentiment_Analysis

class storageHandler:
    items = []

    def initialization(self, itemList):
        self.deleteAll(itemList)
        self.csvReader()
        self.displayItems(itemList)

    def sortParams(self, input, itemList):
        if input == "None":
            pass

        elif input == "ID":
            self.deleteAll(itemList)
            self.csvReader()
            self.sortByID()
            self.displayItems(itemList)

        elif input == "Name":
            self.deleteAll(itemList)
            self.csvReader()
            self.sortByName()
            self.displayItems(itemList)

        elif input == "Price":
            self.deleteAll(itemList)
            self.csvReader()
            self.sortByPrice()
            self.displayItems(itemList)

        elif input == "Rating":
            self.deleteAll(itemList)
            self.csvReader()
            self.sortByRating()
            self.displayItems(itemList)

        elif input == "Rating Count":
            self.deleteAll(itemList)
            self.csvReader()
            self.sortByRatingQuantity()
            self.displayItems(itemList)

        elif input == "Stock Info":
            self.deleteAll(itemList)
            self.csvReader()
            self.sortByQuantityLeft()
            self.displayItems(itemList)

    def sortByID(self):
        self.items.sort(key=lambda x: str(x[0]), reverse=True)

    def sortByName(self):
        self.items.sort(key=lambda x: str(x[1]), reverse=False)

    def sortByPrice(self):
        self.items.sort(key=lambda x: float(
            x[2].replace("$", "") if " - " not in str(x[2]) else x[2].replace("$", "").split(" - ")[0]), reverse=True)

    def sortByRating(self):
        self.items.sort(key=lambda x: float(x[3]), reverse=False)

    def sortByRatingQuantity(self):
        self.items.sort(key=lambda x: float(x[4]), reverse=False)


    def sortByQuantityLeft(self):
        self.items.sort(key=lambda x: str(x[5]) , reverse=True)

    def csvReader(self):
        self.items=[]
        try:
            with open('shopee-scrape.csv', 'r', newline='',
                      encoding='utf-8') as items:  # Open shopee.csv file (must be same directory as this program)
                for row in items:
                    if not "FAILED TO GET" in row or not "" in row:  # Rejects data with "FAILED TO GET"
                        if row not in self.items:
                            if str(row.split(",")[0]) not in str(self.items):  # Removes duplicates via ID
                                self.items.append(list(row.split(",")))
        except:
            pass

        try:
            with open('output-amazon.csv', 'r', newline='',
                      encoding='utf-8') as items:  # Open shopee.csv file (must be same directory as this program)
                for row in items:
                    if ("N/A" not in row) and ("IGNORE" not in row): #Rejects invalid data
                        if str(row.split(",")[0]) not in str(self.items): #Removes duplicates via ID
                            self.items.append(list(row.split(",")))
        except:
            pass

        for i in range(len(self.items)):
            self.items[i][3] = self.items[i][3].replace("out of 5 stars","")
            self.items[i][4] = self.items[i][4].replace("ratings","")
            if self.items[i][5] == "\r\n":  # Removes NULL values
                self.items[i][5] = "0"

    def displayItems(self, itemList):
        for i, column in enumerate(self.items, start=0):
            itemList.insert("", 0, values=(self.items[i]))

    def deleteAll(self, itemList):
        itemList.delete(*itemList.get_children())

    def saveData(self, savedItem):
        duplicate_detection = [None]
        duplicate_flag = False

        if savedItem == "":
            print("?")
            return 0

        with open('savedItems.csv', 'r', newline='',
                  encoding='utf-8') as savedItemsIO:
            for row in savedItemsIO:
                if '"\r\n' not in row:
                    duplicate_detection.append(row)

        for x in range(len(duplicate_detection)):
            try:
                if savedItem[0] == duplicate_detection[x].split(",")[0]:
                    duplicate_flag = True
            except:
                pass

        if duplicate_flag == False:
            with open('savedItems.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(savedItem.replace('\n',''))

        else:
            ctypes.windll.user32.MessageBoxW(0, "You've already saved this item", "", 1)

    def showFavourites(self, itemList):
        savedItem = []
        with open('savedItems.csv', 'r', newline='',
                  encoding='utf-8') as savedItemsIO:
            for row in savedItemsIO:
                if '"\r\n' not in row:
                    savedItem.append(row.split(","))

        for i, column in enumerate(savedItem, start=0):
            itemList.insert("", 0, values=(savedItem[i]))

    def deleteAllFavourites(self, itemList):
        with open('savedItems.csv', 'w', newline='', encoding='utf-8') as f:
            pass
        itemList.delete(*itemList.get_children())

    def deleteFiles(self):
        with open('output-amazon.csv', 'w', newline='', encoding='utf-8') as f:
            pass
        with open('shopee-scrape.csv', 'w', newline='', encoding='utf-8') as f:
            pass

    def readReview(self, itemID, itemList):

        reviewItem=[]

        try:
            with open('reviews/'+itemID+'.csv', 'r', newline='',
                      encoding='utf-8') as IO:
                for row in IO:
                    if '"\r\n' not in row:
                        reviewItem.append(row.split(","))


        except:
            if self.is_number(itemID) == True:
                Shopee_Scraper().reviewScrape(itemID)

            else:
                Amazon_Scraper().reviewScrape(itemID)

            with open('reviews/'+itemID+'.csv', 'r', newline='',
                      encoding='utf-8') as IO:
                for row in IO:
                    reviewItem.append(row.split(","))


        for i, column in enumerate(reviewItem, start=0):
            itemList.insert("", 0, values=(reviewItem[i]))


    def is_number(self, itemID):
        """
        Check if itemID is float or not. If it is a float, it is a shopee ID. Else, amazon ID.
        :param itemID:
        :return:
        """
        try:
            float(itemID)
        except ValueError:
            return False
        return True

    def readSentiment(self, itemID, itemList):
        sentimentItem = []
        try:
            with open('sentiments/'+str(itemID)+'.csv', 'r', newline='',
                      encoding='utf-8') as IO:
                for row in IO:
                    if '"\r\n' not in row:
                        sentimentItem.append(row.split(","))

        except:
            Sentiment_Analysis().analyze(str(itemID)+'.csv')
            with open('sentiments/'+itemID+'.csv', 'r', newline='',
                      encoding='utf-8') as IO:
                for row in IO:
                    if '"\r\n' not in row:
                        sentimentItem.append(row.split(","))


        for i, column in enumerate(sentimentItem, start=0):
            itemList.insert("", 0, values=(sentimentItem[i]))








