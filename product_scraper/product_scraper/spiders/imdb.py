"""
    Description: This is the primary part of the Spider in the Scrapy architecture
    Date: 2023/7/17
    Author:
    Version: 0.1a
    Revision History:
        - 2023/7/11: v. 0.1a the initial version
    Reference:
            1) https://www.scrapingbee.com/blog/crawling-python/
    Notes: In order to improve the architecture based simply on requests and BeautifulSoup
           Scrapy framework is introduced.
    ToDo's  :
        -
"""
import re
import os, signal, sys

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.url import url_query_cleaner
import extruct

from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from scrapy.exceptions import CloseSpider


def process_links(links):
    """
    Remove duplicate links for the crawler and limit the number of crawled URLs

    :param links: list of links to clean up
    :return: list with duplicated links removed
    """
    # print(f'Process_links is called to process the list of links...')
    # print(f'links: {links}')
    for link in links:
        link.url = url_query_cleaner(link.url)
        yield link


class ImdbCrawler(CrawlSpider):
    """
    Spider class sub-class from CrawlSpider. A CrawlSpider follows links defined by a set of rules

    :param CrawlSpider
    """
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/']
    # Workaround of Scrapy's issue not filtering external links
    rules = (
        Rule(
            LinkExtractor(
                deny=[
                    re.escape('https://www.imdb.com/offsite'),
                    re.escape('https://www.imdb.com/whitelist-offsite'),
                    re.escape('https://www.instagram.com/'),
                    re.escape('https://www.tiktok.com/'),
                    re.escape('https://www.twitter.com/'),
                    re.escape('https://www.facebook.com/'),
                    re.escape('https://instagram.com/imdb'),
                    re.escape('https://twitter.com/imdb'),
                    re.escape('https://youtube.com/imdb'),
                    re.escape('https://facebook.com/imdb')
                    ]
            ),
            process_links=process_links,
            callback='parse_item',
            follow=False
        ),
    )
    count = 0
    pid = os.getpid()
    print(f'PID of the current process is: {pid}')

    def parse_item(self, response):
        '''
        Parse the response and return the url, metadata of the received HTML
        :param response, received content
        :param spider, this spider
        :return:
        '''
        self.count += 1
        print(f'Response {self.count} from {response.url}: {response} of status code:{response.status}')
        if self.count > 10:
            raise CloseSpider("Maximum crawled pages reached!")

        return {
            'url': response.url,
            'metadata': extruct.extract(
                response.text,
                response.url,
                syntaxes=['opengraph', 'json-ld']
            ),
        }

