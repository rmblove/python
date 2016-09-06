#----python3.5----
# -*- codeing = 'utf-8' -*-
# version = 2.0
# 一个很小的爬虫with MySQL
#https://www.python.org/dev/peps/pep-0249/      pymysql
#http://lxml.de                                 lxml
import urllib.request
import queue
import time
import re
import pymysql
from lxml import etree 
from threading import Thread
from multiprocessing.dummy import Pool

urls_que = queue.Queue()
tree_que = queue.Queue()
url_host = ['http://www.bttiantang.com']
seen_list = dict()
seen_page = dict()
pymysql.threadsafety = 0 #Threads may not share the module.

def search_inDB(url):
    try:
        conn = pymysql.connect(host='localhost', user='python', password='123456', db='bttiantang.com', charset='utf8mb4')
        with conn.cursor() as cur:
            sql = ("SELECT url FROM urls WHERE url = %s;")
            result = cur.execute(sql, (url))
            if result == 1:
                return(True)
            else:
                return(False)
    except Exception as e:
        print('error in searching on Database')
        print(e)
    finally:
        conn.close()

def insert_inDB(list):
    try:
        conn = pymysql.connect(host='localhost', user='python', password='123456', db='bttiantang.com', charset='utf8mb4')
        with conn.cursor() as cur:
            sql = ("INSERT INTO urls (url, movie) VALUES (%s, %s);")
            result = cur.execute(sql, (list[0], list[1]))
            print('inserting compelete')
        conn.commit()
    except Exception as e:
        print('error in inserting on Database')
        print(e)
    finally:
        conn.close()

def delete_inDB(str):
    try:
        with conn.cursor() as cur:
            sql = ("DELETE FROM urls WHERE url = %s;")
            cur.execute(sql, (str))
        conn.commit()
    except Exception as e:
        print('error in deleting on Database')
        print(e)
    finally:
        conn.close()

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
            pool = Pool(4)
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
            if not search_inDB(path_str):
                insert_inDB([path_str, movie_name])
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
    seen_page = sorted(seen_page.items(),key=lambda d:d[0])
    time.sleep(1)
    conn = pymysql.connect(host='localhost', user='python', password='123456', db='bttiantang.com', charset='utf8mb4')
    cur = conn.cursor()
    all_urls = cur.execute("SELECT * FROM urls")
    print(all_urls)
    for row in all_urls:
        print(row)
    cur.close()
    conn.close()

