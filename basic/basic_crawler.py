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
           one. One of the alternatives to resolve this sequential arrangement is using a more
           sophisticated  framework Scrapy

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
        #
        # Note that headers should be added to mimic a request from a web browser
        # Encountering 403 Forbidden otherwise
        #
        headers={'User-Agent': 'Mozilla/5.0'}
        return requests.get(url, headers=headers).text

    def get_linked_urls(self, url, html):
        """
        Extract embedded links in an HTML file and compose full URL's for creating
        the url list for visit, i.e. self.urls_to_visit[]

        :param url:
        :param html:
        :return:
        """
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            # logging.info(f'Anchor added: {path}')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            yield path

    def add_url_to_visit(self, url):
        """
        If the URL fetched from the website does not exist in either in the visited_urls[] and
        urls_to_visit[], append the url to the list urls_to_visit

        :param url: url under investigation
        :return: updated urls_to_visit list
        """
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        """
        Extracting embedded links and adding them to an url list for visiting

        :param url, url to visit
        :return: updated url list
        """
        html = self.download_url(url)
        # logging.info(f'HTTP Response: {html}')
        for url in self.get_linked_urls(url, html):
            self.add_url_to_visit(url)

    def run(self):
        """
        Visit the url from the url list one-by-one
        :return:
        """
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
