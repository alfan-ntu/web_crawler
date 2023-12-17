"""
    Description: This is the primary part of the Spider in the Scrapy architecture
    Date: 2023/12/12
    Author:
    Version: 0.1e
    Revision History:
        - 2023/12/xx: v. 0.1e, added randomized user-agent information
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
from ..items import BookItem
import random


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    # allowed_domains limits the spider from scrawling websites external to
    # allowed_domain list
    allowed_domains = ["books.toscrape.com"]
    # there could be more than one URL's in this list so that the spider
    # crawls the urls within this list
    start_urls = ["https://books.toscrape.com"]
    #
    # add a customized setting specific to this spider; this is another way of configuration
    # compared to that setting specified in settings.py
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

    def parse(self, response):
        """
        Callback function 'parse' to parse the HTML response per request

        :param response:
        :return:
        """
        # Use css selector to select product information of books
        # We may use the interactive environment in 'Scrapy shell' to experiment the
        # CSS selector before actually writing code here
        books = response.css("article.product_pod")
        #
        # Extract book information one book by another within the response page
        #
        for book in books:
            # go deeper to details of each book
            relative_url = book.css('h3 a ::attr(href)').get()
            # print(f'Book URL: {relative_url}')
            if 'catalogue/' not in relative_url:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/' + relative_url
            # submit requests with callback specified and spoofed user-agent; no need to add 'User-Agent' section
            # if more complicated ways to deal with dynamic user-agent information in middlewares.py
            yield response.follow(book_url,
                                  callback=self.parse_book_page,
                                  # headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]}
                                  )
        #
        # Process the next page button to continue the crawling until no more pages left
        #
        next_page = response.css('li.next a').attrib['href']
        if next_page is not None:
            if 'catalogue/' not in next_page:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/' + next_page
            # response.follow just returns a new Request instance with/without a spoofed user-agent
            print(f'Visit page: {next_page_url}')
            yield response.follow(next_page_url,
                                  callback=self.parse,
                                  # headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]}
                                  )

    def parse_book_page(self, response):
        """
        Parse the book details page and compose an item object

        :param response:
        :return: book details record object
        """
        # print(f'Response: {response}; user-agent: {response.request.headers["User-Agent"]}')
        print(f'Response: {response}')
        # Fetch the table in the book details page
        table_rows = response.css("table tr")
        # Retrieve the book details and return the information of interest to the caller
        # The following selector statements can be collected from experiments in Scrapy shell
        book_item = BookItem()
        book_item['url'] = response.url
        book_item['title'] = response.css('.product_main h1::text').get()
        book_item['upc'] = table_rows[0].css('td ::text').get()
        book_item['product_type'] = table_rows[1].css('td ::text').get()
        book_item['price_excl_tax'] = table_rows[2].css('td ::text').get()
        book_item['price_incl_tax'] = table_rows[3].css('td ::text').get()
        book_item['tax'] = table_rows[4].css('td ::text').get()
        book_item['availability'] = table_rows[5].css('td ::text').get()
        book_item['num_reviews'] = table_rows[6].css('td ::text').get()
        book_item['stars'] = response.css("p.star-rating").attrib['class']
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['price'] = response.css('p.price_color ::text').get()
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        # Return a book_item object which is defined in items.py
        yield book_item

