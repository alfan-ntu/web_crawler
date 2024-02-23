"""
    Description: This is a sample code demonstrating use of SeleniumRequest to scrape a website dynamically
                 composed using JavaScript
    Date: 2024/2/19
    Author:
    Version: 0.1a
    Revision History:
        - 2024/2/19: v. 0.1a the initial version
    Reference:
            1) https://www.zenrows.com/blog/scrapy-selenium#how-to-use
            2) https://www.youtube.com/watch?v=kgW6dOe5MQM
    Notes:
        1) basic spider framework applying SeleniumRequest() to replace standard scrapy's Request()
        2) interact with web pages with scrapy-selenium middleware, including mouse scrolling,

    ToDo's  :
        -
"""
import scrapy
from ..items import QuoteItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class QuotesJsSpider(scrapy.Spider):
    name = "quotes_js"
    allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ["https://quotes.toscrape.com/js/"]

    def start_requests(self):
        url = 'https://quotes.toscrape.com/js/'
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            wait_time=3,
            wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'quote'))
        )

    def parse(self, response):
        quote_item = QuoteItem()
        for quote in response.css('div.quote'):
            quote_item['text']=quote.css('span.text::text').get()
            quote_item['author']=quote.css('small.author::text').get()
            quote_item['tags']=quote.css('div.tags a.tag::text').get()
            yield quote_item

