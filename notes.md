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
      Fix in download_url(self, url) by adding a request header when composing an HTML request. See example download_url in basic_crawler.py which uses the package 'requests'.
```
      headers={'User-Agent': 'Mozilla/5.0'}
      html = requests.get(url, headers=headers).text
```

- 2023/11/17
    - In order to crawl the pages in parallel, we need to switch the basic framework according the article, [Web Crawling With Python](https://www.scrapingbee.com/blog/crawling-python/); Quote: "One of the advantages of Scrapy is that requests are scheduled and handled asynchronously. This means that Scrapy can send another request before the previous one has completed or do some other work in between."
    - Refer to basic_crawler.py for a basic, sequential crawler applying python packages, requests and BeautifulSoup
  
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
Combining both this shell functions with the inspection of the web page we're querying or scraping from, it'll be easy to locate and fetch the content of interest.

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

2023-12-12 21:11:07 [asyncio] DEBUG: Using selector: SelectSelector
In [11]: book.css('p.price_color::text').get()
Out[11]: '£50.10'
```

- 2023/11/27 ~ 2023/12/1(continued)
  - Experiment crawling and scraping continuous pages, again by experimenting in the Scrapy shell environment. For example, grabbing the next button and its associated anchor href.
     
    > response.css('li.next a').attrib['href']
  
    or

    > response.css('li.next a ::attr(href)').get()
    
  - 'Scrapy shell' is very important for composing the selector statement  
  - Configure the output from running 'scrapy crawl <spider> ' by adding --logfile <logfile> -O <output_file>
       
    > scrapy crawl bookspider --logfile bookspider.log -O bookdetails.csv
    
    or   
  
    > scrapy crawl bookspider --logfile bookspider.log -O bookdetails.json

  - Instead of yielding a long dictionary from a response parser callback function, we can define item prototype in Items.py. Items.py can also perform simple data serialization functions, such as removing non-digits from string, on specified fields. Refer to the function serialize_price() in items.py
  
    > price_excl_tax = scrapy.Field(serializer=serialize_price)

  - On the other hand, pipelines.py, provides a single interface for handling different item types. Whatever written in pipeline.py, remember to enable ITEM_PIPELINES in settings.py. This is an important part of data processing before storing data captured from HTML response to Database.

- 2023/12/11~2023/12/17
  - Resuming to this project after business travel to China. Continued **Part 6-Cleaning Data with Item Pipelines**. In summary, 'items.py' defines the item object, applies serialization function to specific item field if necessary. And, 'pipelines.py' collects data processing functions to each individual item field before storing and further processing the data collected from html response we scraped.
  - The command 'scrapy crawl' supports both -O and -o options which creates/overwrites and appends output to the specified file. 
  - On the other hand, file name extension specifies the type of output file. This can be configured in settings.py by adding a FEEDS section so that we don't need to add -o or -O when starting the crawling process. Refer to settings.py for an example. Another way to configure a customized setting in bookspider.py is to add 'custom_settings' section with FEEDS definition. This leads to a more customized setting specific to target spider. 
  - Skipped the section about accessing database, MySQL, which needs to install MySQL database and python packages mysql, mysql-connector-python. Another pipeline class, SaveToMySQLPipeline, needs to be added to pipelines.py and ITEM_PIPELINE section in settings.py
  - **Part 8: Fake User-Agents & Browser Headers**, since Scrapy requests might be blocked by some web servers due to security concern or server loading concern or simply an anti-bots policy. Use inspection-network function on the web page returned to retrieve 'user-agent' information to help pass through request check from the Web Server. Modify 'USER_AGENT' section in settings.py or compose a user_agent_list[] with randomly picked user-agent to spoof the webserver with different identities. This might not be enough for a visit to a more complex server which leads to Fake User Agent API. In summary, there are different ways to adjust the user-agent information in a request.
    - Modify USER_AGENT in settings.py
    - Modify the user-agent when composing requests in spider.py, either using one statically or using a list of user-agent. 
    ```
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36"
    ]
    ...
    yield response.follow(book_url,
                          callback=self.parse_book_page,
                          headers={"User-Agent": self.user_agent_list[random.randint(0, len(self.user_agent_list)-1)]},
                          meta={"proxy": "http://username:password@gate.smartproxy.com:7000"}
                          )
    ```
    - Or apply 3rd party API to get externally generated user-agent in middlewares.py, e.g. [ScrapeOps](scrapeops.io) provides API to create user-agent's on-the-fly, instead of listing them in the spider.py file. A description in details can be found in [Scrapy Playbook](https://thepythonscrapyplaybook.com/freecodecamp-beginner-course/freecodecamp-scrapy-beginners-course-part-8-fake-headers-user-agents/#how-to-set-a-fake-user-agent-in-scrapy). Remember to enable the modified middlewares.py in settings.py by un-comment 'DOWNLOADER_MIDDLEWARES'
    - **Part 8: Fake User-Agents & Browser Headers** (continued): Work-around to deal with anti-robot policy if robots.txt is set on the Webserver. 
    - In addition to change the user-agent part of a header in the request, we can apply ScrapeOps API to create a whole new header section, which is implemented as a class ScrapeOpsFakeBrowseHeaderAgentMiddleware in middlewares.py
  
- 2023/12/18~2023/12/24
  - **Part 9: Rotating Proxies & Proxy APIs**: Changing user-agents or even request headers might not be sophisticated enough if many requests with different user-agents, request headers are sent from the same IP address. This is why proxies are needed for the scraping client to hide its identity. However, scraping or visiting websites through proxy servers might introduce security issues, not to mention stability and performance issues. Went through the youtube materials [Part 9](https://www.youtube.com/watch?v=mBoX_JCKZTE&t=9612s) without actually applied them unless necessary later for other projects. Rotating proxy servers are provided by different service providers, either free(https://geonode.com/free-proxy-list) or paid(smartproxy.com) services.
    - **Alternative 1: Use ROTATING_PROXY_LIST in settings.py** in a static way. Experienced stability and performance issue while testing.
    - **Alternative 2: Use paid proxy service** and implement a dedicated class, e.g. MyProxyMiddleware, in middlewares.py
    - **Alternative 3: Get proxy service by ScrapeOps** in spider.py. get_proxy_url() function needs to be implemented in spider.py to pass API KEY and destination URL to it and get a proxy route to the destination. Refer to preparations to run response.follow() and allowed_domains in spider.py for details.
    - **Alternative 4: Use proxy SDK provided by ScrapeOps** by installing proxy-sdk package and add rotating proxy method in middlewares.py
    ```
    $ pip install scrapeops-scrapy-proxy-sdk
    ```
  - **Part 10: Run Spiders in Cloud with Scrapyd** Deployment/Scheduling/Monitoring Scrapyd. Several options to deploy Scrapyd. The first two need other cloud server service to deploy, e.g. cloud.digitalocean.com.
    - ScrapyD: Free & open source, need preparing a server
    - ScrapeOps: Free, need preparing a server
    - ScrapyCloud: paid, no servers needed
    
    General guidelines of launching a Scrapy application in the cloud: 
    - A cloud platform should be prepared first, such as AWS EC2.
    - On a new Ubuntu AWS EC2 AMI, install python-pip, virtual environment and activate the virtual environment
    ```
    $ sudo apt install python3-pip
    $ pip install virtualenv
    %% or I used
    $ sudo apt install python3-virtualenv
    %% git clone required repository; see the description below
    $ virtualenv venv
    $ source ./venv/bin/activate
    ```
    - 'git clone' the verified scrapy project to the cloud platform; pip install all the required python packages. Say if we're going to clone the tutorial project, https://github.com/python-scrapy-playbook/freeCodeCamp-part-6.git 
    ```
    $ pip install -r requirements.txt
    ```
    - Install ScrapyD using the following command. This is a service for running Scrapy spiders, with an HTTP API; Launch scrapyd and direct the output to a file. Follow the online user guide [ScrapydWeb](https://thepythonscrapyplaybook.com/extensions/scrapydweb-guide) for reference.
    ```
    $ pip install scrapyd
    $ scrapyd > scrapyd_logs.txt 2>&1 &
    ```
    - Use a curl command to check the daemon status. We simply started scrapyd service and yet hook up any spider. That's why daemonstatus.json simply shows no spider "running"
    ```
    $ curl http://localhost:6800/daemonstatus.json
    {"node_name": "ip-172-31-14-200", "status": "ok", "pending": 0, "running": 0, "finished": 0}
    ```
    - Now we have scrapyd service up and need to install a client for Scrapyd from GitHub
    ```
    $ pip install git+https://github.com/scrapy/scrapyd-client.git 
    $ pip show scrapyd-client
    Name: scrapyd-client
    Version: 1.2.3
    Summary: A client for Scrapyd
    Home-page: https://github.com/scrapy/scrapyd-client
    Author: Scrapy developers
    Author-email: info@scrapy.org
    License: BSD
    Location: /home/ubuntu/scrapy/freeCodeCamp-part-6/venv/lib/python3.10/site-packag
    Requires: requests, scrapy, uberegg, urllib3, w3lib
    Required-by:
    ```
    - Modify scrapy.cfg to enable HTTP service @ port 6800 by un-commenting the statement "url = http://localhost:6800" and deploy the spider using scrapyd-deploy command; After this deployment, we've registered a 'bookscraper' spider project
    ```
    $ scrapyd-deploy default
    Packing version 1703081222
    Deploying to project "bookscraper" in http://localhost:6800/addversion.json
    Server response (200):
    {"node_name": "ip-172-31-14-200", "status": "ok", "project": "bookscraper", "version": "1703081222", "spiders": 1}
    ```
    - Use curl command to start the spider
    ```
    $ curl http://localhost:6800/schedule.json -d project=default -d spider=bookspider
    %% After doing this scheduling, we can see a spider running using the daemonstatus.json command, 
    $ curl http://localhost:6800/daemonstatus.json
    2023-12-25T05:55:19+0000 [twisted.python.log#info] "127.0.0.1" - - [25/Dec/2023:05:55:19 +0000] "GET /daemonstatus.json HTTP/1.1" 200 93 "-" "curl/7.81.0"
    {"node_name": "ip-172-31-12-246", "status": "ok", "pending": 0, "running": 1, "finished": 0}
    ```
    - We can use cron service to arrange a cron task for running the spider. Or, scrapy web dashboards, e.g. [Scrapeops](https://scrapeops.io/), [ScrapyWeb](https://github.com/my8100/scrapydweb) provides web interface to get server instances, scraping github repository and schedule web scraping task. Note: ScrapyWeb supports python 2.7, 3.6, 3.7, 3.8 and 3.9, according to its GitHub project site.
    ```
    $ pip install --upgrade git+https://github.com/my8100/scrapydweb.git
    ```
    - Process to install selected python in Ubuntu, especially when we need to install a version not in the standard repository associated with the AMI selected.
    ```
    $ sudo apt update
    $ sudo apt install software-properties-common
    $ sudo add-apt-repository ppa:deadsnakes/ppa
    $ sudo apt update
    $ sudo apt install python3.x
    ```
    - After installing multiple Python version in the system, use the following commands to select the target python version when starting the virtual environment
    ```
    $ virtualenv -p /usr/bin/python3.x venv3x
    ```
    - Encountered ModuleNotFoundError: No module named 'distutils.cmd' and resolved this issue by installing the version specific distutils using the following command. After doing this, 'pip install -r requirements.txt' could be successfully executed
    ```
    $ sudo apt install python3.9-distutils
    ```
    - Start scrapydweb simply using the command. Note: scrapyd is using port 6800 to accept json queries and scrapydweb is using port 5000 to receive requests. We may use the command 'ss' (socket statistics) to check the port listening status with -l option added. Note that scrapydweb_settings_v10.py contains many configurable parameters controlling the execution of scrapydweb, such as SCHEDULE_ADDITIONAL controls spider timeout, spider page count... LOCAL_SCRAPYD_LOGS_DIR and ENABLE_LOGPARSER to enable corporation between Scrapyd and ScrapydWeb.  And ENABLE_AUTH, USERNAME, PASSWORD to enable authentication to access ScrapydWeb
    ```
    $ scrapydweb
    %% Use ss command to check the daemon running status
    $ sudo ss -tunlp
    Netid   State    Recv-Q    Send-Q            Local Address:Port       Peer Address:Port   Process
    udp     UNCONN   0         0                 127.0.0.53%lo:53              0.0.0.0:*       users:(("systemd-resolve",pid=305,fd=13))
    udp     UNCONN   0         0            172.31.12.246%eth0:68              0.0.0.0:*       users:(("systemd-network",pid=303,fd=15))
    udp     UNCONN   0         0                     127.0.0.1:323             0.0.0.0:*       users:(("chronyd",pid=409,fd=5))
    udp     UNCONN   0         0                         [::1]:323                [::]:*       users:(("chronyd",pid=409,fd=6))
    tcp     LISTEN   0         128                     0.0.0.0:5000            0.0.0.0:*       users:(("scrapydweb",pid=1856,fd=5))
    tcp     LISTEN   0         4096              127.0.0.53%lo:53              0.0.0.0:*       users:(("systemd-resolve",pid=305,fd=14))
    tcp     LISTEN   0         50                    127.0.0.1:6800            0.0.0.0:*       users:(("scrapyd",pid=1834,fd=6))
    tcp     LISTEN   0         128                     0.0.0.0:22              0.0.0.0:*       users:(("sshd",pid=548,fd=3))
    tcp     LISTEN   0         128                        [::]:22                 [::]:*       users:(("sshd",pid=548,fd=4))
    ```
- 2023/12/25~2023/12/31
  - Continued to experiment access the Scrapyd daemon running on an AWS EC2 Ubuntu instance. (Successfully connected to scrapyd from remote)
    1. Adjust security settings of AWS EC2 instance to allow inbound connection to port 6800
    2. Bind scrapyd host IP in default_scrapyd.conf in the scrapyd installation. To be specific, change bind_address from 127.0.0.1 to 0.0.0.0
          
            

    
  
