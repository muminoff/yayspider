# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from datetime import datetime
from peewee import *


# psql_db = PostgresqlDatabase('yay', host='172.17.0.109', port=5432, user='sardor', password='sardor')
psql_db = PostgresqlDatabase(
        settings["SITES_DB"],
        host=settings["DB_HOST"],
        port=settings["DB_PORT"],
        user=settings["DB_USER"],
        password=settings["DB_PASSWORD"]
        )

class BaseModel(Model):
    """ Base model for PostgreSQL database """
    class Meta:
        database = psql_db


class Site(BaseModel):
    fqdn = CharField()
    title = CharField()
    url = CharField()
    content = TextField()


class YayPipeline(object):
    def process_item(self, item, spider):
        Site.create(
                fqdn=item['fqdn'],
                title=item['title'],
                url=item['url'],
                content=item['content'],
                crawled_at=datetime.now()
                )
        return item




