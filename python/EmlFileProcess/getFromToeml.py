#!/usr/local/bin/python3
# -*- coding = 'utf-8' -*-
# This is date(from to) process for eml file.
import os
from timelinebar import Timelinebar
from email.parser import Parser
import collections

class emailProcess:
    '''haha'''
    cdir = ""
    file_num = 0
    file_db = []
    msg_db = collections.defaultdict(int)
    def __init__(self,dir):
        if os.path.exists(dir):
            self.cdir, _, self.file_db = [_ for _ in os.walk(dir)][0]
            self.file_num = len(self.file_db)
            print("---loading directory successful---")
        else:
            print("cannot open this directory or the directory is not exist \n ")
            raise IOError

    def getEmailMesssage(self, emlfiledir):
        try:
            with open(emlfiledir, 'r') as fp:
                p = Parser()
                msg = p.parse(fp)
                return (msg["From"], msg["To"])
        except Exception as e:
            raise e
            print("logging getEmailMesssage error : " + emlfiledir + "\n")

    def process(self,  amount=0):
        if self.file_num != 0:
            timebar_lenth = self.file_num if amount == 0 else amount
            timebar = Timelinebar(timebar_lenth)
            timebar.setinfo("<email process>")
            for no, eml in enumerate(self.file_db):

                try:
                    From_To_msg = self.getEmailMesssage(os.path.join(self.cdir, eml))
                except Exception as e:
                    continue

                self.msg_db[From_To_msg] += 1
                timebar.flush(no)
                if no == (amount-1): break


if __name__=="__main__":
    ep = emailProcess('/Volumes/Public/Temp Files/eml')
    ep.process()
    haha = ep.msg_db.copy()

    sorted(haha.items(), key = lambda d:d[1], reverse = True)
    print(haha.items())
