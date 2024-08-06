"""
    Description: This is the spider part of a scraper crawling and scraping office rent from the
                 website, https://sinyi.com.tw (信義房屋), crossing multiple pages
    Date: 2024/8/5
    Author: maoyi.fan@yapro.com.tw
    Version: 0.1a
    Revision History:
        - 2024/8/5: v. 0.1a the initial version
    Reference:
            1) https://www.scrapingbee.com/blog/crawling-python/
            2) https://thepythonscrapyplaybook.com/freecodecamp-beginner-course/freecodecamp-scrapy-beginners-course-part-4-first-scraper/

    Notes:

    ToDo's  :
        - Allow user to input information of location, usage, area size to compose flexible
          request URLs
"""

import scrapy
#
# Use regular expression(re) functions to extract current page property from certain script
# and use json function to extract the data easily
#
import re
import json


class RentspiderSpider(scrapy.Spider):
    """
    Description: spider class of the office_rent_scrapper project
    """
    name = "rentspider"
    allowed_domains = ["www.sinyi.com.tw"]
    # start_urls = ["https://www.sinyi.com.tw/rent/list/Taipei-city/114-104-zip/100-300-area/office-use/index.html"]
    start_urls = ["https://www.sinyi.com.tw/rent/list/Taipei-city/114-105-zip/100-up-area/store-use/index.html"]
    base_url = start_urls[0].rsplit("/", 1)[0] + "/"
    next_page_url = ""
    total_result_count = 0
    total_page_count = 0
    current_page = 1
    results_per_page = 20

    def get_total_record_count(self, response):
        """
        Description: Get the total number of selected offices for rent at the first response HTML replied
                     by sinyi webserver
        :param response:
        :return:
        """
        self.total_result_count = int(response.css('div#search_result_count .num::text').get())
        residual = self.total_result_count % self.results_per_page
        if residual == 0:
            self.total_page_count = self.total_result_count // self.results_per_page
        else:
            self.total_page_count = self.total_result_count // self.results_per_page + 1
        print(f'Total result count: {self.total_result_count}; Result per page: {self.results_per_page}; Total pages count: {self.total_page_count}')

    def get_page_limit(self, response):
        """
        Description: Extract the page limit number, limit, in the filter variable defined in <script>
        :param response:
        :return:
        """
        self.results_per_page = 20
        script_text = response.xpath('//script[contains(text(), "var search_limit")]/text()').get()
        pattern = r'var\s+search_limit\s*=\s*(\d+);'
        match = re.search(pattern, script_text)
        if match:
            json_str = match.group(1)
            self.results_per_page = int(json_str)

    def dict_key_check(self, dict, key):
        """
        Description: check if 'key' existed in the target dictionary 'dict', return True if yes,
                     return False otherwise
        :param dict:
        :param key:
        :return:
        """
        key_exist = False
        for k, v in dict.items():
            if k == key:
                key_exist = True
        return key_exist

    def get_current_page(self, response):
        """
        Description: page navigation is done through "page" property in the JavaScript variable 'filter'

        :param response: the HTML response
        :return: self.current_page is updated according to "page" property in the JSON dictionary
        """
        #
        # extract the variable declaration portion in the script part of the returned HTML
        # <script>
        # var areaAry=[{"cityid":"1","zipcode":"100","areaname":"\u4e2d\u6b63\u5340","lat":"25.042141","lng":"121.519872"}
        # var filter={"city":"Taipei","zip":["114","104"],"area":["100","300"],"use":["office"],"limit":20}
        # var search_limit=20
        #
        script_text = response.xpath('//script[contains(text(), "var filter")]/text()').get()
        pattern = r'var\s+filter\s*=\s*(\{.*?\})'
        match = re.search(pattern, script_text)
        if match:
            json_str = match.group(1)
            print(f'json_str: {json_str}')
            filter_dict = json.loads(json_str)
            if self.dict_key_check(filter_dict, "page"):
                self.current_page = int(filter_dict["page"])
                print(f'Current page: {self.current_page}/{self.total_page_count}')

            else:
                print(f'Current page: {self.current_page}/{self.total_page_count}')

            # self.current_page = int(filter_dict['page'])
            # print(f'Updated current page index: {self.current_page}/{self.total_page_count}')

    def get_next_page_url(self, response):
        if self.current_page < self.total_page_count:
            next_page = self.current_page + 1
            self.next_page_url = self.base_url + str(next_page) + ".html"
            print(f'Next page URL: {self.next_page_url}')

    def parse(self, response):
        print(f'Received response of {response.url}')
        if response.url == self.start_urls[0]:
            print(f'URL Base: {self.base_url}')
            self.get_page_limit(response)
            self.get_total_record_count(response)


        items = response.css('.search_result_item')
        # Iterate over each item and extract data
        for item in items:
            # Extract the item title
            title = item.css('.item_title::text').get()
            # Extract rent area
            detail_l2_spans = item.css('.item_detailbox .detail_line2 .num::text').getall()
            area = detail_l2_spans[1]
            address = detail_l2_spans[4]
            # Extract rent price
            price_new = item.css('.item_detailbox .price_new .num::text').get()
            price_val = price_new.replace(",", "")
            unit_price = round(float(price_val) / float(area), 0)
            # print out the query result
            # print(f'Item: {title}, Addr: {address}, Rent: {price_new}, Area: {area}, Unit Price: {unit_price}')
            yield{
                'Title': title,
                'Addr': address,
                'Rent': price_new,
                'Area': area,
                'Unit Price': unit_price
            }

        self.get_current_page(response)
        # print(f'Current page index: {self.current_page}/{self.total_page_count}')
        if self.current_page < self.total_page_count:
            self.get_next_page_url(response)
            # print(f'Next page url: {self.next_page_url}')
            yield response.follow(self.next_page_url, callback=self.parse)