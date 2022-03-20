import json
import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import pandas as pd

# FILE_NAME = "case"


def parse(url):
    # list = {'description': [], 'url': [],
    #         'price': []}
    url_list = []
    r = requests.get(url)
    if r.status_code == 200:
        with open("test.txt", "w") as f:
            f.write(f"{r.text}\n")
        soup = bs(r.text, 'html.parser')
        urls = soup.find_all(
            'div',
            class_='product-snippet_ProductSnippet__description__xti7vm',
        )[:10]
        # for href in urls:
        #     url_list.append('https://aliexpress.ru'+href.a['href'])
        for href in urls:
            urllib.request.urlopen('https://aliexpress.ru'+href.a['href'])


        # describe = soup.find_all(
        #     'div', class_='product-snippet_ProductSnippet__name__xti7vm'
        # )[:10]
        # print(f"describe: {len(describe)}")
        prices = soup.find_all(
            'div', class_='snow-price_SnowPrice__mainS__18s9w6'
        )[:10]
        for price in prices:
            list['price'].append(price.text)
        # for discr in describe:
        #     list['description'].append(discr.text)
        for href in urls:
            url_list['url'].append('https://aliexpress.ru'+href.a['href'])
        return list
    if r.status_code == 400:
        status_code = {400: 'Bad request, try again!'}
        sc = json.dumps(status_code)
        return sc
    if r.status_code == 521:
        status_code = {521: 'Bad request, try again!'}
        sc = json.dumps(status_code)
        return sc
    if r.status_code == 204:
        status_code = {204: 'Bad request, try again!'}
        sc = json.dumps(status_code)
        return sc


while True:
    URL_TEMPLATE = 'https://aliexpress.ru/wholesale?catId=&SearchText='+input('search_word:')

    df = pd.DataFrame(data=parse(url=URL_TEMPLATE))
    print(df)
    # df.to_csv(FILE_NAME)
