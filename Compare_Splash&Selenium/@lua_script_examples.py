lua_script_example0 = """
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
"""

lua_script_example1 = '''
function main(splash, args)
  splash:go(args.url)
  getTest = splash:jsfunc([[
    function() {
        ret_val = document.getElementsByClassName('apphub_NoMoreContent')
        return ret_val[0].getAttribute('style')
    }
  ]])
  scrollScreen = splash:jsfunc([[
    function() {
        window.scrollBy(0, 2*window.innerHeight)
    }
  ]])
  while (getTest() == 'display: none') do
    scrollScreen()
    splash:wait(1)
  end
  return splash:html()
end'''

lua_script_example2 = '''
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  splash.images_enabled = false
  check_for_age = splash:runjs([[
    if (document.getElementById("ageYear") != null) {
      btn = document.getElementsByClassName("btnv6_blue_hoverfade btn_medium")
      document.getElementById("ageYear").value = 1982
      btn[0].click()
    }
    ]])
    splash:wait(3)
  return splash:html()
end
'''


lua_script_example3 = """
function main(splash)
    local num_scrolls = 10
    local scroll_delay = 1.0
    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)
    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end
    return splash:html()
end
"""

lua_script_example4 = """
function main(splash)
    local url = splash.args.url
    assert(splash:go(url))
    assert(splash:wait(0.5))
    assert(splash:runjs("$('.next')[0].click();"))
    return {
        html = splash:html(),
        url = splash:url(),
    }
end
"""

lua_script_example5 = """
function main(splash)
    assert(splash:go(splash.args.url))
    splash:wait(0.5)
    local title = splash:evaljs("document.title")
    return {title=title}
end
"""

# Using the js_source Parameter
"""
yield SplashRequest(
    'http://example.com',
    self.test,
    endpoint='render.html',
    args={
        'js_source': 'document.title="My Title";'
    },
)
"""


