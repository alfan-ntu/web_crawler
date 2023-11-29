"""
    Description: This is a simple web crawler class
    Date: 2023/7/11
    Author:
    Version: 0.1a
    Revision History:
        - 2023/7/11: v. 0.1a the initial version
    Reference:
            1) https://www.scrapingbee.com/blog/crawling-python/
    Notes: This is a simple web scraper/crawler using requests and BeautifulSoup. Major defects of
           this combination is 'sequential' processing. That makes the crawler a very inefficient
           one. The cure to this defect is Scrapy
    ToDo's  :
        -
"""
import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO
)


class Crawler:
    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls

    def download_url(self, url):
        """
        Issue an HTTP request to the server, specified by the input parameter url

        :param url: request target
        :return: HTTP response text
        """
        # Note that headers should be added to mimic a request from a web browser
        headers={'User-Agent': 'Mozilla/5.0'}
        return requests.get(url, headers=headers).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        # logging.info(f'HTTP Response: {html}')
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                self.visited_urls.append(url)


if __name__ == '__main__':
    Crawler(urls=['https://www.imdb.com/']).run()
