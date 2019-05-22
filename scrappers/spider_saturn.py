from bs4 import BeautifulSoup
import requests


search_domains = {
    'saturn': 'www.saturn.de/de/search.html'
}


def get_price_title(query):
    price_title = []
    response = requests.get(
        'http://www.saturn.de/de/search.html',
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
            title = title.strip()
            price_wrappers = wrapper.findAll('div', {'class': 'price small'})
            price = price_wrappers[0].text
            print(title, price)
            price_title.append((price, title))
        except:
            pass

    return product_wrappers


def query_maker(query):
    param = ''
    for keyword in query.split():
        param += keyword
    return param


if __name__ == '__main__':
    query = input()
    query = query_maker(query)
    get_price_title(query)
