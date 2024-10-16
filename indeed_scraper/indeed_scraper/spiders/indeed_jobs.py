"""
    Description: This is the spider part of a scraper crawling and scraping posted jobs on Indeed.com
    Date: 2024/10/4
    Author: maoyi.fan@yapro.com.tw
    Version: 0.1a
    Revision History:
        - 2024/10/4: v. 0.1a the initial version
    Reference:
            1) Reference tutorial: https://scrapeops.io/python-scrapy-playbook/python-scrapy-indeed-scraper/
            2) Reference YouTube video: https://www.youtube.com/watch?v=_8uxMS0anqQ

    Notes:
            1) This file was created using template 'basic' by executing the command
               $ scrapy genspider indeed_jobs https://www.indeed.com
            2) Job records are stored in "mosaic-provider-jobcards" JSON records in <script id="mosaic-data" type="text/javascript">
            3) Crawling gets blocked; Resolved through using ScrapeOps' scrapy-proxy-sdk
               (https://scrapeops.io/python-scrapy-playbook/python-scrapy-indeed-scraper/)

    ToDo's  :
        - Allow user to input information of location, usage, area size to compose flexible
          request URLs
"""
import scrapy
import re
import json
from urllib.parse import urlencode
import logging
from scrapy.utils.log import configure_logging


class IndeedJobsSpider(scrapy.Spider):
    name = "indeed_jobs"
    # Use proxy service provided by scrapeops.io
    # proxy_server = 'http://scrapeops:2bb9eaa3-b008-48df-98fa-6b175af37535@proxy.scrapeops.io:5353'
    proxy_server = 'http://43.134.121.40:3128'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }
    # customizing log output
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='indeed_jobs.log',
        format='%(levelname)s: %(message)s',
        level=logging.INFO,
        # filemode="w"
    )
    allowed_domains = ["www.indeed.com", "proxy.scrapeops.io"]

    #
    # compose request URL based on the job keyword, location and offset
    #
    def get_indeed_search_url(self, keyword, location, offset=0):
        parameters = {"q": keyword, "l": location, "filter": 0, "start": offset}
        return "https://www.indeed.com/jobs?" + urlencode(parameters)

    #
    # Description: start_requests() generates the initial requests the spider will execute.
    #
    def start_requests(self):
        keyword_list = ['python']
        location_list = ['Taipei']
        for keyword in keyword_list:
            for location in location_list:
                indeed_jobs_url = self.get_indeed_search_url(keyword, location)
                self.logger.info(f'Indeed jobs search url: {indeed_jobs_url}')
                yield scrapy.Request(url=indeed_jobs_url,
                                     callback=self.parse_search_results,
                                     headers=self.headers,
                                     meta={'keyword': keyword,
                                           'location': location,
                                           'offset': 0,
                                           # 'proxy': self.proxy_server,
                                           })

    #
    # compose job URL based on the job keyword, location and jobkey
    #
    def get_indeed_job_url(self, keyword, location, jobkey):
        parameters = {"q": keyword, "l": location, "filter": 0, "vjk": jobkey}
        return "https://www.indeed.com/jobs?" + urlencode(parameters)

    #
    # Description: parses results from indeed.com
    #              response.meta carries the metadata included in the meta dictionary packed in scrapy.Request
    #
    def parse_search_results(self, response):
        # check if anything replied from the host
        self.logger.info('Received response from %s', response.url)
        # self.logger.info('Request sent via %s', response.request.meta['proxy'])
        self.logger.info('Response received %s', response.body.decode("utf-8"))

        location = response.meta['location']
        keyword = response.meta['keyword']
        offset = response.meta['offset']
        script_tag = re.findall(r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});', response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
            #
            # Extract Jobs From Search Page
            #
            jobs_list = json_blob['metaData']['mosaicProviderJobCardsModel']['results']
            for index, job in enumerate(jobs_list):
                if job.get('jobkey') is not None:
                    # job_url = 'https://www.indeed.com/m/basecamp/viewjob?viewtype=embedded&jk=' + job.get('jobkey')
                    job_url = self.get_indeed_job_url(keyword, location, job.get('jobkey'))
                    self.logger.info(f'Indeed jobcard url: {job_url}')
                    yield scrapy.Request(url=job_url,
                                         callback=self.parse_job,
                                         headers=self.headers,
                                         meta={
                                             'keyword': keyword,
                                             'location': location,
                                             'page': round(offset / 10) + 1 if offset > 0 else 1,
                                             'position': index,
                                             'jobKey': job.get('jobkey'),
                                             # 'proxy': self.proxy_server,
                                         })
            #
            # Paginate Through Jobs Pages
            #
            # if offset == 0:
            #     meta_data = json_blob["metaData"]["mosaicProviderJobCardsModel"]["tierSummaries"]
            #     num_results = sum(category["jobCount"] for category in meta_data)
            #     if num_results > 1000:
            #         num_results = 50
            #
            #     for offset in range(10, num_results + 10, 10):
            #         url = self.get_indeed_search_url(keyword, location, offset)
            #         yield scrapy.Request(url=url,
            #                              callback=self.parse_search_results,
            #                              headers=self.headers,
            #                              meta={'keyword': keyword,
            #                                    'location': location,
            #                                    'offset': offset,
            #                                    'proxy': self.proxy_server,
            #                                    })

    def parse_job(self, response):
        location = response.meta['location']
        keyword = response.meta['keyword']
        page = response.meta['page']
        position = response.meta['position']
        script_tag  = re.findall(r"_initialData=(\{.+?\});", response.text)
        if script_tag is not None:
            json_blob = json.loads(script_tag[0])
            # autoOpenTwoPaneViewjobResponse.body.jobInfoWrapperModel.jobInfoModel.sanitizedJobDescription
            job = json_blob["jobInfoWrapperModel"]["jobInfoModel"]['jobInfoHeaderModel']
            sanitizedJobDescription= json_blob["jobInfoWrapperModel"]["jobInfoModel"]['sanitizedJobDescription']
            yield {
                'keyword': keyword,
                'location': location,
                'page': page,
                'position': position,
                'company': job.get('companyName'),
                'jobkey': response.meta['jobKey'],
                'jobTitle': job.get('jobTitle'),
                'jobDescription': sanitizedJobDescription,
            }