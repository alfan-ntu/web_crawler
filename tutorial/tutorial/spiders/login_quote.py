"""
    Description: This is the primary part of the Spider in the Scrapy architecture; It
                 performs a login action to get the authenticated response from the target
                 site, https://quotes.toscrape.com/
    Date: 2024/1/22
    Author:
    Version: 0.1a
    Revision History:
        - 2024/1/22: v. 0.1a the initial version
    Reference:
            1) https://www.youtube.com/watch?v=EijzO7n2-dg
    Notes: The scrapy project intended to exercise the skills required to scrape from
           dynamic web pages
    ToDo's  :
        -
"""
import scrapy
from scrapy.utils.response import open_in_browser
from ..items import QuoteItem


class LoginQuoteSpider(scrapy.Spider):
    name = "login_quote"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/login"]

    def parse(self, response):
        # Retrieve the CSRF(Cross-Site Request Forgery) token to compose a legitimate request in
        # addition to username and password pair
        # The corresponded html code of this CSRF token looks like
        # <input type="hidden" name="csrf_token" value="vFiOjaNnZSUEAxQMCTJVybguBLKtIGeosXqpPRmWHDkzdfhwYcrl"/>
        csrf_token = response.css('input[name="csrf_token"]::attr(value)').get()
        # Form data entry of username
        # <input type="text" class="form-control" id="username" name="username" />
        username = 'username'
        # Form data entry of password
        # <input type="text" class="form-control" id="password" name="password" />
        password = 'password'
        #
        # Compose the request according information filled in the form
        #
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                'scrf_token': csrf_token,
                'username': username,
                'password': password
            },
            callback=self.start_scraping
        )

    def start_scraping(self, response):
        '''
        Registered callback function when the username/password passes authentication
        :param response:
        :return:
        '''
        open_in_browser(response)
        title = response.css('h1 a::text').get()
        print(f'Title of the returned page is {title}')
        quote_item = QuoteItem()
        quotes = response.css('div.quote')
        for quote in quotes:
            quote_item['text']=quote.css('span.text::text').get()
            quote_item['author']=quote.css('small.author::text').get()
            quote_item['tags']=quote.css('div.tags a.tag::text').getall()
            yield quote_item