# /*******************************************************************************************************/ #
import scrapy
from scrapy_splash import SplashRequest

class MySpider(scrapy.Spider):
    start_urls = ["http://example.com", "http://example.com/foo"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        # response.body is a result of render.html call; it
        # contains HTML processed by a browser.
        # ...

# /*******************************************************************************************************/ #
import json
import base64
import scrapy
from scrapy_splash import SplashRequest

class MySpider(scrapy.Spider):

    # ...
        splash_args = {
            'html': 1,
            'png': 1,
            'width': 600,
            'render_all': 1,
        }
        yield SplashRequest(url, self.parse_result, endpoint='render.json',
                            args=splash_args)

    # ...
    def parse_result(self, response):
        # magic responses are turned ON by default,
        # so the result under 'html' key is available as response.body
        html = response.body

        # you can also query the html result as usual
        title = response.css('title').extract_first()

        # full decoded JSON data is available as response.data:
        png_bytes = base64.b64decode(response.data['png'])

        # ...

# /*******************************************************************************************************/ #
import json
import base64
from scrapy_splash import SplashRequest


class MySpider(scrapy.Spider):

    # ...
        script = """
        function main(splash)
            assert(splash:go(splash.args.url))
            return splash:evaljs("document.title")
        end
        """
        yield SplashRequest(url, self.parse_result, endpoint='execute',
                            args={'lua_source': script})

    # ...
    def parse_result(self, response):
        doc_title = response.body_as_unicode()
        # ...


# /***************************************************************************************************************/ #
import json
import base64
from scrapy_splash import SplashRequest

script = """
-- Arguments:
-- * url - URL to render;
-- * css - CSS selector to render;
-- * pad - screenshot padding size.

-- this function adds padding around region
function pad(r, pad)
  return {r[1]-pad, r[2]-pad, r[3]+pad, r[4]+pad}
end

-- main script
function main(splash)

  -- this function returns element bounding box
  local get_bbox = splash:jsfunc([[
    function(css) {
      var el = document.querySelector(css);
      var r = el.getBoundingClientRect();
      return [r.left, r.top, r.right, r.bottom];
    }
  ]])

  assert(splash:go(splash.args.url))
  assert(splash:wait(0.5))

  -- don't crop image by a viewport
  splash:set_viewport_full()

  local region = pad(get_bbox(splash.args.css), splash.args.pad)
  return splash:png{region=region}
end
"""

class MySpider(scrapy.Spider):

    # ...
        yield SplashRequest(url, self.parse_element_screenshot,
            endpoint='execute',
            args={
                'lua_source': script,
                'pad': 32,
                'css': 'a.title'
            }
         )

    # ...
    def parse_element_screenshot(self, response):
        image_data = response.body  # binary image data in PNG format
        # ...



# /***************************************************************************************************************/ #
import scrapy
from scrapy_splash import SplashRequest

script = """
function main(splash)
  splash:init_cookies(splash.args.cookies)
  assert(splash:go{
    splash.args.url,
    headers=splash.args.headers,
    http_method=splash.args.http_method,
    body=splash.args.body,
    })
  assert(splash:wait(0.5))

  local entries = splash:history()
  local last_response = entries[#entries].response
  return {
    url = splash:url(),
    headers = last_response.headers,
    http_status = last_response.status,
    cookies = splash:get_cookies(),
    html = splash:html(),
  }
end
"""

class MySpider(scrapy.Spider):


    # ...
        yield SplashRequest(url, self.parse_result,
            endpoint='execute',
            cache_args=['lua_source'],
            args={'lua_source': script},
            headers={'X-My-Header': 'value'},
        )

    def parse_result(self, response):
        # here response.body contains result HTML;
        # response.headers are filled with headers from last
        # web page loaded to Splash;
        # cookies from all responses and from JavaScript are collected
        # and put into Set-Cookie response header, so that Scrapy
        # can remember them.        


# /***************************************************************************************************************/ #
import json
import scrapy
from scrapy.http.headers import Headers

RENDER_HTML_URL = "http://127.0.0.1:8050/render.html"

class MySpider(scrapy.Spider):
    start_urls = ["http://example.com", "http://example.com/foo"]

    def start_requests(self):
        for url in self.start_urls:
            body = json.dumps({"url": url, "wait": 0.5}, sort_keys=True)
            headers = Headers({'Content-Type': 'application/json'})
            yield scrapy.Request(RENDER_HTML_URL, self.parse, method="POST",
                                 body=body, headers=headers)

    def parse(self, response):
        # response.body is a result of render.html call; it
        # contains HTML processed by a browser.
        # ...