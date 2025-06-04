"""
    Description: This is the primary part of the Spider in the Scrapy architecture
    Date: 2023/12/18
    Author:
    Version: 0.1f
    Revision History:
        - 2023/12/18: v. 0.1f, added rotating proxy sample code
        - 2023/12/17: v. 0.1e, added randomized user-agent information
        - 2023/12/12: v. 0.1d, fixed books item bug and return item object
        - 2023/11/30: v. 0.1c, added parsing function of book details pages
        - 2023/11/29: v. 0.1b, basic parser yielding fields using css selectors; follow href anchor
                      to visit all pages from the starting page
        - 2023/7/11: v. 0.1a the initial version
    Reference:
            1) https://youtu.be/mBoX_JCKZTE?si=NdyjlT7fLS1qAUec
    Notes: In order to improve the architecture based simply on requests and BeautifulSoup
           Scrapy framework is introduced. And the tutorial shown in Reference 1) included
           comprehensive materials to go through the entire process from development to
           deployment
    ToDo's  :
        -
"""
import scrapy


# Import BookItem class from items.py
from ..items import BookItem

import random
from urllib.parse import urlencode


def get_proxy_url(url, enable_proxy=False):
    API_KEY = '2bb9eaa3-b008-48df-98fa-6b175af37535'
    if enable_proxy:
        payload = {'api_key': API_KEY, 'url':url}
        proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    else:
        proxy_url = url

    return proxy_url


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    # allowed_domains limits the spider from scrawling websites external to
    # allowed_domain list. The second item is necessary only when we implemented rotating
    # proxy method through ScrapeOps API
    allowed_domains = ["books.toscrape.com", "proxy.scrapeops.io"]
    # there could be more than one URL's in this list so that the spider
    # crawls the urls within this list
    start_urls = ["https://books.toscrape.com"]
    #
    # add a customized setting specific to this spider; FEEDS configures the output format
    # this is another way of configuration compared to that setting specified in settings.py
    #
    # custom_settings = {
    #     'FEEDS': {
    #         'booksdata.json': {'format': 'json'}
    #     }
    # }
    # Several ways to adjust user-agent. Refer to diary of 2023/12/11~2023/12/17 in notes.md
    # for details. This list will be used for randomly picking any one of them when composing
    # an HTML request in either response.follow(book_url,... or response.follow(next_page_url,
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
    ]

    def start_request(self):
        """
        Scrapy looks for this subroutine to compose customized request,
        only needed if we implement rotating proxy method and submit our requests via proxy and
        worry if the very first request is blocked by the target server
        :return:
        """
        # set a starting URL, arrange proxy and register callback parse function on receiving the response
        yield scrapy.Request(url=get_proxy_url(self.start_urls[0]), callback=self.parse)

    def parse(self, response):
        """
        Callback function 'parse' to parse the HTML response per request

        :param response:
        :return:
        """
        # Use css selector to select product information of books;
        # Each book is a line item described as
        #   <article class="product_pod">
        #   ...
        #   </article>
        # We may use the interactive environment in 'Scrapy shell' to experiment the
        # CSS selector before actually writing code here
        books = response.css("article.product_pod")
        #
        # Extract book information one book by another WITHIN the response page
        #
        for book in books:
            # go deeper to details of each book
            relative_url = book.css('h3 a ::attr(href)').get()
            # print(f'Book URL: {relative_url}')
            if 'catalogue/' not in relative_url:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/' + relative_url
            #
            # (1) submit requests with callback specified and spoofed user-agent; no need to add 'User-Agent' section
            # if more complicated ways to deal with dynamic user-agent information in middlewares.py
            # (2) apply rotating proxy servers by uncomment meta={...}
            # (3) the callback function self.parse_book_page() is registered so that it'll be called when the
            #     server returns the book details HTML response
            #
            book_url = get_proxy_url(book_url, False)
            yield response.follow(book_url,
                                  callback=self.parse_book_page,
                                  # headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]},
                                  # meta={"proxy": "http://username:password@gate.smartproxy.com:7000"}
                                  )
        #
        # Process the next page button to continue the crawling until no more pages left
        # There is no 'Next' button in the last page and the css selector fails to find 'next_page'
        #
        next_page = response.css('li.next a').attrib['href']
        if next_page is not None:
            if 'catalogue/' not in next_page:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/' + next_page
            # response.follow just returns a new Request instance with/without a spoofed user-agent
            print(f'Visit page: {next_page_url}')
            # (1) submit requests with callback function self.parse specified
            # (2) spoofed user-agent; no need to add 'User-Agent' section
            #     if more complicated ways to deal with dynamic user-agent information in middlewares.py
            # (3) apply rotating proxy servers by uncomment meta={...}
            next_page_url = get_proxy_url(next_page_url, False)
            yield response.follow(next_page_url,
                                  callback=self.parse,
                                  # headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]}
                                  # meta={"proxy": "http://username:password@gate.smartproxy.com:7000"}
                                  )

    def parse_book_page(self, response):
        """
        Parse the book details page and compose an item object

        :param response:
        :return: book details record object
        """
        # Fetch the table in the book details page. Notice the differences between response.css("table tr")
        # and response.css("table tr").getall()
        table_rows = response.css("table tr")
        #
        # Retrieve the book details and return the information of interest to the caller through a BookItem() class instance
        # The following selector statements can be collected from experiments in Scrapy shell. After 2024, ChatGPT can easily
        # compose the css selector statement if we simply copy and paste the HTML part and ask ChatGPT to generate the required
        # css selector code
        # 1) Each piece of book item information can be retrieved by using css selector, xpath selector,... etc. and stored in the
        #    dictionary
        # 2) In the Scrapy framework, dictionary-style access is preferred and recommended instead of Python standard way to access
        #    the class attribute. E.g. book_item['url'] = response.url better than book_item.url = response.url because Scrapy
        #    defines scrapy.Field class which accepts a dictionary argument, dict[str, Any]
        #
        book_item = BookItem()
        book_item['url'] = response.url
        # '.class_name' in the css selector string means selecting elements by their class_name attribute
        # '#id_name' in the css selector string means selecting elements by their id_name attribute
        book_item['title'] = response.css('.product_main h1::text').get()
        # otherwise selecting by their HTML tag name
        book_item['upc'] = table_rows[0].css('td ::text').get()
        book_item['product_type'] = table_rows[1].css('td ::text').get()
        book_item['price_excl_tax'] = table_rows[2].css('td ::text').get()
        book_item['price_incl_tax'] = table_rows[3].css('td ::text').get()
        book_item['tax'] = table_rows[4].css('td ::text').get()
        book_item['availability'] = table_rows[5].css('td ::text').get()
        book_item['num_reviews'] = table_rows[6].css('td ::text').get()
        book_item['stars'] = response.css("p.star-rating").attrib['class']
        # //ul ... means anywhere in the HTML response with HTML tag 'ul'
        # [@class='breadcrumb'] filters to only <ul> elements where the class attribute equals "breadcrumb"
        # /li ... locate the tag 'li' in the HTML response
        # [@class='active'] filters to only <li> elements where the class attribute equals "active"
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['price'] = response.css('p.price_color ::text').get()
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        # Yield a book_item object which is defined in items.py
        yield book_item

