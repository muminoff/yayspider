# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from datetime import datetime
from peewee import *
from yay.models import Site
import htmlmin


psql_db = PostgresqlDatabase(
        settings["SITES_DB"],
        host=settings["DB_HOST"],
        port=settings["DB_PORT"],
        user=settings["DB_USER"],
        password=settings["DB_PASSWORD"]
        )


class YayPipeline(object):
    def process_item(self, item, spider):
        content_minimized = htmlmin.minify(item['content'].decode('utf-8'))
        Site.create(
                fqdn=item['fqdn'],
                title=item['title'],
                url=item['url'],
                content=content_minimized,
                crawled_at=datetime.now()
                )
        return item




