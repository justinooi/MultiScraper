# MultiScraper

MultiScraper scrapes Amazon and Shopee product data for sellers and buyers. It helps sellers find best-selling or trending products to sell, while it help buyers cross-check product prices, reviews, and etc. on different platforms.

## Requirements

Install all requirements through our requirements.txt file

```bash
pip install -r requirements.txt
```

## Usage

Simply run MultiScraperGUI.py or you can initialize your own multiScraper class as shown below:

```python
import multiScraperGUI

 main_GUI = multiScraperGUI() # Instantiates a multiScraperGUI object.
 main_GUI.initGUI() # Calls the initGUI() method from the multiScraperGUI() class which starts up the GUI.
```

Tested on Windows 10 only.

## Team
Done by Team 23 of CSC1009 of SIT-UofG Computing Science (AY 20/21)

## License
[MIT](https://choosealicense.com/licenses/mit/)
