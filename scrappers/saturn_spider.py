from bs4 import BeautifulSoup
import requests
from urllib import parse

from scrappers.base_spider import BaseRequestSpider


class SaturnSpider(BaseRequestSpider):
    shop_title = "Saturn"
    currency_title = "Euro"
    search_page = 'http://www.saturn.de/de/search.html'

    def __init__(self):
        super(SaturnSpider, self).__init__()

    def get_price_title(self, query):
        price_title = []
        response = requests.get(
            self.search_page,
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
                url = parse.urljoin(self.search_page, url)
                price_wrappers = wrapper.findAll('div', {'class': 'price small'})
                price = price_wrappers[0].text
                price_title.append((price, title, url))
            except:
                pass

        return price_title

    def get_image_url(self, url):
        try:
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')
            return soup.findAll("a", {"class": "zoom"})[0].get('href')
        except:
            print('failed to get img  url for ', url)
            return ""


if __name__ == '__main__':
    obj = SaturnSpider()
    obj.start()
