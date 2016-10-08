# python3.5
# -*- coding = 'utf-8' -*-
# when you enter a url , it will return a list of urls;

from urllib import request
from io import StringIO, BytesIO
from http import cookiejar
from functools import wraps
from bloomfilter import BloomFilter
from lxml import etree
import pprint
import gzip
import random
import re

def randheader():
    
    head_connection = ['Keep-Alive','close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5','en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
    header = {
        'Connection':head_connection[1],
        'Accept': head_accept[0],
        'Accept-Charset': 'utf-8;q=0.7,*;q=0.3',
        'Accept-Language':head_accept_language[1],
        'Referer':'https://www.hao123.com',   # When you first use __this__.py change it.
        'Accept-Encoding':'gzip',
        'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6',
        'User-Agent':head_user_agent[random.randrange(0,len(head_user_agent))]
             }
    return header


# Change the ip blow when you use __this__.py first time;
# proxy ip: http://www.cybersyndrome.net/pla.html 
# To get a random proxy to conform request.ProxyHandler(randproxies())
def randproxies():
    ip = ['128.199.119.206:3128',
          '128.199.150.111:3128'
    ]
    proxy = {'http':ip[random.randrange(0,len(ip))]}
    return proxy

# Read 'f' opened by urlopen() or opener.open() with the header information in 'info'.
def readweb(f, info):
    html = None
    content_encoding = info.get('Content-Encoding')
    content_type = info.get('Content-Type')
    if content_encoding == 'gzip':
        html = gzip.decompress(f.read())
    else:
        html = f.read()
    if content_type.lower().find("charset=utf-8") != -1:
        html = html.decode('utf-8')
    return html


# Find and return all urls in html where <a href = "www.google.com" \a>
def findurls(html, contain = None):
    urls = []
    tree = None
    parser = etree.HTMLParser()
    if isinstance(html, str):
        tree = etree.parse(StringIO(html), parser)
    elif isinstance(html, bytes):
        tree = etree.parse(BytesIO(html), parser)
    else:
        return None
    for element in tree.findall(".//a[@href]"):
        url = element.get('href')
        if contain == None:
            urls.append(url)
        elif (url.find(contain)) != -1:
            urls.append(url)
        else: 
            continue
    pprint.pprint(urls)           #test
    return urls


filter = BloomFilter()

def urlseen(func):
    global filter
    @wraps(func)
    def warp(*args):
        if not filter.is_in(args[1]):
            return func(args[0], args[1])
        else:
            return None
    return warp


class CrawlerOpener:
    # A opener with a proxy_handler and a cookie_handler
    def __init__(self):
        self.proxy_handler = request.ProxyHandler(randproxies())
        self._cookie = cookiejar.CookieJar()
        self.cookie_handler = request.HTTPCookieProcessor(self._cookie)
        self.opener = request.build_opener(self.proxy_handler, self.cookie_handler)
                
    def open(self, url):
        return self.opener.open(url)
    
    def close(self):
        self.opener.close()



class CrawlerRequest(CrawlerOpener):
    # Auto adding a random header for openning a url
    def __init__(self):
        super().__init__()
        self.header = randheader()
        self.filter = BloomFilter()
        self.err_count = 0

    def open_url(self, url):
        request.install_opener(self.opener)
        req = request.Request(url, headers = self.header)
        with request.urlopen(req) as f:
            #pprint.pprint(f.info().items()) # print headers comes for server
            return readweb(f, f.info())
    
    @urlseen
    def open_url_with_filter(self, url):
        try:
            return self.open_url(url)
        except Exception as e:
            print(e)
    
    #callbacks should be (func, *args)
    def open_url_with_callback(self, url, *callbacks):
        try:
            html = self.open_url_with_filter(url)
            for func, *args in callbacks:
                func(html, *args)
            return html
        except Exception as e:
            self.err_count += 1
            print(e)
    
    
    def get_urls(self, url):
        return findurls(self.open_url(url))

def callback1(html, a):
    urls = findurls(html, a)

cb = (callback1, "baidu.com")

if __name__ == "__main__":
    cr = CrawlerRequest()
    print("---- Test clopener ----\n")
    html = cr.open_url_with_callback("https://www.hao123.com", cb)
    #print(html)








#Blow are deprecated functions
'''
def urlprocess(url):    
    proxy_support = request.ProxyHandler(randproxies())
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)
    req = request.Request(url, headers = randheader())
    html = request.urlopen(req)
    try:
        html = gzip.decompress(html.read())
    except Exception as e:
        html = html.read()
    try:
        html = html.decode('utf-8')
    except Exception as e:
        html = html.decode('gbk')
    finally:
        return html

def nodeprocess(html):
    url_list = []
    try:
        html = etree.HTML(html)
    except Exception as e:
        print(e)
        return url_list 
    find = etree.XPath("//a[@href]")
    nodes = find(html)
    for node in nodes:
        url = node.attrib['href']
        if re.match('http://movie', url):#域过滤
            url_list.append(url)
    return url_list

def get_urls(url):
    url_list = nodeprocess(urlprocess(url))
    return url_list
'''
