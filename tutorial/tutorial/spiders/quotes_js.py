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
            quote_item['tag']=quote.css('div.tags a.tag::text').get()
            yield quote_item

