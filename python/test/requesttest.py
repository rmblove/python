#----python3.5----
# -*- codeing = 'utf-8' -*-
# request add_headers test
from urllib import request as rq
import gzip

head = {'Host':'www.2345.com',
		'Connection':'keep-alive',
		'Cache-Control':'max-age=0',
		'Accept': 'text/html, */*; q=0.01',
		'X-Requested-With': 'XMLHttpRequest',
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36',
		'DNT':'1',
		'Referer': 'http://tools.2345.com/rili.htm',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'zh-CN,zh;q=0.8,ja;q=0.6'
		}

url = rq.Request('http://www.2345.com',headers = head)
#url.add_header(head)
x = rq.urlopen(url)
a = gzip.decompress(x.read())
try:
    c = a.decode('utf-8')
except Exception as e:
    print(e)
    c = a.decode('gb2312')
print(c)