#for test

from clopener import CrawlerRequest, findurls

from time import sleep
from multiprocessing.dummy import Pool
from threading import Thread
from queue import Queue
import time
import re

url_todo = Queue()
opener = CrawlerRequest()
seed = ['https://www.2345.com']

def memo(func):
    cache = {}
    @wraps(func)
    def warp(*args):
        if args not in cache:
            cache[args] = fun(*args)
        return cache[args]
    return warp





if __name__ == '__main__':
    print("---- Test Start ----\n\n")
    
    url_todo.put(seed)
    urls = seed
    while(urls != None and len(urls)!=0):
        for url in urls:
            web = opener.open_url_with_filter(url)
            sleep(2)
            if web is not None:
                urls = findurls(web, "2345.com")
                if len(urls) >= 1:
                    url_todo.put(urls)
        urls = url_todo.get(block=False)
        
    print("---- Test End ----\n\n")
'''
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
    