# python3.5
# -*- coding = 'utf-8' -*-
# 解析url并将相关数据存入mysql
import re
import pymysql
from lxml import etree


def save2mysql(list):
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

def save2sqlite(list)
    pass


def callback1(html, args):
    pass

def callback2(html, args):
    pass
