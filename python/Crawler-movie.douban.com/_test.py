#for test

from clopener import CrawlerRequest, findurls, urlcheck

from time import sleep
from lxml import etree
from multiprocessing.dummy import Pool
from functools import wraps
from threading import Thread
from io import StringIO, BytesIO
from queue import Queue
from copy import deepcopy
from urllib.parse import quote  # solve urlopen can not open url that contains Chinese.
import pprint
import time
import re
import random

random.seed(5)
url_todo = Queue()
opener = CrawlerRequest()
seed = ["https://movie.douban.com/tag/动作"]



def cleanurl(url):
    copyurl = deepcopy(url)
#     if not copyurl.endswith("/"):
#         copyurl = copyurl + "/"
    urlspli = copyurl.split("/")
    if urlspli[-2].isdigit():
        return "/".join(urlspli[0:-1]) + "/"
    else:
        return copyurl
    

def parsedouban(html, Notused):
    info = {}
    parser = etree.HTMLParser()
    if isinstance(html, str):
        root = etree.parse(StringIO(html), parser)
    elif isinstance(html, bytes):
        root = etree.parse(BytesIO(html), parser)
    else:
        return None
    content = root.find(".//div[@id='content']")
    if content == None: return
    name = content.find(".//span[@property='v:itemreviewed']")
    if name == None: return
    info["name"] = name.text
    year = name.getnext()
    if year == None: return
    info["year"] = year.text
    rate = content.find(".//strong[@class='ll rating_num']")
    if rate == None: return
    info["rate"] = rate.text
    rate_count = content.find(".//span[@property='v:votes']")
    if rate_count == None: return
    info["rate_count"] = rate_count.text
    pprint.pprint(info)



if __name__ == '__main__':
    print("---- Test Start ----\n")
    
    url_todo.put(seed)
    urls = []
    douban = (parsedouban, None)
    
    while(True):
        for url in urls:
            sleep(0.5)
            print(url)
            url = quote(url, safe="/:?=&?", encoding='utf-8')
            web = opener.open_url_with_callback(url, douban)
            if web is not None:
                url_list = findurls(web, domain = "https://movie.douban.com", cleaner = cleanurl)
                if len(url_list) >= 1:
                    url_todo.put(url_list)
        urls = url_todo.get(block=False)
        if(urls == None or len(urls) == 0): break
        random.shuffle(urls)
        #pprint.pprint(urls)
    
    print("---- Test End ----\n\n")

    