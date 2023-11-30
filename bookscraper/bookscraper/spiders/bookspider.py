"""
    Description: This is the primary part of the Spider in the Scrapy architecture
    Date: 2023/11/29
    Author:
    Version: 0.1c
    Revision History:
        - 2023/11/30: v. 0.1c, add parsing function of book details pages
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
        """
        Callback function 'parse' to parse the HTML response per request

        :param response:
        :return:
        """
        # Use css selector to select product information of books
        # We may use the interactive environment in 'Scrapy shell' to experiment the
        # CSS selector before actually writing code here
        books = response.css("article.product_pod")

        # Extract book information one book by another within the response page
        for book in books:
            # go deeper to details of each book
            relative_url = response.css('h3 a ::attr(href)').get()
            if 'catalogue/' not in relative_url:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_page)

        # Process the next page button to continue the crawling until no more pages left
        next_page = response.css('li.next a').attrib['href']
        if next_page is not None:
            if 'catalogue/' not in next_page:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/' + next_page
            # response.follow just returns a Request instance
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        """
        Parse the book details page

        :param response:
        :return: book details record object
        """
        print(f'Response from {response.url}: {response} of status code:{response.status}')
        #  Fetch the table in the book details page
        table_rows = response.css("table tr")

        yield {
            'url': response.url,
            'title': response.css('.product_main h1::text').get(),
            'product_type': table_rows[1].css('td ::text').get(),
            'price_excl_tax': table_rows[2].css('td ::text').get(),
            'price_incl_tax': table_rows[3].css('td ::text').get(),
            'tax': table_rows[4].css('td ::text').get(),
            'availability': table_rows[5].css('td ::text').get(),
            'num_reviews': table_rows[6].css('td ::text').get(),
            'stars': response.css("p.star-rating").attrib['class'],
            'category': response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'price': response.css('p.price_color ::text').get(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
        }


