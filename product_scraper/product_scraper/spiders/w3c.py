import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner


class W3cSpider(CrawlSpider):
    name = "w3c"
    allowed_domains = ["www.w3.org"]
    start_urls = ["https://www.w3.org"]

    rules = (
        Rule(
            LinkExtractor(
                deny=[
                    re.escape('https://www.youtube.com/'),
                    re.escape('https://www.edx.org/'),
                    re.escape('https://gooroomee.com/'),
                    re.escape('https://www.sttark.com/'),
                    re.escape('https://www.igalia.com/'),
                    re.escape('https://tetralogical.com/'),
                    re.escape('https://www.uic.edu/'),
                    re.escape('https://chapters.w3.org/'),
                    re.escape('https://validator.w3.org/'),
                    re.escape('https://web-platform-tests.org/'),
                    re.escape('https://testthewebforward.org/docs/'),
                    re.escape('https://wpt.fyi/')
                ],
            ),
            callback='parse_item'
        ),
    )

    def parse_item(self, response):
        self.log(f'RESPONSE: {response.body}')