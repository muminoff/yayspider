from peewee import *
from scrapy.conf import settings

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
