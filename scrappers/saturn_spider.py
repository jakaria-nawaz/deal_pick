from bs4 import BeautifulSoup
import requests
import os
import sys
from urllib import parse
import time
from scrappers.utils import *

this_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(os.path.dirname(this_dir), 'web'))
sys.path.append(os.path.join(os.path.dirname(this_dir), 'web', 'pricing'))

import django


os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
django.setup()

from pricing.models import Product, Price, Currency, Shop

search_domains = {
    'saturn': 'www.saturn.de/de/search.html'
}


def get_price_title(query):
    price_title = []
    search_page = 'http://www.saturn.de/de/search.html'
    response = requests.get(
        search_page,
        params={
            'query': query,
            'searchProfile': 'onlineshop',
            'channel': 'sedede'
        }
    )

    soup = BeautifulSoup(response.content, 'html.parser')

    product_wrappers = soup.findAll('div', {'class': 'product-wrapper'})
    for wrapper in product_wrappers:
        try:
            content = wrapper.findAll('div', {'class': 'content'})[0]
            title = content.findAll('h2')[0].text.strip()
            url = content.findAll('h2')[0].a.get('href')
            url = parse.urljoin(search_page, url)
            price_wrappers = wrapper.findAll('div', {'class': 'price small'})
            price = price_wrappers[0].text
            price_title.append((price, title, url))
        except:
            pass

    return price_title


def query_maker(query):
    param = ''
    for keyword in query.split():
        param += keyword
    return param


def create_price_records(price_title):
    shop = Shop.objects.get(title='Saturn')
    for pt in price_title:
        try:
            product = Product.objects.get(title=pt[1], shop=shop)
        except Product.DoesNotExist:
            product = Product.objects.create(
                title=pt[1],
                shop=shop,
                image=get_image_url(pt[2])
            )
        price_obj = Price.objects.create(
            price=pt[0].split(',')[0],
            currency=Currency.objects.get(title='Euro'),
            product=product,
            url=pt[2]
        )
        print("image", get_image_url(pt[2]))


def get_image_url(url):
    try:
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        return soup.findAll("a", {"class": "zoom"})[0].get('href')
    except:
        print('failed to get img  url for ', url)
        return ""


if __name__ == '__main__':
    # print('enter the query')
    # query = input()
    products = get_products()
    for product in products:
        query = query_maker(product)
        price_title = get_price_title(query)
        create_price_records(price_title)
        time.sleep(2)
