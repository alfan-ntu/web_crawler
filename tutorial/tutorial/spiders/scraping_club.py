"""
    Description: This is a sample code demonstrating use of Selenium framework to crawl a dynamic website
    Date: 2024/2/19
    Author:
    Version: 0.1a
    Revision History:
        - 2024/2/19: v. 0.1a the initial version
    Reference:
            1) https://www.zenrows.com/blog/scrapy-selenium#how-to-use
    Notes:
        1) basic spider framework applying SeleniumRequest() to replace standard scrapy's Request()
        2) interact with web pages with scrapy-selenium middleware, including mouse scrolling,

    ToDo's  :
        -
"""
import scrapy
from scrapy_selenium import SeleniumRequest
# modules required for simulating human operations
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time


class ScrapingClubSpider(scrapy.Spider):
    name = "scraping_club"
    allowed_domains = ["scrapingclub.com"]
    # start_urls = ["https://scrapingclub.com/exercise/list_infinite_scroll/"]

    def start_requests(self):
        url = "https://scrapingclub.com/exercise/list_infinite_scroll/"
        yield SeleniumRequest(url=url,
                              callback=self.parse,
                              # wait for 5 seconds before closing Selenium
                              wait_time=5,
                              screenshot=True
                              )

    def parse(self, response):
        with open('screenshot.png', 'wb') as image_file:
            image_file.write(response.meta["screenshot"])
        # codes for mimicking human operations
        driver = response.request.meta["driver"]
        # click the first product element
        first_product = driver.find_element(By.CSS_SELECTOR, ".post")
        first_product.click()

        # Scroll to the end of the page 10 times
        for x in range(0, 10):
            # Scroll down by 10000 pixels
            ActionChains(driver) \
                .scroll_by_amount(0, 10000) \
                .perform()
            print(f'Viewing page {x}...')
            # waiting 2 seconds for the products to load. Brutal force style
            # time.sleep(2)
            # waiting for 60 elements found. Smarter ways
            wait = WebDriverWait(driver, timeout=10)
            wait.until(lambda driver: driver.find_element(By.CSS_SELECTOR, ".post:nth-child(60)")).is_displayed()
        #
        # Typical Scrapy spider
        #
        # for product in response.css(".post"):
            # scrape the desired data from each product
            # url = product.css("a ::attr(href)").get()
            # image = product.css("a img::attr('src')").get()
            # name = product.css("h4 a::text").get()
            # price = product.css("h5::text").get()
        #
        # Selenium WebDriver API
        #
        for product in driver.find_elements(By.CSS_SELECTOR, ".post"):
            # scrape the desired data from each product
            url = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            image = product.find_element(By.CSS_SELECTOR, ".card-img-top").get_attribute("src")
            name = product.find_element(By.CSS_SELECTOR, "h4 a").text
            price = product.find_element(By.CSS_SELECTOR, "h5").text

            yield {
                "url": url,
                "image": image,
                "name": name,
                "price": price
            }

