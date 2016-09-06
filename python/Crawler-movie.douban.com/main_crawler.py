#-*-python3.5-*-
#-*-coding = 'uft-8'-*-
#-*-version = 1.0-*-
#douban.movie.com crawler
from urlopener import get_urls
from bloomfilter import Filter
from downloader import Download
from urllib import parse
from multiprocessing.dummy import Pool
from threading import Thread
from queue import Queue
import time
import re

url_list_que = Queue()
url_filt_que = Queue()
url_down_que = Queue()
filter = Filter()
seen = []
seed = ['http://movie.douban.com']

def urls_getting(url):
    url_list = get_urls(url)
    url_filt_que.put(url_list)

def urlopenning():
    while(True):
        list = url_list_que.get()
        if len(list) == 0:
            continue
        pool = Pool(4)
        pool.map(urls_getting, list)
        pool.close()
        pool.join()
        print('threading1 is working')

def urlfiltting():
    while(True):
        list = url_filt_que.get()
        if len(list) == 0:
            continue
        url_list = []
        url_down = []
        for url in list:
            if not filter.is_in(url):
                url_list.append(url)
                part = parse.urlparse(url)
                if re.match(r'^/subject/\d+/$', part.path):# and part.query == '':
                    url_down.append(url)
                print(url)
        url_list_que.put(url_list)
        url_down_que.put(url_down)
        print('threading2 is working -----')

def urldownloading():
    while(True):
        list = url_down_que.get()
        if len(list) == 0:
            continue
        pool = Pool(4)
        pool.map(Download, list)
        pool.close()
        pool.join()
        print('threading3 is working******')

if __name__ == '__main__':
#    print(get_urls('http://www.bttiantang.com'))
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
        
