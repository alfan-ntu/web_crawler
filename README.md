# web scraping and crawling 
This is a simple web scraper/crawler program implemented in Python based on the packages requests and BeautifulSoup. 
On the other hand, a more powerful web crawling framework, scrapy, is also included. 

### Important Features
A list of important features to be implemented is shown below
1. Basic access of a specified URL
2. Access of content with authentication
3. Store table content to local Excel files using XlsxWriter or similar Python packages
4. Access paginated contents
5. Allow flexible swap of processor performing specific on the contents received from crawling
6. Able to crawl/scrape online shopping site to get quotes of commodities and a stock website to obtain the stock price of a specific company

### Basic Project Information
- Start date: 2023/7/21

### Prerequisite
- Requests: A package to issue HTTP requests
```commandline
pip install requests
```
- Beautiful Soup: A full-featured HTML and XML parser
```commandline
pip install beautifulsoup4 
```
- Scrapy: A more powerful and versatile package which handles requests and responses asynchronously. In other words, it can handle requests/response in parallel

### Notes
- Some web-servers might prohibit requests from an automation application. Thus packing a custom agent header is a must in this case to avoid '403 Forbidden' response. 
```
    headers = {'User-Agent': 'Mozilla/5.0'}
    requests.get(url, headers=headers).text
```

### Reference
1. Web Crawling With Python: https://www.scrapingbee.com/blog/crawling-python/
2. 
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/WebCrawler_logotype_1995.svg/2560px-WebCrawler_logotype_1995.svg.png" width="150"> 
