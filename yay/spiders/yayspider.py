# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from yay.items import SiteItem
from yay.models import Site
from tldextract import extract
import redis


class YaySpider(scrapy.Spider): 
    name = "yayspider"
    allowed_domains = ["kun.uz"]
    start_urls = ('http://kun.uz/',)
    link_extractor = SgmlLinkExtractor()
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

    def __init__(self, category=None, *args, **kwargs):
        from scrapy.conf import settings
        from peewee import PostgresqlDatabase
        psql_db = PostgresqlDatabase(
                settings["SITES_DB"],
                host=settings["DB_HOST"],
                port=settings["DB_PORT"],
                user=settings["DB_USER"],
                password=settings["DB_PASSWORD"]
                )
        try:
            psql_db.create_tables([Site], safe=True)
        except:
            pass
        super(YaySpider, self).__init__(*args, **kwargs)


    def is_domestic(self, raw_url):
        return extract(raw_url).tld == 'uz'

    def parse(self, response):
        hxs = scrapy.Selector(response)
        item = SiteItem()
        item['fqdn'] = extract(response.url).registered_domain
        item['url'] = response.url
        item['title'] = hxs.xpath('//html/head/title/text()').extract()[0].strip() or item['fqdn']
        item['content'] = hxs.xpath('//html/body/text()').extract()[0].strip()

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
