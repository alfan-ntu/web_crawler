"""
    Description: Custom functionality to process the responses that are sent to Spiders for
                 processing and to process the requests and items that are generated from
                 spiders

    Date: 2023/12/18
    Author:
    Version: 0.1f
    Revision History:
        - 2023/12/18: v. 0.1f, added rotating proxy test code
        - 2023/12/14: v. 0.1e, modified the middlewares.py template first time to enable scrape
                              functionalities from a third party, ScrapeOps

    Reference:
            1) https://scrapeops.io/
            2) https://thepythonscrapyplaybook.com/freecodecamp-beginner-course/freecodecamp-scrapy-beginners-course-part-8-fake-headers-user-agents/#scrapeops-fake-user-agent-api

    Notes:
            1) Formal description of middlewares.py, where the request is modified before actually being
               sent to the web-server and the way scrapy handles the response

    ToDo's  :
        -
"""
# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BookscraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BookscraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


from urllib.parse import urlencode
from random import randint
import requests


class ScrapeOpsFakeUserAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        """
        This class method ensures that crawler.settings is ready to access when the class is
        initialized, i.e. __init__() is called
        Class method is used to ensure all class instances can get the same values of the
        configurable

        :param crawler:
        :return: the crawler settings specified in settings.py
        """
        return cls(crawler.settings)

    def __init__(self, settings):
        """
        Initialize the ScrapeOpsFakeUserAgentMiddleware class by reading the configuration parameters from
        settings.py. Remember to enable this in the section DOWNLOADER_MIDDLEWARES in settings.py and assign
        proper priority level
        :param settings:
        """
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT', 'http://headers.scrapeops.io/v1/user-agents?')
        self.scrapeops_fake_user_agents_active = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        # self.header_list = []
        self.user_agents_list = []     # my debug fix
        self._get_user_agents_list()
        self._scrapeops_fake_user_agents_enabled()

    def _get_user_agents_list(self):
        """
        Sending requests to ScrapeOps API endpoint with the API Key to get
        a specified number of user-agents from ScrapeOps
        :return: a list of dynamically generated user-agents information
        Note: Follow https://scrapeops.io/app/headers for an example to get a user-agent list
        """
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.user_agents_list = json_response.get('result', [])

    def _get_random_user_agent(self):
        """
        Generating a random index to fetch the correspondent user-agent from the list
        self.user_agents_list
        :return: randomly picked user-agent to spoof the webserver with different identity
        """
        random_index = randint(0, len(self.user_agents_list)-1)
        return self.user_agents_list[random_index]

    def _scrapeops_fake_user_agents_enabled(self):
        """
        Enable/Disable fake user-agent information according to the existence of ScrapeOps API Key or
        configurations in settings.py
        :return:
        """
        if self.scrapeops_api_key is None or self.scrapeops_api_key=='' or self.scrapeops_fake_user_agents_activescrapeops_fake_user_agents_active==False:
            self.scrapeops_fake_user_agents_active = False
        else:
            self.scrapeops_fake_user_agents_active = True

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        """
        Processing the request with randomly picked user-agent put in the request header
        :param request:
        :param spider:
        :return:
        """
        random_user_agent = self._get_random_user_agent()
        request.headers['User-Agent'] = random_user_agent
        # For debugging purpose
        # print("********** NEW HEADER ATTACHED **********")
        # print(request.headers['User-Agent'])


class ScrapeOpsFakeBrowseHeaderAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        """
        Initialize the ScrapeOpsFakeUserAgentMiddleware class by reading the configuration parameters from
        settings.py. Remember to enable this in the section DOWNLOADER_MIDDLEWARES in settings.py and assign
        proper priority level
        :param settings:
        """
        self.scrapeops_api_key = settings.get('SCRAPEOPS_API_KEY')
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT', 'http://headers.scrapeops.io/v1/user-agents?')
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_USER_AGENT_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self._get_headers_list()
        self._scrapeops_fake_browser_headers_enabled()

    def _get_headers_list(self):
        """
        Sending requests to ScrapeOps API endpoint with the API Key to get
        a header list from ScrpeOps website
        :return: a list of dynamically generated header information
        Note: Follow https://scrapeops.io/app/headers for an example to get a whole header list
        """
        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        response = requests.get(self.scrapeops_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.headers_list = json_response.get('result', [])

    def _get_random_browser_header(self):
        """
        Generating a random index to fetch the correspondent header from the list
        self.header_list
        :return: randomly picked header to spoof the webserver with different identity
        """
        random_index = randint(0, len(self.headers_list)-1)
        return self.headers_list[random_index]

    def _scrapeops_fake_browser_headers_enabled(self):
        if self.scrapeops_fake_browser_headers_active is None or\
           self.scrapeops_fake_browser_headers_active=='' or\
           self.scrapeops_fake_browser_headers_active==False:
            self.scrapeops_fake_browser_headers_active=False
        else:
            self.scrapeops_fake_browser_headers_active=True

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        """
        Processing the request with randomly picked browser header
        :param request:
        :param spider:
        :return:
        """
        random_browser_header = self._get_random_browser_header()

        request.headers['accept-language'] = random_browser_header['accept-language']
        request.headers['sec-fetch-user'] = random_browser_header['sec-fetch-user']
        request.headers['sec-fetch-mod'] = random_browser_header['sec-fetch-mod']
        request.headers['sec-fetch-site'] = random_browser_header['sec-fetch-site']
        request.headers['sec-ch-ua-platform'] = random_browser_header['sec-ch-ua-platform']
        request.headers['sec-ch-ua-mobile'] = random_browser_header['sec-ch-ua-mobile']
        request.headers['sec-ch-ua'] = random_browser_header['sec-ch-ua']
        request.headers['accept'] = random_browser_header['accept']
        request.headers['user-agent'] = random_browser_header['user-agent']
        request.headers['upgrade-insecure-requests'] = random_browser_header['upgrade-insecure-requests']


#
# Class MyProxyMiddleware is necessary only when we need to rotate the proxies to change spoof the website
# with changing IP address via proxy servers, e.g. smartproxy.com. No need to comment out this class
# as long as we do not enable it in DOWNLOADER_MIDDWARES in settings.py
#
# Note:
#   1) Remember to enable this in settings.py
#   2) Haven't yet verified this part of code due to security and smartproxy.com payment concern
import base64


class MyProxyMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.user = settings.get('PROXY_USER')
        self.password = settings.get('PROXY_PASSWORD')
        self.endpoint = settings.get('PROXY_ENDPOINT')
        self.port = settings.get('PROXY_PORT')

    def process_request(self, request, spider):
        user_credentials = '{user}:{passw}'.format(user=self.user, passw=self.password)
        basic_authentication = 'Basic ' + base64.b64encode(user_credentials.encode()).decode()
        host = 'http://{endpoint}:{port}'.format(endpoint=self.endpoint, port=self.port)
        request.meta['proxy']=host
        request.headers['Proxy-Authorization']=basic_authentication