# python3.5
# -*- coding = 'utf-8' -*-
# 解析url并将相关数据存入mysql
import re
import pymysql
from lxml import etree
from urlopener import urlprocess

def findName(nodes):
    find = etree.XPath("//span[@property='v:itemreviewed']")
    name = find(nodes)
    return name[0].text

def findScore(nodes):
    find = etree.XPath("//strong[@class='ll rating_num']")
    score = find(nodes)
    return score[0].text

def findEvaluNum(nodes):
    find = etree.XPath("//span[@property='v:votes']")
    EvaluNum = find(nodes)
    return EvaluNum[0].text

def findinfo(url):
    html = urlprocess(url)
    nodes = etree.HTML(html)
    try:
        name = findName(nodes)
    except Exception as e:
        name = 'Null'
    try:
        score = float(findScore(nodes))
    except Exception as e:
        score = 'Null'
    try:
        evalunum = findEvaluNum(nodes)
    except Exception as e:
        evalunum = 'Null'
    return[url, name, score, evalunum]

def saveinsql(list):
    try:
        conn = pymysql.connect(host='localhost', user='python', password='123456', db='bttiantang.com', charset='utf8mb4')
        with conn.cursor() as cur:
            sql = ("INSERT INTO doubanmovie (url, movie, score, evalumum, updateday) VALUES (%s, %s, %f, %s, CURRENT_DATE);")
            result = cur.execute(sql, (list[0], list[1], list[2], list[3]))
            conn.commit()
    except Exception as e:
        conn.close()
        print('Error in saving on Database')
        print(e)
    finally:
        conn.close()

def Download(url):
    list = findinfo(url)
    if list[1] == 'Null':
        return
    print(list)
#saveinsql(list)
    print('saving complete')

