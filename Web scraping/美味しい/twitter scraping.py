
# coding: utf-8

# In[10]:


# -*- coding: utf-8 -*-
import sys
import os
import bs4
import json
import urllib
import requests
import re
#from da_vinci import Image
from time import sleep


# クロールしたいユーザのID
crawle_user_id = 'nnahito'


def outputCsv(screen_name, user_name, tweet_timestamp, tweet_body):
    """
    # データをCSVに書き出す
    #  @params screen_name       string              ユーザのスクリーン上の名前（例：Nな人）
    #  @params user_name         string              ユーザの半角英数の名前（例：nnahito）
    #  @params tweet_timestamp   string              ツイート日時
    #  @params tweet_body        string              ツイート本文
    """

    # 書き出すファイル名を決定（ユーザ名.csv）
    file_name = 'outoput.csv'

    # 改行などを削除
    screen_name = screen_name.replace('\n','').replace('\r','')
    user_name = user_name.replace('\n','').replace('\r','')
    tweet_body = tweet_body.replace('\n','').replace('\r','')

    # 出力
    f = open(file_name, 'a')
    f.write(screen_name + ',' + user_name + ',' + tweet_timestamp + ',' + tweet_body + ',' + "\n")
    f.close()


def parseHtml(html_data):
    """
    # 与えられたHTMLをパースしてファイルに書き出します
    #  @paramas html_data           解析したいHTML
    """
    # HTMLを解析
    soup = bs4.BeautifulSoup(html_data)

    # ツイートをブロック単位（ul）に分解
    tweet_blocks = soup.select('.tweet')

    # ツイートのブロックを一つずつ抽出
    for tweet_block in tweet_blocks:
        # スクリーンネームを取得
        screen_name = tweet_block.select('.fullname')[0].text

        # ユーザネームを取得
        user_name = tweet_block.select('.username')[0].text

        # ツイートの日時を取得
        tweet_timestamp = tweet_block.select('.tweet-timestamp')[0].text

        # ツイート内容を取得
        tweet_body = tweet_block.select('.tweet-text')[0].text

        # CSVに出力
        print(screen_name + ',' + user_name + ',' + tweet_timestamp + ',' + tweet_body + ',' + "\n")
        outputCsv(screen_name, user_name, tweet_timestamp, tweet_body)


def getMinPosition(html_data):
    """
    # 次の取得開始位置を抽出し、返します
    #  @params html_data        string          解析するHTMLデータを渡します
    #  @return                  string          次の開始位置（min_position）が返ります
    """
    # HTMLを解析
    soup = bs4.BeautifulSoup(html_data)

    # min-positionを抽出
    min_position = soup.select('div[data-min-position]')[0].attrs['data-min-position']

    # 値を返却
    return min_position


def getNextTweet(user_id, max_position):
    """
    # 与えられたポジションから再帰的にクロールを始めます
    #  @params user_id      string          Twitter上の半角英数のユーザ名（例：nnahito）
    #  @params max_position string          次のTwitterのつぶやきID
    """
    # URLの作成
    base_url = 'https://twitter.com/i/profiles/show/'+ user_id +'/timeline/tweets?include_available_features=1&include_entities=1&max_position='+ max_position +'&reset_error_state=false'

    # ベースURLからデータを取得
    url_data = urllib.request.urlopen(base_url)

    # JSON形式でデータを取得
    content = json.loads(url_data.read().decode('utf8'))

    # 次取得のIDを記録しておく
    next_position = content['min_position']

    # HTMLをパースしてファイルに書き出し
    parseHtml(content['items_html'])
    print(next_position + 'の出力完了')

    # 一応スリープをかませる
    sleep(1)

    # 再起的に呼び出す
    getNextTweet(user_id, next_position)


def getFirstTweet(user_id):
    """
    # 与えられたUserIDから、最初のTweetを取得します
    #  @params user_id      string          取得したいユーザの半角英数のユーザ名（例：nnahito）
    """
    # ベースURLからデータを取得
    url_data = urllib.request.urlopen('https://twitter.com/' + user_id)

    # HTMLデータを取得
    html_data = url_data.read()

    # パースして書き出し
    parseHtml(html_data)

    # 取得開始位置を取得
    max_position = getMinPosition(html_data)

    # 次
    getNextTweet(crawle_user_id, max_position)

# プログラム実行
getFirstTweet(crawle_user_id)

