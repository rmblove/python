from SETTING import config as cfg
import sys
import os
import time

class simplelog:

    def __init__(self, msg=None):
        self.fp = open(cfg["LOG_PATH"], "a")
        sys.stderr = self.fp
        if not msg:
            self.write(msg)

    def __del__(self):
        self.fp = sys.stderr
        self.close()

    def write(self, msg):
        log = time.ctime() + msg + "\n"
        self.fp.writelines(log)

    def close(self):
        self.fp = sys.stderr
        self.fp.close()
