#!/usr/local/bin/python3
# -*- coding = 'utf-8' -*-
import networkx as nx
import matplotlib.pyplot as plt
import sqlite3
from SETTING import config as cfg
import re
import pprint
from collections import defaultdict

def loadfromsqlite():
    edges = defaultdict(int)
    edges_tuple_list = []
    conn = sqlite3.connect(cfg["DATABASE_PATH"])
    cur = conn.cursor()
    for row in cur.execute("SELECT * FROM dnc_email_20160811"):
        _0, _1, emailfrom, emailto = row
        if emailto == None : continue
        emailtogroup = re.findall(r"<.*?>", str(emailto))
        if emailtogroup == None: continue
        for everyemailto in emailtogroup:
            edges[(emailfrom, everyemailto)] += 1
    for everykey in edges.keys():
        edges_tuple_list.append((everykey[0], everykey[1], edges[everykey]))
    return edges_tuple_list






if __name__=="__main__":
    samplelist = loadfromsqlite()
    # pprint.pprint(samplelist)
    FG = nx.Graph()
    FG.add_weighted_edges_from(samplelist[:20])
    nx.draw(FG,pos=nx.spring_layout(FG))
    # nx.draw_networkx_labels(FG,pos=nx.spring_layout(FG),node_size=100)
    plt.show()
