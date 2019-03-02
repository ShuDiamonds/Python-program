#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:30:00 2019

@author: shuichi
"""
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def __get_co_occurrence_matrix_from(keywords):
    # -----------------------------------------------------
    # 以下、CountVectorizer で共起単語行列を作る
    # ----------------------------------
    # from sklearn.feature_extraction.text import CountVectorizer
    # count_model = CountVectorizer(ngram_range=(
    #     1, 1), stop_words=utils.stop_words)  # default unigram model
    # X = count_model.fit_transform(keywords)

    # # normalized co-occurence matrix
    # import scipy.sparse as sp
    # Xc = (X.T * X)
    # g = sp.diags(2. / Xc.diagonal())
    # Xc_norm = g * Xc

    # import collections
    # splited_keywords = []
    # for keyword in keywords:
    #     splited_keywords.extend(utils.split_keyword(keyword))
    # counter = collections.Counter(splited_keywords)
    # return Xc_norm, count_model.vocabulary_, counter

    # -----------------------------------------------------
    # 以下、TfidfVectorizer で共起単語行列を作る
    # ----------------------------------
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(
        1, 1), max_df=0.5, min_df=1, max_features=3000, norm='l2')
    X = tfidf_vectorizer.fit_transform(keywords)
    # normalized co-occurence matrix
    import scipy.sparse as sp
    Xc = (X.T * X)
    g = sp.diags(2. / Xc.diagonal())
    Xc_norm = g * Xc

    import collections
    splited_keywords = []
    #for keyword in keywords:
    #   splited_keywords.extend(utils.split_keyword(keyword))
    counter = collections.Counter(splited_keywords)
    return Xc_norm, tfidf_vectorizer.vocabulary_, counter

def get_keys_from_value(d, val):
    tmp=[k for k, v in d.items() if v == val]
    if  not tmp: # when empty array
        return None
    else:
        return tmp[0]

if __name__ == '__main__':
    search_results_df=pd.read_csv("Google_Scholar.csv",index_col=0)
    print(search_results_df["achivementlist"])
    print("#############")
    
    # -------------------------
    # 2. 共起単語行列を作成する
    # -------------------------
    Xc_norm, vocabulary, counter = __get_co_occurrence_matrix_from(search_results_df["achivementlist"])
    """
    for x,y,z in zip(Xc_norm):
        print(x,y,z)
    """
    Xc_normMC=Xc_norm.tocoo()
    
    Xc_array=[[x,y,z] for x,y,z in zip(Xc_normMC.row,Xc_normMC.col,Xc_normMC.data)]
    Xc_dataframe=pd.DataFrame(Xc_array,columns=["row","col","data"])
    
    Xc_array=[[get_keys_from_value(vocabulary,x),get_keys_from_value(vocabulary,y),z] for x,y,z in zip(Xc_normMC.row,Xc_normMC.col,Xc_normMC.data)]
    Xc_dataframe_moziver=Xc_dataframe=pd.DataFrame(Xc_array,columns=["row","col","data"])
    
    dense=pd.DataFrame(Xc_norm.todense())
    sns.heatmap(dense)
    
    