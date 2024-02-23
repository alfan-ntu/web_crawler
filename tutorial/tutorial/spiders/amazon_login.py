"""
    Description: This is a sample code demonstrating dual stage login process handling using scrapy_splash
    Date: 2024/2/19
    Author:
    Version: 0.1a
    Revision History:
        - 2024/2/19: v. 0.1a the initial version
    Reference:
            1) https://www.youtube.com/watch?v=VySakHZi6HI
            2) https://scrapeops.io/python-scrapy-playbook/scrapy-login-form/
    Notes:
        1) Skipped this operation for complexity consideration

    ToDo's  :
        -
"""
import scrapy
from scrapy_splash import SplashRequest

# A splash script to automatically walk through the two-stage login process of
# amazon.com
lua_script = """
function main(splash, args)
    splash:init_cookies(splash.args.cookies)

    assert(splash:go(args.url))
    assert(splash:wait(1))

    splash:set_viewport_full()

    local email_input = splash:select('input[name=email]')   
    email_input:send_text("maoyi_fan@yahoo.com.tw")
    assert(splash:wait(1))

    local email_submit = splash:select('input[id=continue]')
    email_submit:click()
    assert(splash:wait(3))

    local password_input = splash:select('input[name=password]')   
    password_input:send_text("xxxxxxxx")
    assert(splash:wait(1))

    local password_submit = splash:select('input[id=signInSubmit]')
    password_submit:click()
    assert(splash:wait(3))

    return {
        html=splash:html(),
        url = splash:url(),
        cookies = splash:get_cookies(),
        }
    end
"""

class AmazonLoginSpider(scrapy.Spider):
    name = "amazon_login"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["https://www.amazon.com"]

    def start_requests(self):
        signin_url="https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"
        yield SplashRequest(
            url=signin_url,
            callback=self.start_scraping,
            endpoint='execute',
            args={
                'width': 1000,
                'lua_source': lua_script,
                'ua': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
            }
        )

    def start_scraping(self, response):
        pass

    def parse(self, response):
        pass
