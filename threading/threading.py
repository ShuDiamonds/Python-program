# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 12:05:16 2018

@author: shuichi
"""

import time
import threading
text="hoge1"
def func1():
    time.sleep(1)
    print(text)
    

def func2():
    print(text)
    time.sleep(1)

if __name__ == "__main__":
    thread_1 = threading.Thread(target=func1)
    thread_2 = threading.Thread(target=func2)

    thread_1.start()
    thread_2.start()
    text="aaa"
