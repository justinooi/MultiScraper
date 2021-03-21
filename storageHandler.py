import csv
import ctypes
import webbrowser
from Shopee_Scraper import Shopee_Scraper
from Amazon_Scraper import Amazon_Scraper
from Sentiment_Analysis import Sentiment_Analysis

class storageHandler:
    """This class manages the manipulation of data in the file storages
    """
    items = []

    def initialization(self, itemList):
        """This method refreshes product details in the GUI

        Args:
            itemList (treeview): the details of the products
        """
        self.deleteAll(itemList)
        self.csvReader(0)
        self.displayItems(itemList)
        with open('savedItems.csv','a') as fw:
            pass

    def sortParams(self, input, itemList, sortflag):
        """This method manages the sorting of products

        Args:
            input (str): user input of the type of sort
            itemList (treeview): the details of the products
        """
        if input == "None":
            pass

        elif input == "ID":
            self.deleteAll(itemList)
            self.csvReader(sortflag)
            self.sortByID()
            self.displayItems(itemList)

        elif input == "Name":
            self.deleteAll(itemList)
            self.csvReader(sortflag)
            self.sortByName()
            self.displayItems(itemList)

        elif input == "Price":
            self.deleteAll(itemList)
            self.csvReader(sortflag)
            self.sortByPrice()
            self.displayItems(itemList)

        elif input == "Rating":
            self.deleteAll(itemList)
            self.csvReader(sortflag)
            self.sortByRating()
            self.displayItems(itemList)

        elif input == "Rating Count":
            self.deleteAll(itemList)
            self.csvReader(sortflag)
            self.sortByRatingQuantity()
            self.displayItems(itemList)

        elif input == "Stock Info":
            self.deleteAll(itemList)
            self.csvReader(sortflag)
            self.sortByQuantityLeft()
            self.displayItems(itemList)

    def sortByID(self):
        """This method sorts products by ID
        """
        self.items.sort(key=lambda x: str(x[0]), reverse=True)

    def sortByName(self):
        """This method sorts products by name
        """
        self.items.sort(key=lambda x: str(x[1]), reverse=True)

    def sortByPrice(self):
        """This method sorts products by price
        """
        try:
            self.items.sort(key=lambda x: float(
                x[2].replace("$", "") if " - " not in str(x[2]) else x[2].replace("$", "").split(" - ")[0]), reverse=True)
        except:
            pass

    def sortByRating(self):
        """This method sorts products by rating
        """
        try:
            self.items.sort(key=lambda x: float(x[3]), reverse=False)
        except:
            pass

    def sortByRatingQuantity(self):
        """This method sorts products by quantity
        """
        try:
            self.items.sort(key=lambda x: float(x[4] if self.is_number(x[5]) is True else x[4].replace('rating','')), reverse=False)
        except:
            pass


    def sortByQuantityLeft(self):
        """This method sorts products by remaining quantity
        """
        try:
            self.items.sort(key=lambda x: float(x[5] if self.is_number(x[5]) is True else 0) , reverse=True)
        except:
            pass

    def csvReader(self,sortflag):
        """This method opens the csv files, reads and stores the data 
        """
        self.items=[]
        if sortflag == 0:
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
                        encoding='utf-8') as items:  # Open output-amazon.csv file (must be same directory as this program)
                    for row in items:
                        if ("N/A" not in row) and ("IGNORE" not in row): #Rejects invalid data
                            if str(row.split(",")[0]) not in str(self.items): #Removes duplicates via ID
                                self.items.append(list(row.split(",")))
            except:
                pass
            
        elif sortflag == 1:
            try:
                with open('savedItems.csv', 'r', newline='',
                          encoding='utf-8') as savedItemsIO:
                    for row in savedItemsIO:
                        if '"\r\n' not in row:
                            self.items.append(row.split(","))
            except:
                pass


        if sortflag == 0:
            for i in range(len(self.items)):
                self.items[i][3] = self.items[i][3].replace("out of 5 stars","")
                self.items[i][4] = self.items[i][4].replace("ratings","")
                if self.items[i][5] == "\r\n":  # Removes NULL values
                    self.items[i][5] = "0"

    def displayItems(self, itemList):
        """This method displays the items after sorting

        Args:
            itemList (treeview): the details of the products
        """
        for i, column in enumerate(self.items, start=0):
            itemList.insert("", 0, values=(self.items[i]))

    def deleteAll(self, itemList):
        """This method clears of the treeview data

        Args:
            itemList (treeview): the details of the products
        """
        itemList.delete(*itemList.get_children())

    def saveData(self, savedItem):
        """This method saves the product details into a csv file

        Args:
            savedItem (treeview): the details of the saved products

        Returns:
            int: nothing if savedItems is empty
        """
        duplicate_detection = [None]
        duplicate_flag = False

        if savedItem == "":
            return 0

        try:
            with open('savedItems.csv', 'r', newline='',
                  encoding='utf-8') as savedItemsIO:
                for row in savedItemsIO:
                    if '"\r\n' not in row:
                        duplicate_detection.append(row)
        except:
            pass

        for x in range(len(duplicate_detection)):
            try:
                if savedItem[0] == duplicate_detection[x].split(",")[0]:
                    duplicate_flag = True
            except:
                pass

        if duplicate_flag == False:
            with open('savedItems.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(savedItem)

        else:
            ctypes.windll.user32.MessageBoxW(0, "You've already saved this item", "", 1)

    def showFavourites(self, itemList):
        """This method displays the saved products

        Args:
            itemList (treeview): the details of the saved products
        """
        savedItem = []

        # Create savedItems.csv if not created.

        try:
            with open('savedItems.csv', 'r', newline='',
                  encoding='utf-8') as savedItemsIO:
                for row in savedItemsIO:
                    if '"\r\n' not in row:
                        savedItem.append(row.split(","))
        except:
            pass
        for i, column in enumerate(savedItem, start=0):
            itemList.insert("", 0, values=(savedItem[i]))

    def deleteAllFavourites(self, itemList):
        """This method deletes all saved products 

        Args:
            itemList (treeview): the details of the saved products
        """
        with open('savedItems.csv', 'w', newline='', encoding='utf-8') as f:
            pass
        itemList.delete(*itemList.get_children())

    def deleteFiles(self):
        """This method overwrites the csv files
        """
        with open('output-amazon.csv', 'w', newline='', encoding='utf-8') as f:
            pass
        with open('shopee-scrape.csv', 'w', newline='', encoding='utf-8') as f:
            pass

    def readReview(self, itemID, itemList):
        """This method opens the csv file, reads and stores the reviews 

        Args:
            itemID (str): product ID
            itemList (treeview): the details of the products
        """

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
        """This method checks if product ID is float

        Args:
            itemID (str): product ID

        Returns:
            bool: true or false
        """
        #Check if itemID is float or not. If it is a float, it is a shopee ID. Else, amazon ID.
        try:
            float(itemID)
        except ValueError:
            return False
        return True

    def readSentiment(self, itemID, itemList):
        """This method opens csv file and read the data of sentiment analysis

        Args:
            itemID (str): product ID
            itemList (treeview): the details of the products
        """
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

    def deleteSavedProduct(self, itemID, itemList):
        """This method opens csv file, reads it, stores parameters into a list, if parameter itemID is equal to row of list, delete row from list and rewrite csv file. Remaining products will then be displayed.

        Args:
            itemID (str): product ID
            itemList (treeview): the details of the products
        """
        savedItems = []
        with open('savedItems.csv', 'r+', newline='',
                  encoding='utf-8') as savedItemsIO:
            for row in savedItemsIO:
                if '"\r\n' not in row:
                    row = row.split(",")
                    row[5] = row[5].replace('"','')
                    savedItems.append(row)
                    if row[0] == itemID[0]:
                        savedItems.remove(row)

        self.deleteAll(itemList)

        with open('savedItems.csv', 'w', newline='\n', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(savedItems)

        for i, column in enumerate(savedItems, start=0):
            itemList.insert("", 0, values=(savedItems[i]))

    def openURL(self, selectedItem):
        """This method opens the website directed to the specific item

        Args:
            selectedItem (treeview child): the detail of the selected product
        """

        if "." in selectedItem[0]:
            url = 'https://shopee.sg/load-i.' + selectedItem[0]
        else:
            url = 'https://amazon.com/dp/' + selectedItem[0]

        webbrowser.open(url)




