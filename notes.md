# Development Notes
### Engineering Notes
#### <u>Scrapy Fundamentals</u>
- The way to create a Scrapy project framework after Scrapy is successfully installed
```
    scrapy startproject <project_name>
```
For example, a new project named scrapy_crawler, the following file structure will be generated
```
    scrapy_crawler/
    
    ├── scrapy.cfg
    └── scrapy_crawler
        ├── __init__.py
        ├── items.py
        ├── middlewares.py
        ├── pipelines.py
        ├── settings.py
        └── spiders
            ├── __init__.py
```

- Then use the command genspider to create a basic spider skeleton. This creates example.py in the directory 'spiders' of the above file structure

```
    scrapy genspider example example.com
```

```
    ├── scrapy.cfg
    └── scrapy_crawler
        ├── __init__.py
        ├── items.py
        ├── middlewares.py
        ├── pipelines.py
        ├── settings.py
        └── spiders
            ├── __init__.py
            ├── example.py     <-- Newly created
```

- Run a scrapy crawler

    After generating a selector, e.g. example from the last command, use the crawl command of Scrapy to execute the crawler
```
    scrapy crawl <spider_name>
```
execution with log file created 
```
    scrapy crawl <spider_name> --logfile <spider_log_name>
```

#### <u> Customized User Agent </u>
Some web servers block requests from automation agents, like Scrapy
```commandline
    "user-agent": "Scrapy/2.11.0 (+https://scrapy.org)"
```
Customize the User-Agent either globally or in a local scope to any other popular user agents is a fix to this issue. Refer to the article [Scrapy User Agent](https://www.zenrows.com/blog/scrapy-user-agent#set-new-ua-with-middleware) for descriptions about configuring User-Agent either globally in settings.py or locally in <spider_name>.py

#### <u>Web Crawling at Scale in Scrapy</u>
It is import to configure the crawling behaviour properly in settings.py especially when the potential size of this crawling is huge, such as a website like IMDb, which contains over 130 million pages. Configurable parameters includes:

- USER_AGENT
- DOWNLOAD_DELAY
- CONCURRENT_REQUESTS_PER_DOMAIN
- AUTOTHROTTLE_ENABLED

#### <u>Spider Types</u>
There are a few pre-defined spider class in Scrapy
- **Spider**: fetches the content of each URL, defined in start_urls, and passes its content to the function *parse()* for data extraction
- **CrawlSpider**: follows links defined by a set of rules
- **CSVFeedSpider**: extracts tabular data from CSV URLs
- **SitemapSpider**: extracts URLs defined in a sitemap
- **XMLFeedSpider**: similar to the CSV spider, but handles XML URLs

#### <u>Middlewares</u>
Middlewares sit between the engine and the downloader, providing a way to alter and extend the default behavior of Scrapy's components. There are several types of middlewares in Scrapy:
- **Downloader Middleware**: Download middleware processes requests before they are sent to the downloader and responses before they reach the spider
- **Spider Middleware**: Spider middleware processes requests when they are sent to the spider and responses when they are returned from the spider.
- **Item Middleware**: Item middleware processes items before they are sent to the item pipeline.

Note that Downloader middleware and Spider middleware are implemented in the file middlewares.py. You need to enable/disable them in the configuration file, settings.py


### Journals
- 2023/11/16
    - Encountered '403 Forbidden' response from a simple HTTP request, requests.get(url).
      This means the server rejects the simple bot-like request.
      Fix in download_url(self, url) by adding a request header
```
      headers={'User-Agent': 'Mozilla/5.0'}
      html = requests.get(url, headers=headers).text
```

- 2023/11/17
    - In order to crawl the pages in parallel, we need to switch the basic framework according the article, [Web Crawling With Python](https://www.scrapingbee.com/blog/crawling-python/)
  
- 2023/11/20
  - Open issue: In some cases, we may run into websites that require us to execute JavaScript code to render all the HTML.  
  - Finished the article, [Web Crawling With Python](https://www.scrapingbee.com/blog/crawling-python/). Started another article [Scrapy Tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html). 
  
- 2023/11/22~24
  - Studied how to terminate the crawling process when a specific condition meets. 
  - Raise the exception CloseSpider(Exception) to close the spider in the request callback function. NOTE: Scrapy is an asynchronous framework. The spider will not terminate immediately when this exception is raised.
  - Studied new concept 'select' of the Scrapy framework; Selectors are CSS or XPath expressions, written to extract data from the HTML documents
  - CSS attributes can be identified by Right-Clicking the element of interest and choosing option from the
  - Another interesting tutorial can be found on [Geek For Geeks](https://www.geeksforgeeks.org/how-to-use-scrapy-items/). In which, how the Selector can be identified by inspecting the returned page html file is explained.

- 2023/11/27 ~ 2023/12/1
  - Found another comprehensive and detailed tutorial, [Scrapy Course](https://youtu.be/mBoX_JCKZTE?si=shpV8UxqEKymm-Ha) Hopefully, this will be the last tutorial to go through before wrapping up this topic.
  - Installed the interactive shell package, ipython and enable it in scrapy.cfg, so that we have a friendly shell environment when executing Scrapy's functions. It looks like below:

```commandline
[s] Available Scrapy objects:
[s]   scrapy     scrapy module (contains scrapy.Request, scrapy.Selector, etc)
[s]   crawler    <scrapy.crawler.Crawler object at 0x000001F1D28AB310>
[s]   item       {}
[s]   settings   <scrapy.settings.Settings object at 0x000001F1D28AAFB0>
[s] Useful shortcuts:
[s]   fetch(url[, redirect=True]) Fetch URL and update local objects (by default, redirects are followed)
[s]   fetch(req)                  Fetch a scrapy.Request and update local objects
[s]   shelp()           Shell help (print this help)
[s]   view(response)    View response in a browser
2023-11-29 11:28:22 [asyncio] DEBUG: Using selector: SelectSelector
In [1]: fetch('https://books.toscrape.com/')
```
___
Combining both this shell functions with the inspection of the web page we're querying or scraping, it'll be easy to locate and fetch the content of interest.

```commandline
In [6]: books = response.css('article.product_pod')

2023-11-29 11:37:54 [asyncio] DEBUG: Using selector: SelectSelector
In [7]: len(books)
Out[7]: 20

2023-11-29 11:38:00 [asyncio] DEBUG: Using selector: SelectSelector
In [8]: book = books[0]

2023-11-29 11:44:23 [asyncio] DEBUG: Using selector: SelectSelector
In [9]: book.css('h3 a::text').get()
Out[9]: 'A Light in the ...'
```

- 2023/11/27 ~ 2023/12/1(continued)
  - Experiment crawling and scraping continuous pages, again by experimenting in the Scrapy shell environment. For example, grabbing the next button and its associated anchor href.
     
    > response.css('li.next a').attrib['href']
  
    > response.css('li.next a ::attr(href)').get()
    
  - 'Scrapy shell' is very important for composing the selector statement  
  - Configure the output from running 'scrapy crawl <spider> ' by adding --logfile <logfile> -O <output_file>
       
    > scrapy crawl bookspider --logfile bookspider.log -O bookdetails.csv
  


     

