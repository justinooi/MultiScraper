import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
from Shopee_Scraper import Shopee_Scraper
from Amazon_Scraper import Amazon_Scraper
from storageHandler import storageHandler
import time

class multiScraperGUI():
    """This class manages the overall GUI of this program. Widgets from the Tkinter library were used to construct the overall GUI.
    
    """
    mainBackground = 'LightSteelBlue1' # Sets mainBackground colour

    def initGUI(self):
        """This method initializes a GUI window with a size of 1300 by 700
        
        """
        
        mainGUI = tkinter.Tk(className='MultiScraper')  # Sets window name
        mainGUI.geometry("1300x700+100+50")  # Sets window size
        mainGUI.configure(bg=self.mainBackground) #Sets GUI background color
        mainGUI.resizable(width=False, height=False) #Disallows user from resizing the window.
        self.mainMenu(mainGUI) #Calls the mainMenu() method which initializes the mainmenu screen
        mainGUI.mainloop()  # Starts up and runs the GUI until user exits

    def mainMenu(self, mainGUI):
        """This method constructs the main menu with the use of the frame widget from the tkinter library. The purpose of the Frame widget is to group and organize widgets
        such as buttons, labels, treeview, etc. in a friendly way. It works like a container, which is responsible for arranging other widgets. As users enter another page,
        the widgets of the previous page have to be deinitialized with the place_forget() method from the tkinter library. Since we grouped the buttons, labels, treeview, etc. widgets
        into one frame, we only have to deinitialize the frame itself.
        Args:
            mainGUI (object): The GUI instance 

        """
        #Initializes a frame on the GUI dedicated to the main menu.
        mainMenuFrame = tkinter.Frame(mainGUI, bg=self.mainBackground)
        mainMenuFrame.place(relx=0.1, rely=0, relheight=0.9, relwidth=0.8)

        # Title Display
        title = tkinter.Label(mainMenuFrame, text="MultiScraper", bg=self.mainBackground)
        title.config(font=("MS Sans Serif", 70))
        title.place(relx=0.1, rely=0.05, relheight=0.2, relwidth=0.8)

        # Description Display
        title = tkinter.Label(mainMenuFrame, text="Crawls/Scrapes Amazon and Shopee", bg=self.mainBackground)
        title.config(font=("MS Sans Serif", 20))
        title.place(relx=0, rely=0.23, relheight=0.05, relwidth=1)

        # Displays the 'Crawl' button. Upon clicking the button, user will head to the crawl page and the the main menu frame widget gets deinitialized.
        crawlButton = Button(mainMenuFrame, text="Crawl",
                             command=lambda: [self.crawlerPage(mainGUI), mainMenuFrame.place_forget()])
        crawlButton.config(font=("Arial", 30))
        crawlButton.place(relx=0.25, rely=0.45, relheight=0.1, relwidth=0.5)

        # Displays the 'Review Data' button. Upon clicking the button, user will head to the review products page and the the main menu frame widget gets deinitialized.
        reviewButton = Button(mainMenuFrame, text="Review Data", command=lambda: [mainMenuFrame.place_forget(), self.productDetailsPage(mainGUI)])
        reviewButton.config(font=("Arial", 30))
        reviewButton.place(relx=0.25, rely=0.60, relheight=0.1, relwidth=0.5)

        # Displays the 'Review Data' button. Upon clicking the button, user will head to the review products page and the the main menu frame widget gets deinitialized.
        favouritesButton = Button(mainMenuFrame, text="Favourites", command=lambda: [mainMenuFrame.place_forget(), self.favouritesPage(mainGUI)])
        favouritesButton.config(font=("Arial", 30))
        favouritesButton.place(relx=0.25, rely=0.75, relheight=0.1, relwidth=0.5)

        # Displays 'Exit' button. Upon clicking the button, the program exits
        exitButton = Button(mainMenuFrame, text="Exit", command=lambda: exit(0))
        exitButton.config(font=("Arial", 30))
        exitButton.place(relx=0.25, rely=0.90, relheight=0.1, relwidth=0.5)

    def crawlerPage(self, mainGUI):
        """This method constructs a crawl page. Users can enter a search parameter, choose either Shopee, Amazon or both and set the product quantity to scrape from.

        Args:
            mainGUI (object): The GUI instance

        """
        # Instantiate crawlerFrame
        crawlerFrame = tkinter.Frame(mainGUI, bg=self.mainBackground)
        crawlerFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        # Question to the user
        title = tkinter.Label(crawlerFrame, text="Enter product to scrape", bg=self.mainBackground)
        title.config(font=("Arial", 30))
        title.place(relx=0, rely=0.05, relheight=0.2, relwidth=1)

        # User Input Box
        search_parameter = tk.StringVar()
        nameEntered = tkinter.Entry(crawlerFrame, textvariable=search_parameter)
        nameEntered.config(font=("Arial", 15))
        nameEntered.place(relx=0.3, rely=0.21, relheight=0.05, relwidth=0.4)

        # Checker boxes
        checked_amazon = IntVar()
        checked_shopee = IntVar()
        checkerAmazon = tkinter.Checkbutton(crawlerFrame, text="Amazon", variable=checked_amazon,
                                            bg=self.mainBackground)
        checkerShopee = tkinter.Checkbutton(crawlerFrame, text="Shopee", variable=checked_shopee,
                                            bg=self.mainBackground)
        checkerAmazon.config(font=("Arial", 15))
        checkerShopee.config(font=("Arial", 15))
        checkerAmazon.place(relx=0.35, rely=0.28, relheight=0.04, relwidth=0.14)
        checkerShopee.place(relx=0.5, rely=0.28, relheight=0.04, relwidth=0.14)

        # Invalid Msg
        invalidMsg = tkinter.Label(crawlerFrame, text="Invalid parameters",
                                   bg=self.mainBackground)
        invalidMsg.config(font=("MS Sans Serif", 15), fg='red')

        # Warning MSG
        warningMsg = tkinter.Label(crawlerFrame,
                                   text="Note: Upon clicking submit, it will take quite some time to gather details (Monitor the CLI)",
                                   bg=self.mainBackground)
        warningMsg.config(font=("MS Sans Serif", 15), fg='red')
        warningMsg.place(relx=0, rely=0.6, relheight=0.1, relwidth=1)

        # submit button
        submitButton = Button(crawlerFrame, text="Submit", command=lambda: [
            [crawlerFrame.place_forget(), self.callScrape(mainGUI, search_parameter, checked_amazon.get(), checked_shopee.get(), itemQuantityScroller.get())] if (checked_shopee.get() == 1 or checked_amazon.get() == 1) and search_parameter.get() != "" else [
                invalidMsg.place(relx=0.7, rely=0.2, relheight=0.1, relwidth=0.3)]])

        submitButton.config(font=("Arial", 25))
        submitButton.place(relx=0.35, rely=0.69, relheight=0.1, relwidth=0.3)

        #Item quantity scroller
        itemQuantityScroller = Scale(crawlerFrame, from_=10, to=50, orient=HORIZONTAL, resolution = 10)
        itemQuantityScroller.place(relx=0.35, rely=0.45, relheight=0.07, relwidth=0.3)

        #Item quantity scroller description
        itemQuantityScrollerDesc = tkinter.Label(crawlerFrame,
                                                 text="Number of products to scrape from each website",
                                                 bg=self.mainBackground)
        itemQuantityScrollerDesc.config(font=("MS Sans Serif", 15))
        itemQuantityScrollerDesc.place(relx=0.3, rely=0.40, relheight=0.05, relwidth=0.35)

        # back button
        backButton = Button(crawlerFrame, text="Back",
                            command=lambda: [self.mainMenu(mainGUI), crawlerFrame.place_forget()])
        backButton.config(font=("Arial", 30))
        backButton.place(relx=0.25, rely=0.80, relheight=0.1, relwidth=0.5)

    def callScrape(self, mainGUI, search_parameter, checked_amazon, checked_shopee, itemQuantity):
        """This method constructs a page that informs the user that the program has finished scraping

        Args:
            mainGUI (object): The GUI instance
            search_parameter (str): Search parameter of user
            checked_amazon (int): Flag to crawl Amazon
            checked_shopee (int): Flag to crawl Shopee
            itemQuantity (int): Determines item quantity in multiples of 10
        """
        time.sleep(1)
        storageHandler().deleteFiles()
        time.sleep(1)
        callScrapeFrame = tkinter.Frame(mainGUI, bg=self.mainBackground)
        callScrapeFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        warningMsg = tkinter.Label(callScrapeFrame,
                                   text="Scraping done. . .",
                                   bg=self.mainBackground)
        warningMsg.config(font=("MS Sans Serif", 40))
        warningMsg.place(relx=0, rely=0.3, relheight=0.2, relwidth=1)

        reviewButton = Button(callScrapeFrame, text="Review Data",
                              command=lambda: [callScrapeFrame.place_forget(), self.productDetailsPage(mainGUI)])
        reviewButton.config(font=("Arial", 30))
        reviewButton.place(relx=0.25, rely=0.80, relheight=0.1, relwidth=0.5)

        if checked_shopee == 1:
            url = Shopee_Scraper().linkScrape(search_parameter.get(),itemQuantity)
            Shopee_Scraper().productScrape(url)

        if checked_amazon == 1:
            url = Amazon_Scraper().linkScrape(search_parameter.get(),itemQuantity)
            Amazon_Scraper().productScrape(url)

        print("Done")






    def productDetailsPage(self, mainGUI):
        """This method constructs a page that displays product details
        
        Args:
            mainGUI (object): The GUI instance
        """
        productDetailsFrame = tkinter.Frame(mainGUI, bg=self.mainBackground)
        productDetailsFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = tkinter.Label(productDetailsFrame,
                              text="Product Details",
                              bg=self.mainBackground)
        title.config(font=("MS Sans Serif", 40))
        title.place(relx=0, rely=0, relheight=0.1, relwidth=1)

        #Tree Table
        item_column = ('Item ID','Name', 'Price', 'Rating (out of 5)', 'Number of Ratings', 'Stock Info')
        itemList = ttk.Treeview(productDetailsFrame,columns=item_column,show='headings')
        for i in range(len(item_column)):
            itemList.heading(item_column[i], text=item_column[i])

        itemList.column(item_column[0], anchor="w", width=70)
        itemList.column(item_column[1], anchor="w", width=600)
        itemList.column(item_column[2], anchor="n", width=30)
        itemList.column(item_column[3], anchor="n", width=30)
        itemList.column(item_column[4], anchor="n", width=30)
        itemList.column(item_column[5], anchor="n", width=30)
        itemList.place(relx=0,rely=0.1, relheight=0.5, relwidth=1)


        storageHandler().initialization(itemList)

        #Sorting Options
        sortVariable = StringVar()
        sortVariable.set("None")
        sortOptions = OptionMenu(productDetailsFrame, sortVariable,"None", "ID", "Name", "Price", "Rating", "Rating Count", "Stock Info")
        sortOptions.place(relx=0.2,rely=0.65, relheight=0.05, relwidth=0.12)
        sortOptions.config(font=("MS Sans Serif", 15))

        #Sort Text
        title = tkinter.Label(productDetailsFrame, text="Sort By: ", bg=self.mainBackground)
        title.config(font=("Arial", 20))
        title.place(relx=0.1, rely=0.65, relheight=0.05, relwidth=0.1)

        #Save instructions
        saveInfo = tkinter.Label(productDetailsFrame, text="Select, save a product or check review", bg=self.mainBackground)
        saveInfo.config(font=("Arial", 20))
        saveInfo.place(relx=0.6, rely=0.63, relheight=0.05, relwidth=0.4)

        #Sort Button
        sortButton = Button(productDetailsFrame, text="Sort", command=lambda: [storageHandler().sortParams(sortVariable.get(), itemList,0)])
        sortButton.config(font=("Arial", 10))
        sortButton.place(relx=0.35, rely=0.65, relheight=0.05, relwidth=0.1)

        #View Button
        sortButton = Button(productDetailsFrame, text="Open In Browser",command=lambda: [storageHandler().openURL(itemList.item(itemList.selection())['values'])])
        sortButton.config(font=("Arial", 10))
        sortButton.place(relx=0.475, rely=0.65, relheight=0.05, relwidth=0.1)

        #Main Menu button
        mainMenuButton = Button(productDetailsFrame, text="Main Menu", command=lambda: [productDetailsFrame.place_forget(), self.mainMenu(mainGUI)])
        mainMenuButton.config(font=("Arial", 30))
        mainMenuButton.place(relx=0.05, rely=0.85, relheight=0.1, relwidth=0.2)

        #Favourites Button
        savesButton = Button(productDetailsFrame, text="Saved Products", command=lambda: [productDetailsFrame.place_forget(), self.favouritesPage(mainGUI)])
        savesButton.config(font=("Arial", 30))
        savesButton.place(relx=0.37, rely=0.85, relheight=0.1, relwidth=0.25)

        #ReCrawl Button
        reCrawlButton = Button(productDetailsFrame, text="ReCrawl", command=lambda: [productDetailsFrame.place_forget(), self.crawlerPage(mainGUI)])
        reCrawlButton.config(font=("Arial", 30))
        reCrawlButton.place(relx=0.75, rely=0.85, relheight=0.1, relwidth=0.2)

        #saveButton
        saveButton = Button(productDetailsFrame, text="Save Product Details", command=lambda: [storageHandler().saveData(itemList.item(itemList.selection())['values'])])
        saveButton.config(font=("Arial", 15))
        saveButton.place(relx=0.7, rely=0.69, relheight=0.05, relwidth=0.2)

        #check Review Button
        checkReviewButton = Button(productDetailsFrame, text="Check Reviews", command=lambda: [(productDetailsFrame.place_forget(),self.reviewsPage(mainGUI, itemList.item(itemList.selection())['values'])) if itemList.item(itemList.selection())['values'] != "" else 0])
        checkReviewButton.config(font=("Arial", 15))
        checkReviewButton.place(relx=0.7, rely=0.75, relheight=0.05, relwidth=0.2)


    def favouritesPage(self, mainGUI):
        """This method constructs a page that displays products saved by users
        
        Args:
            mainGUI (object): The GUI instance
        """
        favouritesFrame = tkinter.Frame(mainGUI, bg=self.mainBackground)
        favouritesFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = tkinter.Label(favouritesFrame,
                              text="🌟 Saved Products 🌟",
                              bg=self.mainBackground)
        title.config(font=("MS Sans Serif", 40))
        title.place(relx=0, rely=0, relheight=0.1, relwidth=1)

        item_column = ('Item ID','Name', 'Price', 'Rating', 'Number of Ratings', 'Stock Info')
        itemList = ttk.Treeview(favouritesFrame,columns=item_column,show='headings')
        for i in range(len(item_column)):
            itemList.heading(item_column[i], text=item_column[i])

        itemList.column(item_column[0], anchor="w", width=70)
        itemList.column(item_column[1], anchor="w", width=600)
        itemList.column(item_column[2], anchor="n", width=30)
        itemList.column(item_column[3], anchor="n", width=30)
        itemList.column(item_column[4], anchor="n", width=30)
        itemList.column(item_column[5], anchor="n", width=30)
        itemList.place(relx=0,rely=0.1, relheight=0.5, relwidth=1)

        storageHandler().showFavourites(itemList)

        #Main Menu
        mainMenuButton = Button(favouritesFrame, text="Main Menu", command=lambda: [favouritesFrame.place_forget(), self.mainMenu(mainGUI)])
        mainMenuButton.config(font=("Arial", 30))
        mainMenuButton.place(relx=0.05, rely=0.85, relheight=0.1, relwidth=0.2)

        #Review Button
        reviewButton = Button(favouritesFrame, text="Review Data", command=lambda: [favouritesFrame.place_forget(), self.productDetailsPage(mainGUI)])
        reviewButton.config(font=("Arial", 30))
        reviewButton.place(relx=0.37, rely=0.85, relheight=0.1, relwidth=0.25)

        #ReCrawl Button
        reCrawlButton = Button(favouritesFrame, text="reCrawl", command=lambda: [favouritesFrame.place_forget(), self.crawlerPage(mainGUI)])
        reCrawlButton.config(font=("Arial", 30))
        reCrawlButton.place(relx=0.75, rely=0.85, relheight=0.1, relwidth=0.2)

        #delete all Button
        deleteAllButton = Button(favouritesFrame, text="DELETE ALL", command=lambda: [storageHandler().deleteAllFavourites(itemList)])
        deleteAllButton.config(font=("Arial", 15))
        deleteAllButton.place(relx=0.05, rely=0.75, relheight=0.05, relwidth=0.20)

        # Delete particular product
        deleteProductButton = Button(favouritesFrame, text="Delete Product", command=lambda: [(storageHandler().deleteSavedProduct(itemList.item(itemList.selection())['values'],itemList)) if itemList.item(itemList.selection())['values'] != "" else 0])
        deleteProductButton.config(font=("Arial", 20))
        deleteProductButton.place(relx=0.37, rely=0.7, relheight=0.08, relwidth=0.20)

        #Check reviews
        checkReviewButton = Button(favouritesFrame, text="Check reviews", command=lambda: [(favouritesFrame.place_forget(),self.reviewsPage(mainGUI, itemList.item(itemList.selection())['values'])) if itemList.item(itemList.selection())['values'] != "" else 0])
        checkReviewButton.config(font=("Arial", 15))
        checkReviewButton.place(relx=0.7, rely=0.72, relheight=0.05, relwidth=0.25)

        #Sorting Options
        sortVariable = StringVar()
        sortVariable.set("None")
        sortOptions = OptionMenu(favouritesFrame, sortVariable,"None", "ID", "Name", "Price", "Rating", "Rating Count", "Stock Info")
        sortOptions.place(relx=0.05,rely=0.63, relheight=0.05, relwidth=0.12)
        sortOptions.config(font=("MS Sans Serif", 15))

        #Sort Text
        title = tkinter.Label(favouritesFrame, text="Sort By: ", bg=self.mainBackground)
        title.config(font=("MS Sans Serif", 20))
        title.place(relx=0.15, rely=0.63, relheight=0.05, relwidth=0.1)

        #Sort Button
        sortButton = Button(favouritesFrame, text="SORT", command=lambda: [storageHandler().sortParams(sortVariable.get(), itemList,1)])
        sortButton.config(font=("Arial", 20))
        sortButton.place(relx=0.25, rely=0.63, relheight=0.05, relwidth=0.1)

    def reviewsPage(self, mainGUI, itemID):
        """This method constructs a page that displays reviews of a product selected by a user
        
        Args:
            mainGUI (object): The GUI instance
            itemID (str): Product ID
        """

        reviewsFrame = tkinter.Frame(mainGUI, bg=self.mainBackground)
        reviewsFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = tkinter.Label(reviewsFrame,
                              text="Reviews",
                              bg=self.mainBackground)
        title.config(font=("MS Sans Serif", 40))
        title.place(relx=0, rely=0, relheight=0.1, relwidth=1)

        item_column = ('Rating','Review')
        itemList = ttk.Treeview(reviewsFrame,columns=item_column,show='headings')
        for i in range(len(item_column)):
            itemList.heading(item_column[i], text=item_column[i])

        itemList.column(item_column[0], anchor="n", width=30)
        itemList.column(item_column[1], anchor="w", width=1200)

        itemList.place(relx=0,rely=0.1, relheight=0.5, relwidth=1)

        storageHandler().readReview(itemID[0], itemList)


        #Back Button
        backButton = Button(reviewsFrame, text="Back", command=lambda: [reviewsFrame.place_forget(), self.productDetailsPage(mainGUI)])
        backButton.config(font=("Arial", 30))
        backButton.place(relx=0.2, rely=0.85, relheight=0.1, relwidth=0.25)

        #Sentiment Analysis Button
        reviewButton = Button(reviewsFrame, text="Sentiment Analysis", command=lambda: [reviewsFrame.place_forget(), self.sentimentPage(mainGUI, itemID)])
        reviewButton.config(font=("Arial", 30))
        reviewButton.place(relx=0.6, rely=0.85, relheight=0.1, relwidth=0.3)

    def sentimentPage(self, mainGUI, itemID):
        """This method constructs a page that displays sentiments of reviews
        
        Args:
            mainGUI (object): The GUI instance
            itemID (str): Product ID

        """

        sentimentFrame = tkinter.Frame(mainGUI, bg=self.mainBackground)
        sentimentFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        title = tkinter.Label(sentimentFrame,
                              text="Sentiment Analysis",
                              bg=self.mainBackground)
        title.config(font=("MS Sans Serif", 40))
        title.place(relx=0, rely=0, relheight=0.1, relwidth=1)

        item_column = ('No.','Rating', 'Review', 'Sentiment', 'Confidence')
        itemList = ttk.Treeview(sentimentFrame, columns=item_column, show='headings')
        for i in range(len(item_column)):
            itemList.heading(item_column[i], text=item_column[i])

        itemList.column(item_column[0], anchor="n", width=5)
        itemList.column(item_column[1], anchor="n", width=30)
        itemList.column(item_column[2], anchor="w", width=1000)
        itemList.column(item_column[3], anchor="n", width=50)
        itemList.column(item_column[4], anchor="w", width=50)

        itemList.place(relx=0, rely=0.1, relheight=0.5, relwidth=1)

        #Back Button
        backButton = Button(sentimentFrame, text="Back", command=lambda: [sentimentFrame.place_forget(), self.reviewsPage(mainGUI, itemID)])
        backButton.config(font=("Arial", 30))
        backButton.place(relx=0.35, rely=0.85, relheight=0.1, relwidth=0.25)

        storageHandler().readSentiment(itemID[0], itemList)

if __name__ == '__main__':
    main_GUI = multiScraperGUI() #Instantiates a multiScraperGUI object.
    main_GUI.initGUI() #Calls the initGUI() method from the multiScraperGUI() class which starts up the GUI
