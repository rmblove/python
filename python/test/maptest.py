#----python3.5----
# -*- codeing = 'utf-8' -*-
# pool.map-test
from urllib import request
from lxml import etree
import queue
import re
from multiprocessing.dummy import Pool
seen = dict()
seenpage = queue.Queue()
url = 'http://www.bttiantang.com'
def a(node):
    if re.search('/?Page', node.attrib['href']):
        if node.attrib['href'] not in seen:
            seen[node.attrib['href']] = node.text
            seenpage.put(url+node.attrib['href'])
#        return(node.attrib['href'])

web = request.urlopen(url)
html = web.read().decode('utf-8')
HTML = etree.HTML(html)
find = etree.XPath("//a[@href]")
nodelist = find(HTML)
pool = Pool(4)
pool.map(a, nodelist[::-1])
pool.close()
pool.join()
#print(results)
while(not seenpage.empty()):
    print(seenpage.get())
print(seen)

'''
for node in nodelist:
    if re.search('/?Page', node.attrib['href']):
        print(node.attrib['href'])
'''