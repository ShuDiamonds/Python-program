#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 12:50:29 2018

@author: shuichi
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import MeCab
import datetime
import time

from sklearn.cluster import KMeans
from gensim.models import word2vec

import plotly.graph_objs as go
import plotly.offline as offline

import numpy as np
import matplotlib.pyplot as plt

from sklearn import decomposition
from sklearn import datasets
import re


if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    
    search_results_df=pd.read_csv("Google_Scholar.csv",index_col=0)
    docs = search_results_df["achivementlist"]
    #np.set_printoptions(precision=2)##有効桁2桁で丸める
    
    stop_wordslist=["及び","する","および","により","同じ","入力","乗じ"]
    
    #vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
    vectorizer = TfidfVectorizer(use_idf=True,min_df=0.03,stop_words=stop_wordslist)
    vecs = vectorizer.fit_transform(docs)
    
    temp=vecs.toarray()
    colnames=sorted(vectorizer.vocabulary_.items(), key=lambda x:x[1])
    print(vecs.toarray())
    
    K = 15 #top k 
    for i in np.arange(temp.shape[0]):
        my_array=temp[:][i]
        # ソートはされていない上位k件のインデックス
        unsorted_max_indices = np.argpartition(-my_array, K)[:K]
        # 上位k件の値
        y = my_array[unsorted_max_indices]
        print("##### {0} ###########".format(i))
        for tfidfindex,value in zip(unsorted_max_indices,y):
            print(colnames[tfidfindex][0],value)
    
    """
    for k,v in sorted(vectorizer.vocabulary_.items(), key=lambda x:x[1]):
        print(k,v)
    """
    
    # クラスタリング
    clusters_resultlist=[]
    clusters = KMeans(n_clusters=10, random_state=0).fit_predict(vecs)
    for doc, cls in zip(docs, clusters):
        #print(cls, doc)
        clusters_resultlist.append([cls, doc])
    search_results_df["cluster"]=pd.DataFrame(clusters_resultlist)[0]
    sorted_clusters_resultlist=sorted(clusters_resultlist, key=lambda x:x[0])
    
   
    #############
    
    offline.init_notebook_mode()
    pca = decomposition.PCA(n_components=3)
    pca.fit(vecs.toarray())
    X = pca.transform(vecs.toarray())
    trace = go.Scatter3d(x=X[:, 0], y=X[:, 1], z=X[:, 2], 
                         mode='markers+text',
                         marker=dict(color=clusters,
                                     colorscale="Viridis",
                                     line=dict(color='black', width=1)),
                         text=list(search_results_df["achivementlist"].values)
                         )
    
    layout = go.Layout(scene=
                       dict(
                            xaxis=dict(ticks='', showticklabels=False),
                            yaxis=dict(ticks='', showticklabels=False),
                            zaxis=dict(ticks='', showticklabels=False),
                           )
                      )
    
    fig = go.Figure(data=[trace], layout=layout)
    offline.plot(fig, filename='./pca.html', image_filename='test', image='jpeg')
    
    #############
    
    
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )