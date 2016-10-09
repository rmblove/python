#-*-python3.5-*-
#-*-coding = 'uft-8'-*-
#-*-version = 1.0-*-
#douban.movie.com crawler
from urlopener import get_urls
from lxml import etree
from multiprocessing.dummy import Pool
from threading import Thread
from queue import Queue
import pprint
import time
import re

url_list_que = Queue()
url_filt_que = Queue()
url_down_que = Queue()

seed = ['http://movie.douban.com']

def parsedouban(html):
    info = {}
    root = etree.HTML(html)
    content = root.find(".//div[@id='content']")
    if content == None: return
    name = content.find(".//span[@property='v:itemreviewed']")
    info["name"] = name.text
    year = name.getnext()
    info["year"] = year.text
    rate = content.find(".//strong[@class='ll rating_num']")
    info["rate"] = rate.text
    rate_count = content.find(".//span[@property='v:votes']")
    info["rate_count"] = rate_count.text
    pprint.pprint(info)

if __name__ == '__main__':
'''
    url_list_que.put(seed)
    func_list = [urlopenning, urlfiltting, urldownloading]
    threads = []
    for func in func_list:
        threads.append(Thread(target = func))
    for thread in threads:
        thread.setDaemon(True)
        thread.start()
        time.sleep(1)
    for thread in threads:
        thread.join()
'''        
