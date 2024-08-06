"""
    Description: Define here the models for your scraped items
    Date: 2023/12/12
    Author:
    Version: 0.1d
    Revision History:
        - 2023/12/12: v. 0.1d, created book item object class
        - 2023/11/30: v. 0.1c, demonstrate the use of item class and use of serializer

    Reference:
            1) https://youtu.be/mBoX_JCKZTE?si=NdyjlT7fLS1qAUec
            2) https://docs.scrapy.org/en/latest/topics/items.html

    Notes:
            1) Formal description of items.py, a model for the extracted data. Spider's
               parser extracts contents of each correspondent item from the response.

    ToDo's  :
        -
"""
import scrapy
import re


def serialize_price(value):
    '''
    Item serializer post-process values from html response
    Use regular expression to remove non-digit or . from the string
    :param value:
    :return:
    '''
    # numeric_value = re.sub(r'[^0-9.]', '', value)
    # return f'${str(numeric_value)}'
    return value


class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class BookItem(scrapy.Item):
    '''
    Item Class which initializes all fields of a scraped item
    '''
    url = scrapy.Field()
    title = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    # Use serializer to post process received item details
    price_excl_tax = scrapy.Field(serializer=serialize_price)
    price_incl_tax = scrapy.Field(serializer=serialize_price)
    tax = scrapy.Field(serializer=serialize_price)
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field(serializer=serialize_price)
    description = scrapy.Field()
