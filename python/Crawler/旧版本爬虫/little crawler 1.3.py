#----python3.5----
# -*- codeing = 'utf-8' -*-
# version = 1.3
# 一个很小的爬虫
import urllib.request
import queue
import time
import re
from lxml import etree 
from threading import Thread
from multiprocessing.dummy import Pool

urls_que = queue.Queue()
tree_que = queue.Queue()
url_host = ['http://www.bttiantang.com']
seen_list = dict()
seen_page = dict()

def get_htmls():
    wait_time = 0
    while(True):
        if not urls_que.empty():   
            urls = urls_que.get()
            pool = Pool(4)
            pool.map(work_on_html,urls)
            pool.close()
            pool.join()
            print('thread1:working')
            wait_time = 0
        else:
            time.sleep(1)
            print('thread1:--------sleeping')
            wait_time += 1
        if wait_time == 10:
            break

def work_on_html(url):
    try:
        HTML = urllib.request.urlopen(url, timeout = 3)
#        time.sleep(0.1)
        html = HTML.read().decode('utf-8')
        html_parse = etree.HTML(html)
        HTML.close()
        find = etree.XPath("//a[@href]")
        node_list = find(html_parse)
        tree_que.put(node_list)
    except Exception as e:
        pass

def get_urls():
    wait_time = 0
    while(True):
        if not tree_que.empty():
            node_list = tree_que.get()
            pool = Pool(8)
            urls = pool.map(work_on_nodelist, node_list[::-1]) 
            pool.close()
            pool.join()
            urls = list(set(urls))
            urls_que.put(urls) 
            print('thread2:working')    
            wait_time = 0
        else:
            time.sleep(1)
            print('thread2:---------sleeping')
            wait_time += 1
        if wait_time == 10:
            break

def work_on_nodelist(node):
    try:
        path_str = node.attrib['href']
        movie_name = node.text
        if re.search('/?PageNo', path_str):
            if path_str not in seen_page:
                seen_page[path_str] = movie_name
                print(path_str)
                return (url_host[0]+path_str) 
        if re.match('/subject/', path_str) and movie_name is not None:
            if path_str not in seen_list:
                seen_list[path_str] = movie_name
    except Exception as e:
        print(e)        

            
if __name__ == '__main__':
    urls_que.put(url_host)
    func_list = [get_htmls, get_urls]
    threads = []
    for func in func_list:
        threads.append(Thread(target = func))
    for thread in threads:
        thread.setDaemon(True)
        thread.start()
        time.sleep(1)
    for thread in threads:
        thread.join()
    time.sleep(1)
    seen_list = sorted(seen_list.items(),key=lambda d:d[0])
    seen_page = sorted(seen_page.items(),key=lambda d:d[0])
    time.sleep(1)
    print(seen_list)
    print(len(seen_list))

