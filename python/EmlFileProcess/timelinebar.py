#!/usr/local/bin/python3
# -*- coding = 'utf-8' -*-
# This is time line;
import sys
import os
import curses
from time import sleep

class Timelinebar:
    progress_bar_lenth = 25 # progress bar progress_bar_lenth******-------
    info = ""
    info_lenth = 0
    count = 0
    console_col, console_lin = os.get_terminal_size()
    def __init__(self, totlecount):
        self.totlecount = totlecount
    def setinfo(self, info):
        self.info = "  " + info
        self.info_lenth = len(self.info)

    def flush(self, count, padding=''):
        rate = count/self.totlecount
        print('\r' + ' '*self.console_col + '\r', end='', flush=True)
        print('\r'
               + '*'*int(rate*self.progress_bar_lenth)
               + '-'*(self.progress_bar_lenth - int(rate*self.progress_bar_lenth))
               + str(int(rate*100))
               + '%'
               + self.info
               + padding
               + '\r'
               , end=''
               , flush=True)
        # self.sys.stdout.flush()
        # self.sys.stdout.write('\r'
        #                + '*'*int(rate*self.progress_bar_lenth)
        #                + '-'*(self.progress_bar_lenth - int(rate*self.progress_bar_lenth))
        #                + str(int(rate*100))
        #                + '%'
        #                + self.info
        #                + padding
        #                + ' '*45
        #                + '\r')
        # self.sys.stdout.flush()

    def toString(self, count):
        rate = count/self.totlecount
        return(
                 '*'*int(rate*self.progress_bar_lenth)
               + '-'*(self.progress_bar_lenth - int(rate*self.progress_bar_lenth))
               + str(int(rate*100))
               + '%'
               + self.info
               )

    def update(self, pad=''):

        self.count += 1
        #print(self.count)
        self.flush(self.count, pad)

    def run(self, result_queue):
        while(True):
            if(self.count == self.totlecount): break
            self.update(result_queue.get())

    def curses_run(self, result_queue):
        wholescr = curses.initscr()
        stdscr = curses.newpad(100, 100)
        while(True):
            self.count += 1
            if(self.count == self.totlecount): break
            messege_string = result_queue.get()
            title_string = self.toString(self.count)
            messege_string += ' ' * (self.console_col - len(messege_string))
            # stdscr.refresh()
            stdscr.refresh(0, 0, 5, 5, 20, 75)
            stdscr.addstr(2,0,title_string)
            stdscr.addstr(3,0,messege_string)
        curses.endwin()

if __name__ == "__main__":
    t = Timelinebar(100)
    t.setinfo("haha")
    for i in range(100):
        t.flush(i)
        sleep(0.05)
    print("\n3")
