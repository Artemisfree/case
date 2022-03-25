import json
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def url_parse(url):
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
        for href in urls:
            url_list.append('https://aliexpress.ru'+href.a['href'])
        return url_list


def parse(url_list):
    for i in url_list:
        the_list = {'title': [], 'description': [], 'url': [],
                    'price': []}
        req = requests.get(i)
        if req.status_code == 200:
            with open("test2.txt", "w") as f:
                f.write(f"{req.text}\n")
            soup = bs(req.text, 'html.parser')
            titles = soup.find_all(
                'div', class_='Product_Name__container__hntp3'
            )
            describe = soup.find_all(
                'div', class_='detail-desc-decorate-richtext'
            )
            prices = soup.find_all(
                'div', class_='Product_Price__container__1uqb8 product-price'
            )
                # pubDate = soup.find_all(
                #     '', class_=''
                # )
            for title in titles:
                the_list['title'].append(title.text)
            for discr in describe:
                the_list['description'].append(discr.text)
            for price in prices:
                the_list['price'].append(price.text)
            the_list['url'].append(i)
            return the_list

        if req.status_code == 400:
            status_code = {400: 'Bad request, try again!'}
            sc = json.dumps(status_code)
            return sc
        if req.status_code == 521:
            status_code = {521: 'Web server is down, maybe later'}
            sc = json.dumps(status_code)
            return sc
        if req.status_code == 204:
            status_code = {204: 'No content, something else?'}
            sc = json.dumps(status_code)
            return sc


while True:
    URL_TEMPLATE = 'https://aliexpress.ru/wholesale?catId=&SearchText='+input(
        'search_word:')

    df = url_parse(url=URL_TEMPLATE)
    df1 = pd.DataFrame(data=parse(url_list=df))
    print(df1)
