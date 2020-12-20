# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
# -*- coding: utf-8 -*-

import os
import scrapy
from scrapy.http import Request

base_dir = os.path.dirname(os.path.abspath(__file__))

class TestSpider(scrapy.Spider):
    name = 'scrapy_test'
    start_urls = ["https://www.bcmitsubishiofsaltillo.com/new-vehicles/"]

    # parse item from response
    def parse(self, response):
        print(response)
        with open("{}/scrapy_test.txt".format(base_dir), "w", encoding="utf-8") as ff:
            ff.write(response.text)
