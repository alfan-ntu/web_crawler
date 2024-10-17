from pathlib import Path
import scrapy
from ..items import QuoteItem

# Debugging the code using Scrapy Shell
from scrapy.shell import inspect_response


class QuoteSpider(scrapy.Spider):
    name = "quotes"     # spider name that scrapy uses to identify the specific scraping operation
    allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ["https://quotes.toscrape.com/"]

    # Starting point of a spider
    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        # url = "https://quotes.toscrape.com/"
        # yield scrapy.Request(url=url, callback=self.parse)

    # The method processing the response from the website and extract the data from within
    def parse(self, response):
        # Typical way to yield parsed content
        # for quote in response.css('div.quote'):
        #     yield {
        #         "text": quote.css('span.text::text').get(),
        #         "author": quote.css('small.author::text').get(),
        #         "tags": quote.css('div.tags a.tag::text').getall(),
        #     }
        #
        # Yield parsed content by item object
        # inspect_response(response, self)
        quote_item = QuoteItem()
        for quote in response.css('div.quote'):
            quote_item['text'] = quote.css('span.text::text').get()
            quote_item['author'] = quote.css('small.author::text').get()
            quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
            yield quote_item

        # # Follow the links
        # next_page = response.css('li.next a::attr(href)').get()
        # # if next_page is not None:
        # #     next_url = response.urljoin(next_page)
        # #     yield scrapy.Request(next_url, callback=self.parse)
        # # An alternative to schedule this new Request without urljoin listed below
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
