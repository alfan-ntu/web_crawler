# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


def serialize_text(value):
    value = value.strip()
    return value


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QuoteItem(scrapy.Item):
    '''
    Item class initializing all fields of a scraped item. Necessary only if spider yielding
    item objects is implemented
    '''
    text = scrapy.Field(serialize=serialize_text)
    author = scrapy.Field()
    tags = scrapy.Field()


class AuthorItem(scrapy.Item):
    '''
    Item class initializing all fields of a scraped item. Necessary only if spider yielding
    item objects is implemented
    '''
    name = scrapy.Field()
    birthdate = scrapy.Field()
    bio = scrapy.Field()

