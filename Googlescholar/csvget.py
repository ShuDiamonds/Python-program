# -*- coding: utf-8 -*-
"""
ref: https://qiita.com/kuto/items/9730037c282da45c1d2b
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import re
import sys
import datetime
import time
import os
import subprocess


def not_exist_mkdir( output_path ):
    if( not os.path.exists(output_path) ):
        os.mkdir( output_path )
    
    
def get_article_detail(detail_url,detail_text):
    try:
        html_doc_detail=requests.get(detail_url)
        html_doc_detail.encoding=html_doc_detail.apparent_encoding
        html_doc_detail = html_doc_detail.text
        soup_detail = BeautifulSoup(html_doc_detail, "html.parser") # BeautifulSoupの初期化
        return soup_detail.find(text=re.compile(detail_text))
    except:
        return "error"
def get_maximum_page_numbert(keyword,startpage=0,year=2015):
    html_doc = requests.get("https://scholar.google.co.jp/scholar?"+"as_ylo="+str(year)+ "&q=" + keyword+"&hl=ja&as_sdt=0,5"+"&start="+str(startpage) ).text
    soup = BeautifulSoup(html_doc, "html.parser") # BeautifulSoupの初期化
    tags = soup.find_all("a", {"class": "gs_nma"})
    pagenumbers=[]
    for tag in tags:
        try:
            pagenumbers.append(int(tag.text))
        except:
            pass
    return max(pagenumbers)
    
def get_search_results_df(keyword,startpage=0,year=2015,pdfgetflag=False):
    columns = ["rank", "title", "writer", "year", "citations",
               "url","pdf_url","citations_url","explanation_detail"]
    df = pd.DataFrame(columns=columns) #表の作成
    #html_doc = requests.get("https://scholar.google.co.jp/scholar?hl=ja&as_sdt=0%2C5&num=" + str(number) + "&q=" + keyword).text
    html_doc = requests.get("https://scholar.google.co.jp/scholar?"+"as_ylo="+str(year)+ "&q=" + keyword+"&hl=ja&as_sdt=0,5"+"&start="+str(startpage) ).text
    soup = BeautifulSoup(html_doc, "html.parser") # BeautifulSoupの初期化
    #tags = soup.find_all("div", {"class": "gs_ri"}) 
    tags = soup.find_all("div", {"class": "gs_r"}) 
    
    rank = startpage
    not_exist_mkdir("pdf")
    not_exist_mkdir("explanation")
    for tag in tags:
        try:
            ### get title
            title = tag.find("h3", {"class": "gs_rt"}).text.replace("[HTML]","")
            url_is_correct_flag=title.find("[PDF]") == -1 and title.find("[引用]")== -1 # when both are true, its okay
            title = title.replace("[PDF]","")
            url=None
            try:
                url = tag.find("h3", {"class": "gs_rt"}).select("a")[0].get("href")
            except:
                print(sys.exc_info())
                pass
            
            ### PDF get
            pdf_url=None
            if pdfgetflag:
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
                    pass
            
            ### get writer info
            writer = tag.find("div", {"class": "gs_a"}).text
            writer = re.sub(r'\d', '', writer)
            year = tag.find("div", {"class": "gs_a"}).text            
            year = re.search(r'\d{4}', year).group()
            
            ### get citations
            citations=None
            citations_url=None
            try:
                citations = int(tag.find(text=re.compile("引用元")).replace("引用元",""))
                citations_url = "https://scholar.google.co.jp"+tag.find_all("a",href=re.compile(r"/scholar.cites.*"))[0].get("href")
            except:
                pass
            
            ### get explanation
            explanation_detail=""
            if url_is_correct_flag==True:
                try:
                    explanation = tag.find("div", {"class": "gs_rs"}).text[7:10]
                    print(explanation)
                    #explanation_detail=get_article_detail(detail_url=url,detail_text=explanation)
                    #tmp=get_article_detail(detail_url=url,detail_text=explanation).replace("\n","").replace("\r","").replace("\t","")
                    tmp1=[str(rank),title,tmp]
                    with open("./explanation/"+keyword+".tsv", 'a') as f:
                                f.write("\t".join(tmp1)+"\n")
                except:
                    pass
            else:
                explanation_detail="it is pdf or has not url"
            ### make Dataframe
            se = pd.Series([rank, title, writer, year, citations, url,pdf_url,citations_url,explanation_detail], columns)
            df = df.append(se, columns)
            rank += 1
            
            
            print("rank{0} was done.".format(rank))   
        except:
            print("rank{0} has errored".format(rank))
            print(sys.exc_info())
         
    return df



if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    
    keyword = "照明 機械学習"
    startpage=0
    year=2005
    search_results_df=pd.DataFrame()
    
    ### get maximum page number
    maxpagenum=get_maximum_page_numbert(keyword=keyword,startpage=startpage,year=year)
    
    #search_results_df = get_search_results_df(keyword=keyword,startpage=startpage,year=year)
    for startpage in range(0,maxpagenum*10,10):
        time.sleep(1)
        print("startpage:"+str(startpage))
        search_results_df=search_results_df.append(get_search_results_df(keyword=keyword,startpage=startpage,year=year))
    search_results_df=search_results_df.reset_index(drop=True)
    filename = "Google_Scholar.csv"
    search_results_df.to_csv(filename, encoding="utf-8")
    
    
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )#!/usr/bin/env python3

