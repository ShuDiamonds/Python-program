# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 10:10:27 2019

@author: fukuda
"""
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import matplotlib


def not_exist_mkdir( output_path ):
    if( not os.path.exists(output_path) ):
        os.mkdir( output_path )
if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    sns.set()
    
    #parser = lambda date: pd.to_datetime(date, format='%Y/%m/%d  %H:%M:%S')
    parser = lambda date: pd.to_datetime(date, format='%Y_%m_%d %H:%M:%S')
    df = pd.read_csv('data.csv', index_col=0,parse_dates=True,date_parser=parser)    
    #df = pd.read_csv('data.csv',encoding="shift_jisx0213",header=2,skiprows=1,index_col=0, parse_dates=True,date_parser=parser)
    #df = pd.read_csv('data.csv',header=4,skiprows=[5],index_col=0, parse_dates=True,date_parser=parser)    
    
    df["count"]=1
    groupedby1hourdf=df.groupby(pd.TimeGrouper(freq='1H')).sum().fillna(0)
    groupedby1hourdf["weekday_name"]=groupedby1hourdf.index.weekday_name
    groupedby1hourdf["hour"]=groupedby1hourdf.index.hour
    ###
    #groupedby1hourdf.groupby("weekday_name","hour").sum()
    
    heatmapdata=pd.DataFrame()
    weekdays=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    for weekday in weekdays:
        #print("######## {0} ##########".format(weekday))
        #print(groupedby1hourdf[groupedby1hourdf["weekday_name"]==weekday].groupby("hour").sum())
        heatmapdata[weekday]=groupedby1hourdf[groupedby1hourdf["weekday_name"]==weekday].groupby("hour").sum()["count"]
    
    #make heatmap
    plt.figure()
    sns.heatmap(heatmapdata)
    #plt.savefig('seaborn_hetmap.png')
    plt.show()
    plt.close('all')

        
        
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )#!/usr/bin/env python3
