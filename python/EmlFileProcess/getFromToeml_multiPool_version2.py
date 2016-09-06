#!/usr/local/bin/python3
# -*- coding = 'utf-8' -*-
# This is date(from to) process for eml file.
import os
import re
import pickle
from multiprocessing import Pool
from multiprocessing import Queue
from multiprocessing import Process
from time import sleep, time
from email.parser import Parser
from functools import partial
import collections

from SETTING import config as cfg
from timelinebar import Timelinebar
from simpleLog import simplelog
from simplesqlite import simpleSqlite

class emailProcess:

    '''haha'''
    eml_path = ""
    file_num = 0
    file_list = []
    msg_dict = collections.defaultdict(int)
    eml_log = simplelog("Dnc Email Process")
    q = Queue()
    def __init__(self, dir):
        self.initial(dir)
        print("---loading directory successful---")
        os.chdir(dir)

    def initial(self, dir):
        if os.path.isfile(cfg["CACHE_PATH"]):
            with open(cfg["CACHE_PATH"], 'rb') as fp:
                self.file_list = pickle.load(fp)
                self.file_num = len(self.file_list)
                self.eml_path = dir
        elif os.path.exists(dir):
            self.eml_path, _, self.file_list = [_ for _ in os.walk(dir)][0]
            self.file_num = len(self.file_list)
            with open(cfg["CACHE_PATH"], 'wb') as fp:
                pickle.dump(self.file_list, fp)
        else:
            print("cannot open this directory or the directory is not exist \n ")
            raise IOError

    def getEmailMesssage(self, emlpath):
        try:
            with open(emlpath, 'r') as fp:
                p = Parser()
                mime = p.parse(fp, headersonly=True)
                mime["EmailPath"] = emlpath
                return mime

        except Exception as e:
            raise e
            # return(" !!! ERROR !!! from : " + emlpath)



    def process(self,  amount_to_process = 0):
        lenth = self.file_num if amount_to_process == 0 else amount_to_process
        file_list = self.file_list[:lenth]
        if lenth==0: return
        simplebar_handle = Timelinebar(lenth) # initialize progress bar with length of work and its name
        simplebar_handle.setinfo(self.eml_path)
        simplesql_handle = simpleSqlite()
        simpsql_process = Process(target=partial(simplesql_handle.run_withcallback,callback=simplebar_handle), args=(self.q,))
        simpsql_process.start()
        ep_callback = partial(self.ep_callback, handle=None)
        ep_error_callback = partial(self.ep_error_callback, handle=None)
        p = Pool(16)
        for file in file_list:
            p.apply_async(self.getEmailMesssage,
                          args = (file,),
                          callback = ep_callback,
                          error_callback = ep_error_callback
                        )
        p.close()
        p.join()
        simpsql_process.join()
        print("\n-----email process is done------\n")

    def ep_callback(self, msg, handle):
        self.q.put(msg)

    def ep_error_callback(self, error, handle):
        self.q.put(str(error))


if __name__=="__main__":
    test = emailProcess('/Volumes/Public/Temp Files/eml/')
    # print(test.file_list)
    start = time()
    test.process()
    end = time()
    print("it takes :\n")
    print(start - end)
    print("\n\n"
        "-----   test is end   ------"
        "\n\n")
