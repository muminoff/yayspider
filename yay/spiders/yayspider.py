# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from yay.items import SiteItem
from tldextract import extract
import redis


class YaySpider(scrapy.Spider):
    name = "yayspider"
    allowed_domains = ["xushnudbek.uz"]
    start_urls = ('http://www.xushnudbek.uz/',)
    link_extractor = SgmlLinkExtractor()
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

    def is_domestic(self, raw_url):
        return extract(raw_url).tld == 'uz'

    def parse(self, response):
        hxs = scrapy.Selector(response)
        item = SiteItem()
        item['fqdn'] = extract(response.url).registered_domain
        item['url'] = response.url
        item['title'] = hxs.xpath('//html/head/title/text()').extract()[0]
        item['content'] = response.body

        r = redis.Redis(connection_pool=self.pool)
        raw_links = self.link_extractor.extract_links(response)
        tld_links = [link.url for link in raw_links if self.is_domestic(link.url)]
        filtered_links = []
        for link in tld_links:
            if not r.sismember('urls', link):
                r.sadd('urls', link)
                filtered_links.append(link)

        yield item

        for link in filtered_links:
            yield scrapy.http.Request(url=link, callback=self.parse)
