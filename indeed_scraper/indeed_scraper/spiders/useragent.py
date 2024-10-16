import scrapy
import logging
from scrapy.utils.log import configure_logging
import random


class UseragentSpider(scrapy.Spider):
    name = "useragent"
    allowed_domains = ["httpbin.org"]
    # Check what the User_Agent is used for the crawling requests
    # start_urls = ["https://httpbin.org/user-agent"]
    # Check what the public IP is used for the crawling requests
    start_urls = ["https://httpbin.org/ip", "https://httpbin.org/user-agent",
                  "https://httpbin.org/headers", "https://httpbin.org/get",
                  "https://httpbin.org/cache"]
    # proxy_server = 'http://scrapeops:2bb9eaa3-b008-48df-98fa-6b175af37535@proxy.scrapeops.io:5353'
    proxy_server = 'http://47.74.152.29:8888'
    # customizing log output
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='useragent.log',
        format='@Maoyi -> %(levelname)s: %(message)s',
        level=logging.INFO
    )
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
    ]
    repeat_count = 5
    last_url_index = 0

    def get_user_agent(self):
        ua_len = len(self.user_agent_list)
        print(f'Length of user_agent_list: {ua_len}')
        ua_index = random.randint(0, ua_len-1)
        return ua_index, self.user_agent_list[ua_index]

    def get_http_request(self):
        url_len = len(self.start_urls)
        print(f'Length of url list: {url_len}')
        url_index = random.randint(0, url_len-1)
        return url_index, self.start_urls[url_index]

    def start_requests(self):
        # Setting a custom user-agent for this specific spider
        # headers = {'User-Agent':
        # 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
        idx, usr_agent = self.get_user_agent()
        print(f'Using {idx} user agent: {usr_agent}')
        headers = {'User-Agent': usr_agent}
        # for url in self.start_urls:
            # yield scrapy.Request(url, headers=headers)
        self.last_url_index, url = 0, self.start_urls[0]
        print(f'{self.repeat_count}th trial=>sending a request to: {url}')
        yield scrapy.Request(url=url,
                             callback=self.parse,
                             headers=headers,
                             dont_filter=True,
                             # meta={
                             #       'proxy': self.proxy_server,
                             # }
                             )

    def parse(self, response):
        # check if anything replied from the host
        self.logger.info('Received response from %s', response.url)
        # check the IP address returned by the proxy
        proxy = response.text

        self.logger.info(f'Host response: {proxy}')
        # self.logger.info('Through proxy server %s', response.request.meta['proxy'])
        user_agent = response.request.headers['User-Agent'].decode('utf-8')
        self.logger.debug(f'User-Agent being used: {user_agent}')
        self.repeat_count -= 1
        if self.repeat_count > 0:
            idx, usr_agent = self.get_user_agent()
            self.logger.info(f'{self.repeat_count} is using {idx} user agent: {usr_agent}')
            headers = {'User-Agent': usr_agent}
            idx = self.last_url_index
            while idx == self.last_url_index:
                idx, url = self.get_http_request()
            self.last_url_index = idx
            self.logger.info(f'{self.repeat_count}th trial=>sending a request to: {url}')
            print(f'{self.repeat_count}th trial=>sending a request to: {url}')
            yield scrapy.Request(url=url,
                                 headers=headers,
                                 callback=self.parse,
                                 dont_filter=True,
                                 # meta={
                                 #     'proxy': self.proxy_server
                                 # }
                                 )
