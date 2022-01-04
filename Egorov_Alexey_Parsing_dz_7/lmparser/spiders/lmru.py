import scrapy
from scrapy.http import HtmlResponse
from lmparser.items import LmparserItem
from scrapy.loader import ItemLoader


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__(search)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="product-name"]')
        for link in links:
            yield response.follow(link, callback=self.parse_goods)

    def parse_goods(self, response: HtmlResponse):
        # print()
        loader = ItemLoader(item=LmparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('photo', '//source[contains(@media, " only screen and (min-width: 1024px)")]/@srcset')
        loader.add_value('url', response.url)
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        print()
        yield loader.load_item()

        # name = response.xpath('//h1/text()').get()
        # photo = response.xpath('//source[contains(@media, "1024px")]/@srcset').getall()
        # url = response.url
        # price = response.xpath('//span[@slot="price"]/text()').get()
        # yield LmparserItem(name=name, photo=photo, url=url, price=price)


