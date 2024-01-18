from pathlib import Path
import scrapy


class QuoteSpider(scrapy.Spider):
    name = "quote"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f"quotes-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f'Saved file {filename}')
        # Parse the quotes one by one
        for quote in response.css('div.quote'):
            yield {
                "text": quote.css('span.text::text').get(),
                "author": quote.css('small.author::text').get(),
                "tags": quote.css('div.tags a.tag::text').getall(),
            }
        # Follow the links
        next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     next_url = response.urljoin(next_page)
        #     yield scrapy.Request(next_url, callback=self.parse)
        # An alternative to schedule this new Request without urljoin listed below
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

