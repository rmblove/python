#!/usr/local/bin/python3
# -*- coding = 'utf-8' -*-
import re
import sys
from time import sleep
import queue
from SETTING import config as cfg
import sqlite3

class mimeadapter:
    def __init__(self):
        pass

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return "string"

class simpleSqlite:

    def __init__(self):
        self.conn = sqlite3.connect(cfg["DATABASE_PATH"])
        self.conn.isolation_level = None
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def insert(self, msg):
        email_path = msg["EmailPath"]
        email_from = re.search(r"<.*>", str(msg["From"])).group(0)
        email_to = msg['To']
        self.cur.execute("INSERT INTO dnc_email_20160811 (EMAIL_PATH, EMAIL_FROM, EMAIL_TO) VALUES (?, ?, ?)",
                    (email_path, email_from, email_to)
                    )

    def insertall(self, msg):
        email_path = msg["EmailPath"]
        email_from = re.search(r"<.*>", str(msg["From"])).group(0)
        email_to = msg['To']
        email_to = re.findall(r"<.*?>", str(email_to))
        email_to = ','.join(email_to)
        email_date = msg['Date']
        email_subject = msg['Subject']
        self.cur.execute("INSERT INTO dnc_email_20160815 (EMAIL_PATH, EMAIL_FROM, EMAIL_TO, EMAIL_DATE, email_subject) VALUES (?, ?, ?, ?, ?)",
                    (email_path, email_from, email_to, email_date, email_subject)
                    )

    def run(self, task_queue):
        "This method is for multiprocessing only."
        while(True):
            try:
                try:
                    mime = task_queue.get(timeout=10)
                except Exception as e:
                    sys.stderr.write(str(e))
                    print("\nDatabase is done\n")
                    break
                self.insert(mime)
            except Exception as e:
                sys.stderr.write(mime["EmailPath"]+str(e)+"\n")
                continue
        self.conn.commit()
        self.conn.close()

    def run_withcallback(self, task_queue, callback):
        "This method is for multiprocessing only."
        while(True):
            try:
                try:
                    mime = task_queue.get(timeout=10)
                    if type(mime)==str:
                        callback.update(mime)
                        continue
                    callback.update(mime["EmailPath"])
                except Exception as e:
                    sys.stderr.write(str(e))
                    print("\nDatabase is done\n")
                    break
                self.insertall(mime)
            except Exception as e:
                sys.stderr.write(mime["EmailPath"]+str(e)+"\n")
                continue
        self.conn.commit()
        self.conn.close()




if __name__ == "__main__":
    conn = sqlite3.connect(cfg["DATABASE_PATH"])
    conn.execute("""CREATE TABLE dnc_email_20160815
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    EMAIL_PATH text,
                    EMAIL_FROM text,
                    EMAIL_TO text,
                    EMAIL_DATE text,
                    EMAIL_SUBJECT text)
    """)
    conn.commit()
    conn.close()
    # cur = conn.cursor()
    # OK = mimeadapter()
    # cur.execute("INSERT INTO email VALUES (?,?,?)", (OK,))
    # conn.commit()
    # cur.execute("SELECT * FROM email")
    # for row in cur:
    #     print(row)
