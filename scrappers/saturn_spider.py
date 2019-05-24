from bs4 import BeautifulSoup
import requests
import os
import sys
from urllib import parse



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
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_wrappers = soup.findAll('div', {'class': 'product-wrapper'})
    for wrapper in product_wrappers:
        try:
            content = wrapper.findAll('div', {'class': 'content'})[0]
            title = content.findAll('h2')[0].text
            url = content.findAll('h2')[0].a.get('href')
            url = parse.urljoin(search_page, url)
            price_wrappers = wrapper.findAll('div', {'class': 'price small'})
            price = price_wrappers[0].text
            print(title, price)
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

    for pt in price_title:
        try:
            product = Product.objects.get(title=pt[1])
        except Product.DoesNotExist:
            product = Product.objects.create(
                title=pt[1],
                shop=Shop.objects.get(title='Saturn'),
            )
        price_obj = Price.objects.create(
            price=pt[0].split(',')[0],
            currency=Currency.objects.get(title='Euro'),
            product=product,
            url=pt[2]
        )


if __name__ == '__main__':
    print('enter the query')
    query = input()
    query = query_maker(query)
    price_title = get_price_title(query)
    create_price_records(price_title)