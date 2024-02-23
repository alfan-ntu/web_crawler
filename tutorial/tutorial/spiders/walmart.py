"""
    Description: This is a sample code implementing a product crawler. It also demonstrates
                 use of ScrapeOps Proxy Aggregator to deal with Walmart's anti-bot protection
    Date: 2024/2/21
    Author:
    Version: 0.1a
    Revision History:
        - 2024/2/21: v. 0.1a the initial version
    Reference:
            1) https://www.youtube.com/watch?v=VySakHZi6HI
            2) https://scrapeops.io/python-scrapy-playbook/python-scrapy-walmart-scraper/
    Notes:
        1) The primary difficulty to crawl Walmart's product website is to penetrate the anti-bot
           protection. One approach to do this is to use ScrapeOps Proxy service for which an API
           account needs to be registered and the python package 'scrapeops-scrapy-proxy-sdk' needs
           to be installed

    ToDo's  :
        -
"""
import scrapy
import json
import math
from urllib.parse import urlencode
import time


class WalmartSpider(scrapy.Spider):
    name = "walmart"
    allowed_domains = ["walmart.com"]
    start_urls = ["https://walmart.com"]

    def start_requests(self):
        keyword_list = ['ipad']
        for keyword in keyword_list:
            # Compose HTTP requests with correspondent payload
            payload = {'q': keyword, 'sort': 'best_seller', 'page': 1, 'affinityOverride': 'default'}
            walmart_search_url = 'https://www.walmart.com/search?' + urlencode(payload)

            yield scrapy.Request(url=walmart_search_url,
                                 callback=self.parse_search_results,
                                 meta={'keyword': keyword, 'page': 1})

    def parse_search_results(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword']
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        print(f'Received response from walmart for {keyword}')
        if script_tag is not None:
            json_blob = json.loads(script_tag)
            # Request product page
            product_list = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["items"]
            for product in product_list:
                walmart_product_url = 'https://www.walmart.com' + product.get('canonicalUrl', '').split('?')[0]
                yield scrapy.Request(url=walmart_product_url, callback=self.parse_product_data)
            # Request next page
            if page == 1:
                # extract product count information from the embedded JSON data structure
                total_product_count = json_blob["props"]["pageProps"]["initialData"]["searchResult"]["itemStacks"][0]["count"]
                print(f'Total product count: {total_product_count}')
                max_pages = math.ceil(total_product_count/40)
                # if max_pages > 25:
                #     max_pages = 25
                # Reduce max_pages to 3 for experimental purpose
                max_pages = 3
                for p in range(2, max_pages):
                    payload = {'q': keyword, 'sort': 'best_seller', 'page': p, 'affinityOverride': 'default'}
                    walmart_search_url = 'https://www.walmart.com/search?' + urlencode(payload)
                    yield scrapy.Request(url=walmart_search_url,
                                         callback=self.parse_search_results,
                                         meta={'keyword': keyword, 'page': p})
        else:
            print(f'Found no results of {keyword} ')


    def parse_product_data(self, response):
        # page = response.meta['page']
        # keyword = response.meta['keyword']
        script_tag = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()
        if script_tag is not None:
            # print(f'Successfully got the production information of "{keyword}"')
            json_blob = json.loads(script_tag)
            raw_product_data = json_blob["props"]["pageProps"]["initialData"]["data"]["product"]
            yield {
                # extract product information from the JSON blob by field name
                'id':  raw_product_data.get('id'),
                'type':  raw_product_data.get('type'),
                'name':  raw_product_data.get('name'),
                'brand':  raw_product_data.get('brand'),
                'averageRating':  raw_product_data.get('averageRating'),
                'manufacturerName':  raw_product_data.get('manufacturerName'),
                'shortDescription':  raw_product_data.get('shortDescription'),
                'thumbnailUrl':  raw_product_data['imageInfo'].get('thumbnailUrl'),
                'price':  raw_product_data['priceInfo']['currentPrice'].get('price'),
                'currencyUnit':  raw_product_data['priceInfo']['currentPrice'].get('currencyUnit'),
            }
        # else:
        #     print(f'Failed to get any results of "{keyword}"')