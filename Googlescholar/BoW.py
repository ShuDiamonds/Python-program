#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 08:21:30 2019

@author: shuichi
#BoW url:https://www.haya-programming.com/entry/2018/02/25/044525#%E5%90%8D%E8%A9%9E%E3%81%A0%E3%81%91%E3%81%A7BoW%E3%82%92%E4%BD%9C%E3%82%8B%E6%9B%B4%E3%81%ABstemming%E3%82%82%E8%A1%8C%E3%81%86

"""

import datetime
import time
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer

if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    
    search_results_df=pd.read_csv("Google_Scholar.csv",index_col=0)
    docs = search_results_df["achivementlist"]
    
    count = CountVectorizer()
    
    bag = count.fit_transform(docs)
    
    print(count.vocabulary_)
    print("############")
    bagvector=bag.toarray()
    print(bagvector)
    
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )