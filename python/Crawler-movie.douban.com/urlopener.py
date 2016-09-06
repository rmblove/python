# python3.5
# -*- coding = 'utf-8' -*-
# 随机headers 打开url 返回一个url的列表
from urllib import request
from urllib.parse import urlparse
from multiprocessing.dummy import Pool
from lxml import etree
import gzip
import random
import re

def randHeader():
    
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
        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
        'Accept-Language':head_accept_language[1],
        'Referer':'http://movie.douban.com/tag',
        'Accept-Encoding':'gzip',
        'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6',
        'User-Agent':head_user_agent[random.randrange(0,len(head_user_agent))]
             }
    return header



def randproxies():
    ip = ['61.38.252.17:3128',
          '158.199.140.91:3128',
          '136.0.16.217:7808',
          '49.212.149.221:8080',
          '203.195.162.96:8080',
          '71.19.154.122:8080',
          '117.177.243.42:8080',
          '117.135.250.138:8080',
          '61.38.252.17:3128',
          '117.135.250.133:80'
    ]
    proxies = {'sock5':ip[random.randrange(0,len(ip))]}
    return proxies

def urlprocess(url):    
    proxy_support = request.ProxyHandler(randproxies())
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)
    req = request.Request(url, headers = randHeader())
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

