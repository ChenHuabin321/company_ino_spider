# -*- coding: utf-8 -*-
import scrapy


class BafangSpiderSpider(scrapy.Spider):
    name = 'bafang_spider'
    allowed_domains = ['www.b2b168.com']
    start_urls = ['http://www.b2b168.com/']

    def parse(self, response):
        pass
