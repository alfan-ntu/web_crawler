import scrapy
from scrapy.utils.response import open_in_browser

class StockTypeSpider(scrapy.Spider):
    name = "stock_type"
    allowed_domains = ["isin.twse.com.tw"]
    # This means that the starting URL can be a java script file but, the following css
    # selector 'h2 strong font.h1 center::text' gets nothing.
    start_urls = ["https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"]

    def parse(self, response):
        title = response.css('h2 strong font.h1::text').get()
        print(f'Title of the page: {title}')
        update_time = response.css('h2 strong font.h1 center::text').get()
        print(f'Update time of the page: {update_time}')
        rows = response.css('tr')
        print(f'Number of rows in response: {len(rows)}')
        open_in_browser(response)
