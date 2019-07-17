import os
import sys
from scrappers.utils import get_products

this_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(os.path.dirname(this_dir), 'web'))
sys.path.append(os.path.join(os.path.dirname(this_dir), 'web', 'pricing'))

import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'web.settings'
django.setup()

from pricing.models import Product, Price, Currency, Shop


class BaseRequestSpider:
    shop_title = ""
    currency_title = ""

    def __init__(self):
        self.currency, created = Currency.objects.get_or_create(title=self.currency_title)
        self.shop, created = Shop.objects.get_or_create(title=self.shop_title, currency=self.currency)

    def start(self):

        products = get_products()
        for product in products:
            print('-- request sent for product -- {} to {}'.format(product, self.shop_title))
            query = self.query_maker(product)
            price_title = self.get_price_title(query)
            self.create_price_records(price_title)

    def query_maker(self, query):
        return '+'.join(query.split())

    def create_price_records(self, price_title):

        for pt in price_title:
            try:
                product = Product.objects.get(title=pt[1], shop=self.shop)
            except Product.DoesNotExist:
                print("creating new product", pt[1])
                product = Product.objects.create(
                    title=pt[1],
                    shop=self.shop,
                    image=self.get_image_url(pt[2])
                )
            price_obj = Price.objects.create(
                price=pt[0].split(',')[0],
                currency=self.currency,
                product=product,
                url=pt[2],
            )
