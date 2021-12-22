from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['news_database']
news_db = db.news


def lenta_parser(collection):
    url = 'https://lenta.ru'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    response = requests.get(url, headers=header)
    dom = html.fromstring(response.text)

    items = dom.xpath("//div[contains(@class, 'last24')]//a[contains(@class, 'card-mini')]")
    for item in items:
        news_data = {}
        name = item.xpath(".//span[contains(@class, 'card-mini')]/text()")
        ref = item.xpath(".//span[contains(@class, 'card-mini')]/../../@href")
        news_data['name'] = name[0]
        if not ref[0].startswith('https://lenta.ru'):
            ref_full = url + ref[0]
        else:
            ref_full = ref[0]
        news_data['ref'] = ref_full
        news_data['source'] = url
        ref_list = ref_full.split('/')
        news_data['date'] = f'{ref_list[6]}.{ref_list[5]}.{ref_list[4]}'
        if not collection.find_one(news_data):
            collection.insert_one(news_data)


lenta_parser(news_db)
print(news_db.count_documents({}))
for vacancy in news_db.find({}):
    pprint(vacancy)

