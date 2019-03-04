#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 18:39:23 2019

@author: shuichi

# 論文のタイトルから以下の情報を抜き出す
1.どんなことをしているのか
2.技術や手法のキモ
3.対象とする分野・目的
4.条件

"""

import MeCab
import CaboCha

import pandas as pd
import numpy as np

import re
import sys
import datetime
import time
import os
import subprocess
from itertools import chain



def extractNoun(text):
    # パース
    #mecab = MeCab.Tagger("-u ./userdic/myterm.dic")
    mecab = MeCab.Tagger()
    parse = mecab.parse(text)
    lines = parse.split('\n')
    items = (re.split('[\t,]', line) for line in lines)
    # 名詞をリストに格納
    return [item[0] for item in items
            if (item[0] not in ('EOS', '', 't', 'ー') and
                 item[1] == '名詞' and item[2] == '一般')]
                
def extract_eightpart(text,part="名詞"):
    # パース
    #mecab = MeCab.Tagger("-u ./userdic/myterm.dic")
    mecab = MeCab.Tagger()
    parse = mecab.parse(text)
    lines = parse.split('\n')
    items = (re.split('[\t,]', line) for line in lines)
    # 名詞をリストに格納
    return [item[0] for item in items
            if (item[0] not in ('EOS', '', 't', 'ー') and
                 item[1] == part)] 


methodword=[
        "適用し",
        "による",
        "利用し",
        "付き",
        "用い",
        "基づ",
        "着目し",
        "適した",
        "組み合わせた",
        "からの"]
objectword=[
        "における",
        "目的と",
        "向けた",
        "ための",
        "対応可能な",
        "に対する",
        "対象と"]

def return_methodword(text):
        returnword = { word :"method" for word in methodword if word in text}
        return returnword
def return_objectword(text):
        returnword = {word : "object"for word in objectword if word in text}
        return returnword

def list2flatten(l):
    return list(chain.from_iterable(l))
if __name__ == '__main__':
    
    search_results_df=pd.read_csv("Google_Scholar.csv",index_col=0)
    
    """
    ### making dictonary
    with open("./userdic/japtext.txt", 'w') as f:
        f.write("\n".join(search_results_df["title"].values))
    
    ## wakatigaki by janome and output janome_extracted.txt
    command = ["python", "./userdic/termex_janome.py", "./userdic/japtext.txt"] #python termex_janome.py japanese_text.txt
    subprocess.call(command)
    
    # transform from csv to .dic file
    command = ["python", "./userdic/makedic.py"] #python termex_janome.py japanese_text.txt
    subprocess.call(command)
    """
    c = CaboCha.Parser()
    #cabocha ref: http://njf.jp/cms/modules/xpwiki/?%E8%87%AA%E7%84%B6%E8%A8%80%E8%AA%9E%E8%A7%A3%E6%9E%90%2FCaboCha%E3%82%92python%E3%81%A7%E4%BD%BF%E3%81%86
    
    
    methodlist=[]
    objectlist=[]
    achivementlist=[]
    
    for x in search_results_df["title"]:
        """
        print("###",x)
        print("名詞:",extract_eightpart(x,"名詞"))
        print("名詞一般:",extractNoun(x))
        print("動詞:",extract_eightpart(x,"動詞"))
        print("助詞:",extract_eightpart(x,"助詞"))
        #print(extractNoun(x))
        print(c.parseToString(x))
        tree =  c.parse(x)
        """
        print("########")
        object_sentence=[]
        method_sentence=[]
        #search object sentence
        tmp010=dict(return_objectword(x), **return_methodword(x))
        tmp011=dict(sorted({dictword:x.find(dictword) for dictword in tmp010.keys()}.items(), key=lambda x: x[1]))
        rear_sentence=x
        for splitword in tmp011.keys():
            dividedsentence=rear_sentence.split(splitword)
            rear_sentence=dividedsentence[1]
            if tmp010[splitword] =='object':
                object_sentence.append(dividedsentence[0])
            else:
                method_sentence.append(dividedsentence[0])
        #extract noun
        method_sentence=list2flatten([extract_eightpart(x) for x in method_sentence])
        object_sentence=list2flatten([extract_eightpart(x) for x in object_sentence])
        #output
        print("sentence:",x)
        print("object:", object_sentence)
        print("method:", method_sentence)
        print("rear_sentence:",extract_eightpart(rear_sentence))
        
        #append
        methodlist.append(" ".join(method_sentence))
        objectlist.append(" ".join(object_sentence))
        achivementlist.append(" ".join(extract_eightpart(rear_sentence)))
        #sprint(tree.toString(CaboCha.FORMAT_LATTICE))
    
    search_results_df["methodlist"]=methodlist
    search_results_df["objectlist"]=objectlist
    search_results_df["achivementlist"]=achivementlist
    search_results_df.to_csv("Google_Scholar.csv", encoding="utf-8")
    
    
    
    """
    
    print("#################################")
    sampletext="IoT環境における利用者の状況に基づく生活支援システムの検討"
    print(sampletext)
    #tree.toString(CaboCha.FORMAT_TREE).replace("-","").replace(" ","").replace("D","").split("\n")
    
    tree =  c.parse(sampletext)
    
    for i in range(tree.chunk_size()):
        chunk = tree.chunk(i)
        print('Chunk:', i)
        print(' Score:', chunk.score)
        print(' Link:', chunk.link)
        print(' Size:', chunk.token_size)
        print(' Pos:', chunk.token_pos)
        print(' Head:', chunk.head_pos) # 主辞
        print(' Func:', chunk.func_pos) # 機能語
        print(' Features:')
        
        for j in range(chunk.feature_list_size):
            print(chunk.feature_list(j))
    
    print("#################################")
    for i in range(tree.token_size()):
        D = tree.token(i)
        print('Surface:', token.surface)
        print(' Normalized:', token.normalized_surface)
        print(' Feature:', token.feature)
        #print(' NE:', token.ne) # 固有表現
        #print(' Info:', token.additional_info)
        print(' Chunk:', token.chunk)
        
    
    """
    
    
    #####
    
    tmp001=search_results_df["title"][search_results_df["methodlist"] !=""]
