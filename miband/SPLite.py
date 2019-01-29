# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 13:39:44 2018


@author: fukuda
 reffered url:http://www.mirandora.com/?p=697
 
 BrowsingHistoryViewもある
"""

# sqlite3 標準モジュールをインポート
import sqlite3
import pandas as pd


import os
print(os.getlogin())

# データベースファイルのパス
dbpath = 'db.sqlite'
#dbpath = r'C:\Users\{0}\AppData\Local\Google\Chrome\User Data\Default\History'.format(os.getlogin())

# データベース接続とカーソル生成
connection = sqlite3.connect(dbpath)
# 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
# connection.isolation_level = None
cursor = connection.cursor()

# 全行をlistで返す
#cursor.execute( "select * from sleep" )
#cursor.execute( "PRAGMA TABLE_INFO(urls);" )

cursor.execute( "select name from sqlite_master where type='table';" ) # データベースのテーブル取得
print(cursor.fetchall())

print("###############")
# テーブルの構造把握：https://www.dbonline.jp/sqlite/table/index2.html
cursor.execute( "select * from sqlite_master;" ) # データベースのテーブル取得 
tmp=cursor.fetchall()
#print(tmp)

# sleep データの取得
#CREATE TABLE `sleep` (`id` integer primary key,`start_time` integer,`end_time` integer,`awake` integer,`deep` integer,`light` integer,`stages` text,`deleted` integer,`manually` integer)

cursor.execute( "select * from steps;" ) # データベースのテーブル取得 
tmp1=cursor.fetchall()
print(tmp1)

df1=pd.DataFrame(tmp)

  #=> [('1', 'test1'), (2, 'test2'), (3, 'test3'), (4, 'test4')]
cursor.close()


