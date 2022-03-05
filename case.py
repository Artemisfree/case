import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

FILE_NAME = "case"


def parse(url):
    list = {'names': [], 'prices': [], 'urls': []}
    r = requests.get(url)
    if r.status_code == 200:
        soup = bs(r.text, 'html.parser')
        titles = soup.find_all(
            'div', class_='product-snippet_ProductSnippet__name__mdters'
        )[:10]
        prices = soup.find_all(
            'div', class_='snow-price_SnowPrice__mainS__18s9w6'
        )[:10]
        urls = soup.find_all(
            'div',
            class_='product-snippet_ProductSnippet__description__mdters'
        )[:10]
        for price in prices:
            list['prices'].append(price.text)
        for name in titles:
            list['names'].append(name.text)
        for href in urls:
            list['urls'].append('https://aliexpress.ru'+href.a['href'])
        return list
    if r.status_code == 400:
        return ('Bad request, try again!')
    if r.status_code == 521:
        return ('Web server is down, maybe later?')
    if r.status_code == 204:
        return ('No content, try somthing else')


while True:
    URL_TEMPLATE = 'https://aliexpress.ru/wholesale?catId=&SearchText='+input('search_word:')

    df = pd.DataFrame(data=parse(url=URL_TEMPLATE))
    df.to_csv(FILE_NAME)
