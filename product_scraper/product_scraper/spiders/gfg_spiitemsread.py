import scrapy
from ..items import GfgSpiderreadingitemsItem


class GfgSpiitemsreadSpider(scrapy.Spider):
    """
    Spider class sub-class from scrapy. A Spider follows links defined by a set of rules

    :param CrawlSpider
    """
    name = "gfg_spiitemsread"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/tag/reading"]
    count = 0

    def parse(self, response):
        """
        Selectors with XPath expressions responsible for data extraction from the response are
        implemented
        Note: selectors can be defined using CSS expressions as well.

        :param response:
        :return:
        """
        self.count += 1
        print(f'Response {self.count} from {response.url}: {response} of status code:{response.status}')
        quotes = response.xpath('//*[@class="quote"]')
        for quote in quotes:
            # Create an object of Item class
            item = GfgSpiderreadingitemsItem()

            # XPath expression to fetch text of the Quote title
            item['title'] = quote.xpath('.//*[@class="text"]/text()').extract_first()
            # XPath expression to fetch author of the Quote
            item['author'] = quote.xpath('.//*[@itemprop="author"]/text()').extract()
            # XPath expression to fetch tags of the Quote
            item['tags'] = quote.xpath('.//*[@itemprop="keywords"]/@content').extract()

            # Yield all elements
            yield item



