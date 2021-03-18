import tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import *
from Shopee_Scraper import Shopee_Scraper
from Amazon_Scraper import Amazon_Scraper
from csvSorter import csvSorter


class multiScraperGUI:
    mainBackground = 'LightSteelBlue1'
    testBackground = 'SlateGray2'

    def initialization(self):
        mainGUI = tkinter.Tk(className='MultiScraper')  # Sets window name
        mainGUI.geometry("1300x700+100+50")  # Sets window size
        mainGUI.configure(bg=self.mainBackground)
        mainGUI.resizable(width=False, height=False)
        self.mainMenu(mainGUI)
        mainGUI.mainloop()  # Run the GUI

    def mainMenu(self, mainGUI):
        mainMenuFrame = tkinter.Frame(mainGUI, bg=self.mainBackground)
        mainMenuFrame.place(relx=0.1, rely=0, relheight=0.9, relwidth=0.8)

        # Title
        title = tkinter.Label(mainMenuFrame, text="MultiScraper", bg=self.mainBackground)
        title.config(font=("MS Sans Serif", 70))
        title.place(relx=0.1, rely=0.05, relheight=0.2, relwidth=0.8)

        # Description
        title = tkinter.Label(mainMenuFrame, text="Crawls/Scrapes Amazon and Shopee", bg=self.mainBackground)
        title.config(font=("MS Sans Serif", 20))
        title.place(relx=0, rely=0.23, relheight=0.05, relwidth=1)

        # Crawl Button
        crawlButton = Button(mainMenuFrame, text="Crawl",
                             command=lambda: [self.crawlerPage(mainGUI), mainMenuFrame.place_forget()])
        crawlButton.config(font=("Arial", 30))
        crawlButton.place(relx=0.25, rely=0.45, relheight=0.1, relwidth=0.5)

        # Review Data Button
        reviewButton = Button(mainMenuFrame, text="Review Data", command=lambda: [mainMenuFrame.place_forget(),self.productDetailsPage(mainGUI)])
        reviewButton.config(font=("Arial", 30))
        reviewButton.place(relx=0.25, rely=0.60, relheight=0.1, relwidth=0.5)

        #Favourites Button
        favouritesButton = Button(mainMenuFrame, text="Favourites", command=lambda: [mainMenuFrame.place_forget(),self.favouritesPage(mainGUI)])
        favouritesButton.config(font=("Arial", 30))
        favouritesButton.place(relx=0.25, rely=0.75, relheight=0.1, relwidth=0.5)

        # Exit Button
        exitButton = Button(mainMenuFrame, text="Exit", command=lambda: exit(1))
        exitButton.config(font=("Arial", 30))
        exitButton.place(relx=0.25, rely=0.90, relheight=0.1, relwidth=0.5)

    def crawlerPage(self, mainGUI):
        # Instantiate crawlerFrame
        crawlerFrame = tkinter.Frame(mainGUI, bg=self.mainBackground)
        crawlerFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        # Question
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
            [crawlerFrame.place_forget(),self.callScrape(mainGUI, search_parameter, checked_amazon.get(), checked_shopee.get())] if (checked_shopee.get() == 1 or checked_amazon.get() == 1) and search_parameter.get() != "" else [
                invalidMsg.place(relx=0, rely=0.5, relheight=0.1, relwidth=1)]])

        submitButton.config(font=("Arial", 25))
        submitButton.place(relx=0.35, rely=0.35, relheight=0.1, relwidth=0.3)

        # back button
        backButton = Button(crawlerFrame, text="Back",
                            command=lambda: [self.mainMenu(mainGUI), crawlerFrame.place_forget()])
        backButton.config(font=("Arial", 30))
        backButton.place(relx=0.25, rely=0.80, relheight=0.1, relwidth=0.5)

    def callScrape(self, mainGUI, search_parameter, checked_amazon, checked_shopee):
        callScrapeFrame = tkinter.Frame(mainGUI, bg=self.mainBackground)
        callScrapeFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        warningMsg = tkinter.Label(callScrapeFrame,
                                   text="Scraping done. . .",
                                   bg=self.mainBackground)
        warningMsg.config(font=("MS Sans Serif", 40))
        warningMsg.place(relx=0, rely=0.3, relheight=0.2, relwidth=1)

        if checked_shopee == 1:
            url = Shopee_Scraper().linkScrape(search_parameter.get())
            Shopee_Scraper().productScrape(url)

        if checked_amazon == 1:
            url = Amazon_Scraper().linkScrape(search_parameter.get())
            Amazon_Scraper().productScrape(url)

            # process = threading.Thread(target=lambda: SS.linkScrape(search_parameter.get()))
            # process.start()
            # time.sleep(1)
        print("Done")

            # process = threading.Thread(target=lambda q, arg1: q.put(SS.linkScrape(arg1), args=(que, search_parameter.get())))

        reviewButton = Button(callScrapeFrame, text="Review Data",
                            command=lambda: [callScrapeFrame.place_forget(), self.productDetailsPage(mainGUI)])
        reviewButton.config(font=("Arial", 30))
        reviewButton.place(relx=0.25, rely=0.80, relheight=0.1, relwidth=0.5)


    def productDetailsPage(self, mainGUI):
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


        csvSorter().initialization(itemList)

        #Sorting Options
        sortVariable = StringVar()
        sortVariable.set("None")
        sortOptions = OptionMenu(productDetailsFrame, sortVariable,"None", "ID", "Name", "Price", "Rating", "Rating Count", "Stock Info")
        sortOptions.place(relx=0.2,rely=0.65, relheight=0.05, relwidth=0.12)
        sortOptions.config(font=("MS Sans Serif", 15))

        #Sort Text
        title = tkinter.Label(productDetailsFrame, text="Sort By: ", bg=self.mainBackground)
        title.config(font=("MS Sans Serif", 20))
        title.place(relx=0.1, rely=0.65, relheight=0.05, relwidth=0.1)

        #Save instructions
        saveInfo = tkinter.Label(productDetailsFrame, text="Select, save a product or check review", bg=self.mainBackground)
        saveInfo.config(font=("MS Sans Serif", 15))
        saveInfo.place(relx=0.6, rely=0.6, relheight=0.05, relwidth=0.4)

        #Sort Button
        sortButton = Button(productDetailsFrame, text="SORT", command=lambda: [csvSorter().sortParams(sortVariable.get(),itemList)])
        sortButton.config(font=("Arial", 20))
        sortButton.place(relx=0.4, rely=0.65, relheight=0.05, relwidth=0.1)

        #Main Menu button
        mainMenuButton = Button(productDetailsFrame, text="Main Menu", command=lambda: [productDetailsFrame.place_forget(),self.mainMenu(mainGUI)])
        mainMenuButton.config(font=("Arial", 30))
        mainMenuButton.place(relx=0.05, rely=0.85, relheight=0.1, relwidth=0.2)

        #Favourites Button
        savesButton = Button(productDetailsFrame, text="Saved Products", command=lambda: [productDetailsFrame.place_forget(),self.favouritesPage(mainGUI)])
        savesButton.config(font=("Arial", 30))
        savesButton.place(relx=0.37, rely=0.85, relheight=0.1, relwidth=0.25)

        #ReCrawl Button
        reCrawlButton = Button(productDetailsFrame, text="reCrawl", command=lambda: [productDetailsFrame.place_forget(),self.crawlerPage(mainGUI)])
        reCrawlButton.config(font=("Arial", 30))
        reCrawlButton.place(relx=0.75, rely=0.85, relheight=0.1, relwidth=0.2)

        #saveButton
        saveButton = Button(productDetailsFrame, text="Save Product Details", command=lambda: [csvSorter().saveData(itemList.item(itemList.selection())['values'])])
        saveButton.config(font=("Arial", 15))
        saveButton.place(relx=0.7, rely=0.66, relheight=0.05, relwidth=0.2)

        #check Review Button
        saveButton = Button(productDetailsFrame, text="Check reviews (work in progress)", command=lambda: [])
        saveButton.config(font=("Arial", 15))
        saveButton.place(relx=0.7, rely=0.72, relheight=0.05, relwidth=0.25)


    def favouritesPage(self, mainGUI):
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

        csvSorter().showFavourites(itemList)

        #Main Menu
        mainMenuButton = Button(favouritesFrame, text="Main Menu", command=lambda: [favouritesFrame.place_forget(),self.mainMenu(mainGUI)])
        mainMenuButton.config(font=("Arial", 30))
        mainMenuButton.place(relx=0.05, rely=0.85, relheight=0.1, relwidth=0.2)

        #Review Button
        reviewButton = Button(favouritesFrame, text="Review Data", command=lambda: [favouritesFrame.place_forget(),self.productDetailsPage(mainGUI)])
        reviewButton.config(font=("Arial", 30))
        reviewButton.place(relx=0.37, rely=0.85, relheight=0.1, relwidth=0.25)

        #ReCrawl Button
        reCrawlButton = Button(favouritesFrame, text="reCrawl", command=lambda: [favouritesFrame.place_forget(),self.crawlerPage(mainGUI)])
        reCrawlButton.config(font=("Arial", 30))
        reCrawlButton.place(relx=0.75, rely=0.85, relheight=0.1, relwidth=0.2)

        #delete all Button
        deleteAllButton = Button(favouritesFrame, text="Delete ALL", command=lambda: [csvSorter().deleteAllFavourites(itemList)])
        deleteAllButton.config(font=("Arial", 30))
        deleteAllButton.place(relx=0.37, rely=0.7, relheight=0.1, relwidth=0.25)


main_GUI = multiScraperGUI()
main_GUI.initialization()
