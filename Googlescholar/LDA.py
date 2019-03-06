#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 08:32:29 2019

@author: shuichi

#ref:https://openbook4.me/projects/193/sections/1154
解析のストラレジー

    MeCabとかで、文章から日本語、例えば名詞だけを抽出した配列を作る。
    Gensimで特徴語辞書を作る。この特徴語辞書にfilterをかけて、高頻度or低頻度すぎるものを削除する。
    GensimのBoWで各文章の特徴語をカウントして特徴ベクトルを作る。
    何個か正解の特徴ベクトルでfitさせてtrainingさせる

gensimのinstallと、documentを定義する。

"""


import datetime
import time
import os
import numpy as np
import pandas as pd

from gensim import corpora, models, similarities
import matplotlib.pyplot as plt

from wordcloud import WordCloud

def splitdfwords(text):
    return text.split(" ")
def not_exist_mkdir( output_path ):
    if( not os.path.exists(output_path) ):
        os.mkdir( output_path )
def get_keys_from_value(d, val):
    tmp=[k for k, v in d.items() if v == val]
    if  not tmp: # when empty array
        return None
    else:
        return tmp[0]
    
def plot_polar(labels, values, imgname):
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)
    values = np.concatenate((values, [values[0]]))  # 閉じた多角形にする
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-')  # 外枠
    ax.fill(angles, values, alpha=0.25)  # 塗りつぶし
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)  # 軸ラベル
    ax.set_rlim(0 ,250)
    fig.savefig(imgname)
    plt.close(fig)

labels = ['HP', 'Attack', 'Defense', 'Speed',"type"]
values = [155, 156, 188, 139,90]
plot_polar(labels, values, "radar.png")

if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    
    not_exist_mkdir("./tmp")
    
    search_results_df=pd.read_csv("Google_Scholar.csv",index_col=0)
    
    
    search_results_df["methodlist"]=search_results_df["methodlist"].fillna("")
    search_results_df=search_results_df[search_results_df["methodlist"] !=""].fillna("")
    docs=search_results_df["achivementlist"]
    #docs = search_results_df["achivementlist"].fillna("")
    #docs = search_results_df["methodlist"].fillna("")
    
    texts=list(map(splitdfwords,docs))
    dictionary = corpora.Dictionary(texts)
    dictionary.save('./tmp/deerwester.dict')
    # store the dictionary, for future reference
    # バイナリではなくテキストとして保存する場合
    dictionary.save_as_text('./tmp/deerwester_text.dict')
    
    
    #print dictonary 
    #dictionaryからdictionary形式に特徴語を吐き出す。 それぞれの単語にidを付与する。
    print(dictionary.token2id)
    
    #example to vectolization
    #この特徴語辞書により、文章(単語)を特徴ベクトルに変換する事ができる。
    #doc2bowというbag of wordsを体現した関数があり、これで単語IDと頻度のタプルに変換した特徴ベクトルになおしてくれる。
    new_doc = "行動 ラベリング システム  hogehoge II"
    new_vec = dictionary.doc2bow(new_doc.split())
    print(new_vec)
    
    #making corpus
    #text全体に対する特徴ベクトルの集合= corpusを作成する。
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('./tmp/deerwester.mm', corpus) # store to disk, for later use
    print(corpus)
    
        
    #corpusは膨大になってしまうため、一度Matrix Market fileに保存される（した）。 これを呼び出す。
    corpus = corpora.MmCorpus('./tmp/deerwester.mm')
    
    #### LSI
    #corpusのtrainingのためのtfidfというオブジェクトをcorpusから作る。	
    tfidf = models.TfidfModel(corpus)
    #特徴ベクトルがtfidfベクトル空間のベクトルに変換することができる。
    doc_bow = dictionary.doc2bow("3 次元 物体 認識".split())
    print( [(get_keys_from_value(dictionary.token2id,x[0]),x[1]) for x in tfidf[doc_bow]])
    print(tfidf[doc_bow])
    # step 2 -- use the model to transform vectors
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=6)
    corpus_lsi = lsi[corpus_tfidf]
    # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
    #これをcorpusに適用する。 (一度使ったデータを、そのデータがtrainingで作ったtfidf空間へと変換する)
    
    #tfidf空間にlsiモデルを作成する。そしてlsiで分類されたもののcorpusを抽出。
    lsi.print_topics()
    
    for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
        print(doc)
    lsi.save('./tmp/model.lsi') # same for tfidf, lda, ...
    
    
    ###### LDA
    #ref: http://blog.yuku-t.com/entry/20110623/1308810518
    
    #model = ldamodel.LdaModel(bow_corpus, id2word=dictionary, num_topics=100)
    lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=16)
    lda.save('./tmp/jawiki_lda.model')  # せっかく計算したので保存
    print(lda.print_topics(6))
    corpus_lda = lda[corpus_tfidf]
    
    def get_topic(doc):
        return sorted(doc, key=lambda x:x[1],reverse=True)[0][0]
    topicclass=[get_topic(doc) for doc in corpus_lda]
    search_results_df["topicclass"]=topicclass
    
    ### clustering LDA topic result
    # get topicvector df
    topicname=["topic"+str(i) for i in range(lda.num_topics)]
    topicdata=pd.DataFrame(columns=topicname)
    for i,doc in enumerate(corpus_lda): # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
        #print(doc)
        topicdata.loc[i]=[x[1] for x in doc]
        
    #clusering
    from sklearn.cluster import KMeans
    clusters_resultlist=[]
    cluster_num=int(lda.num_topics/2)
    clusters = KMeans(n_clusters=cluster_num, random_state=0).fit_predict(topicdata)
    
    # print each cluster's topic strength
    topicdata["clusters"]=clusters
    leadervector=[]
    for i in range(cluster_num):
        leadervector.append(list(topicdata[topicdata["clusters"]==i].mean()[topicname]))
    
    # make radar chart #ref:https://qiita.com/1007/items/80406e098a4212571b2e
    labels = topicname
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    for radardata in leadervector:
        radardataTMP=np.concatenate((radardata, [radardata[0]]))  # 閉じた多角形にする
        ax.plot(angles, radardataTMP, 'o-')  # 外枠
        ax.fill(angles, radardataTMP, alpha=0.25)  # 塗りつぶし
    
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)  # 軸ラベル
    ax.set_rlim(0 ,max(max(leadervector)))
    fig.savefig("radar.png")
    plt.show()
    plt.close(fig)
    
    ############# Word cloud
    fig, axs = plt.subplots(ncols=4, nrows=int(lda.num_topics/4), figsize=(25,17))
    axs = axs.flatten()
    
    def color_func(word, font_size, position, orientation, random_state, font_path):
        return 'darkturquoise'
    from PIL import Image
    mask = np.array(Image.open('ball.png'))
    
    for i, t in enumerate(range(lda.num_topics)):
        x = dict(lda.show_topic(t, 30))
        im = WordCloud(
            font_path='./fonts/sawarabi-mincho-medium.ttf',
            background_color='white',
            color_func=color_func,
            mask=mask,
            random_state=0
        ).generate_from_frequencies(x)
        axs[i].imshow(im)
        axs[i].axis('off')
        axs[i].set_title('Topic '+str(t))
            
    plt.tight_layout()
    plt.savefig("wordball.png")
    plt.show()
    
    #############
    #tf-idf特徴量の最も大きい単語を示す。
    def get_maximum_tfidfword(word):
        doc_bow = dictionary.doc2bow(word.split())
        tmp01011=[(get_keys_from_value(dictionary.token2id,x[0]),x[1]) for x in tfidf[doc_bow]]
        return sorted(tmp01011, key=lambda x:x[1],reverse=True)[0][0]
    
    search_results_df["maximum_tfidfword"]=list(map(get_maximum_tfidfword,search_results_df["achivementlist"]))
    
    tmp001=search_results_df[["title","topicclass","achivementlist","maximum_tfidfword"]][search_results_df["methodlist"] !=""]
        
    print("############ summary #############")
    print("dictionary lenth:",len(dictionary))
    print("corpus_tfidf lenth:",len(corpus_tfidf))          
              
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )