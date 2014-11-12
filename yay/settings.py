# -*- coding: utf-8 -*-

# Scrapy settings for yay project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'yay'

SPIDER_MODULES = ['yay.spiders']
NEWSPIDER_MODULE = 'yay.spiders'

ITEM_PIPELINES = (
        'yay.pipelines.YayPipeline',
        )

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'yay (+http://www.yourdomain.com)'
CONCURRENT_REQUESTS=128

SITES_DB = "yay"
DB_HOST = "172.17.0.109"
DB_PORT = 5432
DB_USER = "sardor"
DB_PASSWORD = "sardor"
