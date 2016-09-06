# python3.5
# -*- coding = 'utf-8' -*-
# 定位<a href="/subject/27476.html" target="_blank">血色庄园(港)/腥红山庄(台)/Haunted Peak</a>
import urllib
from urllib import request
from lxml import etree
import re


start_url = ['http://www.bttiantang.com',]
pattern = '/subject/'
haha = dict()

web = urllib.request.urlopen(start_url[0]).read()
webtree = etree.HTML(web)
find = etree.XPath("//a[@href]")
node = find(webtree)
for x in node:
#   b = x.attrib['href']
#   print(b)
    if re.match(pattern, x.attrib['href']):
        if x.text is not None:
            if x.attrib['href'] not in haha:
                url = x.attrib['href']
                txt = x.text
#                print(txt)
                haha[url] = txt
print(haha)