import scrapy


class AuthorSpider(scrapy.Spider):
    name = "author"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        # parse authors from all the quotes
        authors = response.css('div.quote span a::attr(href)').getall()
        for author in authors:
            next_author_url = response.urljoin(author)
            yield scrapy.Request(url=next_author_url, callback=self.parse_author)
        # follow the links and create further requests
        # next_url = response.css('li.next a::attr(href)').get()
        # next_url = response.urljoin(next_url)
        # if next_url is not None:
        #     yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get().strip()

        yield {
            "name": extract_with_css('h3.author-title::text'),
            "birthdate": extract_with_css('span.author-born-date::text'),
            "bio": extract_with_css('div.author-description::text')
        }
