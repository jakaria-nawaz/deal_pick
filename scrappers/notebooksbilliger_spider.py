from selenium import webdriver

from bs4 import BeautifulSoup
import requests
import os
import sys
from urllib import parse
import time

this_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(os.path.dirname(this_dir), 'web'))
sys.path.append(os.path.join(os.path.dirname(this_dir), 'web', 'pricing'))

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
django.setup()

from pricing.models import Product, Price, Currency, Shop

search_domains = {
    'notebooksbilliger': 'https://www.notebooksbilliger.de'
}


def create_price_records(price_title):
    shop = Shop.objects.get(title='notebooksbilliger')
    currency = Currency.objects.get(title='Euro')
    for pt in price_title:
        try:
            product = Product.objects.get(title=pt[1], shop=shop)
        except Product.DoesNotExist:
            print("creating new product", pt[1])
            product = Product.objects.create(
                title=pt[1],
                shop=shop,
                image=get_image_url(pt[2])
            )
        price_obj = Price.objects.create(
            price=pt[0].split(',')[0],
            currency=currency,
            product=product,
            url=pt[2],
        )


def query_maker(query):
    return '+'.join(query.split())


def get_price_title(query):
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


def get_image_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        image_url = soup.find("img", {'id': 'detailimage'}).get("src")
        return image_url[2:] if image_url.startswith("//") else image_url
    except Exception as e:
        print("could not retrieve image from", url, " due to", e)
        return ""


if __name__ == '__main__':

    from scrappers.utils import get_products

    products = get_products()
    for product in products:
        print('-- request sent for product --', product)
        query = query_maker(product)
        price_title = get_price_title(query)
        create_price_records(price_title)
