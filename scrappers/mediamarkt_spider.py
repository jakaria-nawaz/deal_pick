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
    'mediamarkt': 'https://www.mediamarkt.de/de/search.html'
}


def get_price_title(query):
    price_title = []
    search_page = 'https://www.mediamarkt.de/de/search.html'
    response = requests.get(
        search_page,
        params={
            'query': query,
        }
    )
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_wrappers = soup.findAll('a', {'class': 'mms-link mms-srp-product'})
    for wrapper in product_wrappers:
        try:
            #content = wrapper.findAll('div', {'class': 'mms-product-row__grid'})[0]
            title = wrapper.findAll('h2', {'class': 'mms-headline mms-headline--styling-level3'})[0].text
            url = wrapper.get('href')
            url = parse.urljoin(search_page, url)
            price_wrappers = wrapper.findAll('span', {'class': 'mms-price__price'})
            price = price_wrappers[0].text.split('.')[0]
            print(title, price)
            price_title.append((price, title, url))
        except Exception as e:
            print(e)
            e
            pass

    return price_title


def query_maker(query):
    param = ''
    for keyword in query.split():
        param += keyword
    return param


def get_image_url(url):
    try:
        soup = BeautifulSoup(requests.get(url).content, 'html.parser')
        return soup.findAll("div", {"class": "mms-zoom-image"})[0].find('img').get('src')
    except:
        print('failed to get img  url for ', url)
        return ""


def create_price_records(price_title):
    shop = Shop.objects.get(title='mediamarkt')
    for pt in price_title:
        try:
            product = Product.objects.get(title=pt[1], shop=shop)
        except Product.DoesNotExist:
            product = Product.objects.create(
                title=pt[1],
                shop=shop,
                image=get_image_url(pt[2])
            )
            print('image', product.image)
        price_obj = Price.objects.create(
            price=pt[0].split(',')[0],
            currency=Currency.objects.get(title='Euro'),
            product=product,
            url=pt[2]
        )


if __name__ == '__main__':
    from scrappers.utils import get_products
    products = get_products()
    for product in products:
        print('-- product --', product)
        query = query_maker(product)
        price_title = get_price_title(query)
        create_price_records(price_title)
        time.sleep(2)
