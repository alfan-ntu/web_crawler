"""
    Description: This is the primary part of the Spider in the Scrapy architecture; It
                 performs a login action to get the authenticated response from the target
                 site, https://www.twse.com.tw/
    Date: 2024/1/22
    Author:
    Version: 0.1a
    Revision History:
        - 2024/1/22: v. 0.1a the initial version
    Reference:
            1)
    Notes: This scrapy project intended to crawl the stock price listed from TWSE
    ToDo's  :
        -
"""
import scrapy
from scrapy.utils.response import open_in_browser


class StockPriceSpiderSpider(scrapy.Spider):
    name = "stock_price_spider"
    allowed_domains = ["www.twse.com.tw"]
    start_urls = ["https://www.twse.com.tw/zh/trading/historical/stock-day.html"]

    def parse(self, response):
        open_in_browser(response)
        stockNo = '1101'
        date = '20240122'
        response_type = 'json'
        session_tag = '1706758737378'
        url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY"
        print(f'Response URL: {response.url}')
        # self.dump_cookies(response)

        request = scrapy.FormRequest(
            url=url,
            formdata={
                'date': date,
                'stockNo': stockNo,
                'response': response_type,
                '_': session_tag
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
            },
            method='GET',
            callback=self.after_login
        )
        print(f'Request URL: {request.url}')
        self.logger.info(f'Request URL: {request.url}')
        self.logger.info(f'Request Method: {request.method}')
        self.logger.info(f'Request Header: {request.headers}')
        self.logger.info(f'Request Body: {request.body}')
        yield request

    def dump_cookies(self, response):
        # Extract cookies from the response headers
        cookies = response.headers.getlist('Set-Cookie')
        print(f'Parsing cookie {cookies}...')
        # List cookies
        for cookie in cookies:
            self.logger.info(f'Cookie: {cookie.decode("utf-8")}')

    def after_login(self, response):
        # self.logger.info(f'Stock price returned from {response.url}')
        # response.encoding = 'utf-8'
        open_in_browser(response)
