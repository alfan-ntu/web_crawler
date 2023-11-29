# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_url = scrapy.Field()
    price = scrapy.Field()
    title = scrapy.Field()
    img_url = scrapy.Field()


class GfgSpiderreadingitemsItem(scrapy.Item):
    """
    Define the fields for scrapy item here in class
    """
    # Item key for Title of Quote
    title = scrapy.Field()

    # Item key for Author of Quote
    author = scrapy.Field()

    # Item key for Tags of Quote
    tags = scrapy.Field()