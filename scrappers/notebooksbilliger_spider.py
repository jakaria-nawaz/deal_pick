from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from scrappers.base_spider import BaseRequestSpider


class NotebooksBilligerSpider(BaseRequestSpider):
    shop_title = "notebooksbilliger"
    currency_title = "Euro"
    search_page = 'https://www.notebooksbilliger.de'

    def __init__(self):
        super(NotebooksBilligerSpider, self).__init__()

    def get_price_title(self, query):
        try:
            options = webdriver.ChromeOptions()

            options.add_argument('headless')

            # set the window size
            options.add_argument('window-size=1200x600')

            # initialize the driver
            driver = webdriver.Chrome(chrome_options=options)
            res = driver.get("https://www.notebooksbilliger.de/produkte/" + query)
            wrappers = driver.find_elements_by_class_name('listing_main')[0].find_elements_by_css_selector(
                ".mouseover.clearfix")
            price_title = []
            for wrapper in wrappers:
                title = wrapper.find_elements_by_class_name('listing_product_title')[0].text
                url = wrapper.find_elements_by_class_name('listing_product_title')[0].get_attribute('href')
                price = wrapper.find_element_by_class_name('nbb-svg-shadow').text

                print("prepared price title record", price, title, url)
                price_title.append((price, title, url))
            return price_title
        except Exception as e:
            print("Exception at line", e)
            return []

    def get_image_url(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            image_url = soup.find("img", {'id': 'detailimage'}).get("src")
            return image_url[2:] if image_url.startswith("//") else image_url
        except Exception as e:
            print("could not retrieve image from", url, " due to", e)
            return ""


if __name__ == '__main__':
    obj = NotebooksBilligerSpider()
    obj.start()
