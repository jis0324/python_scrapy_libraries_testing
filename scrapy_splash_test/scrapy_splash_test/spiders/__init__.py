# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import os
import scrapy
from scrapy.http import Request
from scrapy_splash import SplashRequest

base_dir = os.path.dirname(os.path.abspath(__file__))

class TestSpider(scrapy.Spider):
    name = 'scrapy_splash_test'

    script = """
        function main(splash, args)
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return {
                html = splash:html(),
            }
        end
    """

    def start_requests(self):
        # yield SplashRequest(url = "https://www.bcmitsubishiofsaltillo.com/new-vehicles/", callback = self.parse, endpoint = "execute", args = {
        #     "lua_source": self.script
        # })

        yield SplashRequest(url = "https://www.bcmitsubishiofsaltillo.com/new-vehicles/", callback = self.parse, endpoint='render.html', args={
            'wait': 0.5
        })


    # parse item from response
    def parse(self, response):
        with open("{}/scrapy_splash_test.txt".format(base_dir), "w", encoding="utf-8") as ff:
            ff.write(response.text)
