#----python3.5----
# -*- codeing = 'utf-8' -*-
# 一个很小的爬虫
import urllib.request
import queue
import time
import re
from lxml import etree 
from threading import Thread
from multiprocessing.dummy import Pool

url_que = queue.Queue()
html_que = queue.Queue()
tree_que = queue.Queue()
url_host = ['http://www.bttiantang.com']
seen_list = dict()
seen_page = dict()

def get_html_tree():
    wait_time = 0
    while(True):
        if not url_que.empty():   
            url = url_que.get()
            try:
                HTML = urllib.request.urlopen(url, timeout = 3)
            except Exception as e:
                continue
            time.sleep(0.1)
            html_que.put(HTML)
            print('thread1:working')
            wait_time = 0
        else:
            time.sleep(1)
            print('thread1:sleeping')
            wait_time += 1
        if wait_time == 10:
            break

def get_url_fromhtmlQ():
#    <a href="/subject/25524.html" target="_blank">龙虎少年队2.2014</a>
    wait_time = 0
    while(True):
        if not html_que.empty():
            html_unread = html_que.get()
            try:
                html = html_unread.read().decode('utf-8')
            except Exception as e:
                continue
            html_parse = etree.HTML(html)
            html_unread.close()
            find = etree.XPath("//a[@href]")
            node_list = find(html_parse)
            tree_que.put(node_list)
            print('thread2:working')
            wait_time = 0
        else:
            time.sleep(1)
            print('thread2:sleeping')
            wait_time += 1
        if wait_time == 10:
            break

def work_on_tree():
    wait_time = 0
    while(True):
        if not tree_que.empty():
            node_list = tree_que.get()
            pool = Pool(4)
            results = pool.map(work_on_nodelist, node_list[::-1]) 
            pool.close()
            pool.join() 
            print('thread3:working')    
            wait_time = 0
        else:
            time.sleep(1)
            print('thread3:sleeping')
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
                url_que.put(url_host[0]+path_str)
#               pass
        if re.match('/subject/', path_str) and movie_name is not None:
            if path_str not in seen_list:
                seen_list[path_str] = movie_name
#                url_que.put(url_host[0]+path_str)
    except Exception as e:
        print(e)        

            
if __name__ == '__main__':
    url_que.put(url_host[0])
    func_list = [get_html_tree, get_url_fromhtmlQ, work_on_tree]
    threads = []
    for func in func_list:
        threads.append(Thread(target = func))
    for thread in threads:
        thread.setDaemon(True)
        thread.start()
        time.sleep(1)
    for thread in threads:
        thread.join()
    time.sleep(60)
    seen_list = sorted(seen_list.items(),key=lambda d:d[0])
    seen_page = sorted(seen_page.items(),key=lambda d:d[0])
    print(seen_list)
    print(seen_page)

