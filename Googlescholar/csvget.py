# -*- coding: utf-8 -*-
"""
ref: https://qiita.com/kuto/items/9730037c282da45c1d2b
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import sys
import datetime
import time
import os

def not_exist_mkdir( output_path ):
    if( not os.path.exists(output_path) ):
        os.mkdir( output_path )

def get_search_results_df(keyword,number=10,year=2015):
    columns = ["rank", "title", "writer", "year", "citations", "url","pdf_url","citations_url"]
    df = pd.DataFrame(columns=columns) #表の作成
    #html_doc = requests.get("https://scholar.google.co.jp/scholar?hl=ja&as_sdt=0%2C5&num=" + str(number) + "&q=" + keyword).text
    html_doc = requests.get("https://scholar.google.co.jp/scholar?"+"as_ylo="+str(year)+ "&q=" + keyword+"&hl=ja&as_sdt=0,5"+"&num="+str(number) ).text
    soup = BeautifulSoup(html_doc, "html.parser") # BeautifulSoupの初期化
    #tags = soup.find_all("div", {"class": "gs_ri"}) 
    tags = soup.find_all("div", {"class": "gs_r"}) 
    print(len(tags))
    
    rank = 1
    not_exist_mkdir("pdf")
    for tag in tags:
        try:
            ### get title
            title = tag.find("h3", {"class": "gs_rt"}).text.replace("[HTML]","")
            try:
                url = tag.find("h3", {"class": "gs_rt"}).select("a")[0].get("href")
            except:
                print(sys.exc_info())
                url=None
            
            ### PDF get
            try:
                pdf_url = tag.find("div", {"class": "gs_or_ggsm"}).select("a")[0].get("href")
                try:
                    r = requests.get(pdf_url)
                    if r.status_code == 200:
                        file_name=title.replace("/"," ").replace("/","").replace(":"," ").replace(";"," ").replace("="," ").replace("?"," ").replace("|"," ").replace("<"," ").replace(">"," ")+".pdf"
                        with open("./pdf/"+file_name, 'wb') as f:
                            f.write(r.content)
                except:
                    print(sys.exc_info())
                    pass
            except:
                pdf_url=None
            
            ### get writer info
            writer = tag.find("div", {"class": "gs_a"}).text
            writer = re.sub(r'\d', '', writer)
            year = tag.find("div", {"class": "gs_a"}).text            
            year = re.search(r'\d{4}', year).group()
            
            ### get citations
            try:
                citations = tag.find(text=re.compile("引用元")).replace("引用元","")
                citations_url = "https://scholar.google.co.jp"+tag.find("div", {"class": "gs_fl"}).find("a",href=re.compile(r"/scholar.cites.*")).get("href")
            except:
                citations=None
                citations_url=None
            se = pd.Series([rank, title, writer, year, citations, url,pdf_url,citations_url], columns)
            df = df.append(se, columns)
            rank += 1
        except:
            print("rank{0} has errored".format(rank))
            print(sys.exc_info())
            
        
    
    return df

if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    
    keyword = "遺伝的アルゴリズム"
    number = 10
    year=2015
    search_results_df = get_search_results_df(keyword,number,year)
    filename = "Google_Scholar.csv"
    search_results_df.to_csv(filename, encoding="utf-8")
    
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )#!/usr/bin/env python3

