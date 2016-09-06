# python3.5
# -*- coding = 'utf-8' -*-
# 随机headers 打开url 返回一个url的列表
from urllib import request
from urllib.parse import urlparse
import threading
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
from lxml import etree
from time import sleep
import csv
import gzip
import random
import re
import os

def randHeader():
    
    head_connection = ['Keep-Alive','close']
    head_accept = ['text/html, application/xhtml+xml, */*']
    head_accept_language = ['zh-CN,fr-FR;q=0.5','en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']
    header = {
        'Connection':head_connection[1],
        'Accept': head_accept[0],
        'Accept-Charset': 'GBK,utf-8;q=0.7,*;q=0.3',
        'Accept-Language':head_accept_language[1],
        'Referer':'http://www.baidu.com',
        'Accept-Encoding':'gzip',
        'Accept-Language':'zh-CN,zh;q=0.8,ja;q=0.6',
        'User-Agent':head_user_agent[random.randrange(0,len(head_user_agent))]
             }
    return header



def initProxies():
    ip = ['61.234.37.117:1080',
          '95.188.77.233:1080',
    ]
    proxies = {'sock5':ip[random.randrange(0,len(ip))]}
    return proxies

def urlopener(url, proxy=initProxies(), header=randHeader()):
    proxy_support = request.ProxyHandler(proxy)
    opener = request.build_opener(proxy_support)
    request.install_opener(opener)
    req = request.Request(url, headers = header)
    response = request.urlopen(req)
    return response

def readHtml(resp):    
    try:
        html = gzip.decompress(resp.read())
    except Exception as e:
        html = html.read()
    try:
        html = html.decode('utf-8')
    except Exception as e:
        html = html.decode('gbk')
    finally:
        return html

     

def nodeprocess(html):
    url_list = []
    try:
        html = etree.HTML(html)
    except Exception as e:
        print(e)
        return url_list 
    find = etree.XPath("//a[@href]")
    nodes = find(html)
    for node in nodes:
        url = node.attrib['href']
        if re.match('http://movie', url):#域过滤
            url_list.append(url)
    return url_list

    
def saveCSV(row, fileaddr="./temp.csv"):
    csvFile = open(fileaddr, 'a+') 
    try:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    finally:
        csvFile.close()

def getCSV(fileaddr):
    csvFile = open(fileaddr, "r")
    try:
        reader = csv.reader(csvFile)
    finally:
        return reader

def checkIP():
    p = proxiesProvider()
    proxies = p.getProxies()
    checkipurl = "http://1212.ip138.com/ic.asp"
    for proxy in proxies:
        try:
            h = urlopener(checkipurl, proxy={proxy[1]:proxy[2]})
            bsOBJ = BeautifulSoup(h, "lxml")
            ipGEO = bsOBJ.findAll("center")[0].get_text()
            print(proxy + "--------->" + ipGEO)  
        except Exception as e:
            print(e)    

class proxiesProvider():
    def __init__(self, fileaddress="./proxies.csv"):
        
        self.fileaddr = fileaddress
        self.proxies = []
        self.getProxiesfromWeb(["self.page1()"])
        
    def getRandomProxies(self):
        return self.proxies[random.randrange(0, len(self.proxies))]
        
    def getProxies(self):
        return self.proxies
        
    def getProxiesfromWeb(self, pages=[]):
        result = []        
        if not os.path.isfile(self.fileaddr):
            for page in pages:
                rows = eval(page)
                for row in rows:
                    saveCSV(row, self.fileaddr)
                    result.append(row)
            self.proxies = result
        else:
            for proxy in getCSV(self.fileaddr):
                if proxy[2] != "DEAD":
                    result.append(proxy)
            self.proxies = result
    
    def page1(self):
        result = []
        url = "http://www.xicidaili.com/wn/"
        html = readHtml(urlopener(url))
        bsOBJ = BeautifulSoup(html, "lxml")
        proxieslist = bsOBJ.findAll('tr')
        for list in proxieslist[1:]:
            proxy = list.findAll('td')
            result.append(("http", proxy[1].get_text() + ":" + proxy[2].get_text(), "UN_KNOWN"))
        return result

class Crawer():

    def __init__(self, starturl):
        self.proxies = proxiesProvider()
        self.starturl = starturl
        self.host = starturl
        self.pages = set()
        print("Crawler has been initialized.")
        
    def run(self):
        self.getLinksCur(self.starturl)
    
    def getLinks(self, starturl):
        try:
            proxy = self.proxies.getRandomProxies()
            html = readHtml(urlopener(starturl, proxy={proxy[0]:proxy[1]}))
            bsOBJ = BeautifulSoup(html, "lxml")
            for href in bsOBJ.findAll("a", href = re.compile(".*(html|/?PageNo=\d)$")):
                newpage = self.host + href.attrs["href"]
                if newpage not in self.pages:
                    print(newpage)
                    self.pages.add(newpage)
                    self.getLinks(newpage)
        except Exception as e:
            print(e)
    
    def getLinksCur(self, starturl):
        try:
            html = readHtml(urlopener(starturl))
            bsOBJ = BeautifulSoup(html, "lxml")
            for href in bsOBJ.findAll("a", href = re.compile(".*(html|/?PageNo=\d)$")):
                newpage = self.host + href.attrs["href"]
                if newpage not in self.pages:
                    print(newpage)
                    self.pages.add(newpage)
                    urlthread = threading.Thread(target=self.getLinksCur, args=(newpage,))
                    urlthread.start()
                sleep(0.255)
        except Exception as e:
            print(e)
        

      
def main():

    mycrawler = Crawer("http://www.bttiantang.com")
    mycrawler.run()  
    

if __name__ == "__main__":
    main()