"""
    Description: This is the primary part of the Spider in the Scrapy architecture
    Date: 2023/11/29
    Author:
    Version: 0.1b
    Revision History:
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


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    # allowed_domains limits the spider from scrawling websites external to
    # allowed_domain list
    allowed_domains = ["books.toscrape.com"]
    # there could be more than one URL's in this list so that the spider
    # crawls the urls within this list
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        # Use css selector to select product information of books
        # We may use the interactive environment in 'Scrapy shell' to experiment the
        # CSS selector before actually writing code here
        books = response.css("article.product_pod")

        # Extract book information one book by another
        for book in books:
            # Yielding key elements of the page
            yield {
                # css tags
                "name" : book.css('h3 a::text').get(),
                # class tags
                "price" : book.css('.product_price .price_color::text').get(),
                "url" : book.css('h3 a').attrib['href']
            }

        # Process the next page button to continue the crawling until no more pages left
        next_page = response.css('li.next a').attrib['href']
        if next_page is not None:
            if 'catalogue/' not in next_page:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/' + next_page
            # response.follow just returns a Request instance
            yield response.follow(next_page_url, callback=self.parse)

