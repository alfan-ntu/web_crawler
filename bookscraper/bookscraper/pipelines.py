"""
    Description: Define here the models for your scraped items
    Date: 2023/12/12
    Author:
    Version: 0.1e
    Revision History:
        - 2023/12/14: v. 0.1e, added interface to store grabbed data to a database (disabled for now)
        - 2023/12/12: v. 0.1d, applied data processing routine before storing data to database
        - 2023/11/30: v. 0.1c, put all the data post-processing routines in pipelines.py

    Reference:
            1) https://youtu.be/mBoX_JCKZTE?si=NdyjlT7fLS1qAUec
            2) https://docs.scrapy.org/en/latest/topics/items.html

    Notes:
            1) Formal description of pipelines.py, where the item yielded by the spider get
               processed
            2) Remember to enable the pipeline routine by un-comment ITEM_PIPELINES
               in settings.py

    ToDo's  :
        -
"""

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        '''
        Post-processing the received data before storing them into external files or database

        :param item:
        :param spider:
        :return:

        Note: If the processing is not too complicated, items.py can do it as well
        '''
        adapter = ItemAdapter(item)
        #
        # Strip all leading and trailing whitespaces from strings
        #
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()
        #
        # Switch to lowercase for Category & Product Type
        #
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()
        #
        # Convert price string to float
        # Raw data looks like: "price_excl_tax": "£26.20", "price_incl_tax": "£26.20", "tax": "£0.00"
        #
        price_keys = ['price_excl_tax', 'price_incl_tax', 'tax', 'price']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)
        #
        # Extract numbers from the in stock strings
        # (Converting the number string to integer before storing it to database)
        # Raw data looks like: "availability": "In stock (14 available)"
        #
        availability_string = adapter.get('availability')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            stock_value = split_string_array[1].split(' ')[0]
            adapter['availability'] = int(stock_value)
        #
        # Extract number of reviews from the book details
        # (Converting string to integer before storing it to database)
        #
        num_review_string = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_review_string)
        #
        # Extract number of stars string from the book details to correspondent
        # integers
        #
        stars_string = adapter.get('stars')
        x = stars_string.split(' ')
        number_string = x[1].lower()
        match number_string:
            case "one":
                number = 1
            case "two":
                number = 2
            case "three":
                number = 3
            case "four":
                number = 4
            case "five":
                number = 5
            case _:
                number = 0
        adapter['num_reviews'] = number

        return item


#
# Database access section. Intended to skip this for the time being.
# import mysql.connector

# Associated with Part 7: Saving Data to File and Database in the tutorial
# class SaveToMySQLPipeline:
#
#     def __init__(self):
#         # Setup connection parameters
#         self.conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='',         # put password here
#             database='books'
#         )
#
#         # Create cursor, used to execute SQL commands
#         self.cur = self.conn.cursor()
#
#         # Create books table if none exists
#         self.cur.execute("""
#             CREATE TABLE IF NOT EXISTS books(
#                 id int NOT NULL auto_increment,
#                 url VARCHAR(255),
#                 title text,
#                 upc VARCHAR(255),
#                 product_type VARCHAR(255),
#                 price_excl_tax DECIMAL,
#                 price_incl_tax DECIMAL,
#                 tax DECIMAL,
#                 price DECIMAL,
#                 availability INTEGER,
#                 num_reviews INTEGER,
#                 stars INTEGERS,
#                 category VARCHAR(255),
#                 description text,
#                 PRIMARY KEY (id)
#             )
#             """
#         )
#
#     def process_item(self, item, spider):
#         # Define insert SQL statement
#         self.cur.execute("""
#             insert into books (
#                 url,
#                 title,
#                 upc,
#                 product_type,
#                 price_excl_tax,
#                 price_incl_tax,
#                 tax,
#                 price,
#                 availability,
#                 num_reviews,
#                 stars,
#                 category,
#                 description
#                 ) values (
#                     %s,
#                     %s,
#                     %s,
#                     %s,
#                     %s,
#                     %s,
#                     %s,
#                     %s,
#                     %s,
#                     %s,
#                     %s,
#                     %s,
#                     %s
#                 )""", (
#                     item['url'],
#                     item['title'],
#                     item['upc'],
#                     item['product_type'],
#                     item['price_excel_tax'],
#                     item['price_incl_tax'],
#                     item['tax'],
#                     item['price'],
#                     item['availability'],
#                     item['num_reviews'],
#                     item['stars'],
#                     item['category'],
#                     str(item['description'][0])
#                 )
#             )
#
#         # Execute insert of data into database
#         self.conn.commit()
#         return item
#
#     def close_spider(self, spider):
#         # housekeeping, close cursor & connection to database
#         self.cur.close()
#         self.conn.close()
