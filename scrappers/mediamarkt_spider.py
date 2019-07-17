from bs4 import BeautifulSoup
import requests
from urllib import parse
from scrappers.base_spider import BaseRequestSpider


class MediaMarktSpider(BaseRequestSpider):
    shop_title = "mediamarkt"
    currency_title = "Euro"
    search_page = 'https://www.mediamarkt.de/de/search.html'

    def __init__(self):
        super(MediaMarktSpider, self).__init__()

    def get_price_title(self, query):

        price_title = []
        search_page = 'https://www.mediamarkt.de/de/search.html'
        response = requests.get(
            search_page,
            params={
                'query': query,
            }
        )
        soup = BeautifulSoup(response.content, 'html.parser')

        product_wrappers = soup.findAll('a', {'class': 'mms-link mms-srp-product'})
        for wrapper in product_wrappers:
            try:
                # content = wrapper.findAll('div', {'class': 'mms-product-row__grid'})[0]
                title = wrapper.findAll('h2', {'class': 'mms-headline mms-headline--styling-level3'})[0].text
                url = wrapper.get('href')
                url = parse.urljoin(search_page, url)
                price_wrappers = wrapper.findAll('span', {'class': 'mms-price__price'})
                price = price_wrappers[0].text.split('.')[0]
                price_title.append((price, title, url))
            except Exception as e:
                print("meidamarkt exc", e)
        return price_title

    def get_image_url(self, url):
        try:
            soup = BeautifulSoup(requests.get(url).content, 'html.parser')
            return soup.findAll("div", {"class": "mms-zoom-image"})[0].find('img').get('src')
        except:
            print('@mediamrkt, failed to get img  url for ', url)
            return ""


if __name__ == '__main__':
    obj = MediaMarktSpider()
    obj.start()
