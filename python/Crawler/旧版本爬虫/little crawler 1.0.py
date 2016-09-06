#----python3.5----
# -*- codeing = 'utf-8' -*-
# version = 1.0
# 一个很小的爬虫
import urllib.request
import queue
import time
import re
from lxml import etree 
url_que = queue.Queue()
url_host = ['http://www.bttiantang.com']
seen_list = dict()

def get_url():
    while(True):
        if  not url_que.empty():   
            url = url_que.get()
            HTML = urllib.request.urlopen(url).read().decode('utf-8')
            print(HTML)
            filter_url(HTML)
        else:
            time.sleep(1)
            break

def filter_url(html):
#    <a href="/subject/25524.html" target="_blank">龙虎少年队2.2014</a>
    html_parse = etree.HTML(html)
    find = etree.XPath("//a[@href]")
    node_list = find(html_parse)
    for node in node_list:
        try:
            path_str = node.attrib['href']
            movie_name = node.text
        except Exception as e:
            continue
        if path_str not in seen_list and movie_name is not None:
            seen_list[path_str] = movie_name
            if re.match('http',path_str):
                url_que.put(path_str)
            else:
                url_que.put(url_host[0]+path_str)
            
if __name__ == '__main__':
    url_que.put(url_host[0])
    url = url_que.get()
    HTML = urllib.request.urlopen(url, timeout = 3).read().decode('utf-8')
    print(HTML)
    filter_url(HTML)   
    print(seen_list)
while not url_que.empty():
    print(url_que.get())
