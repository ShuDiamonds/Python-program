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
dbpath = 'History'
#dbpath = r'C:\Users\{0}\AppData\Local\Google\Chrome\User Data\Default\History'.format(os.getlogin())

# データベース接続とカーソル生成
connection = sqlite3.connect(dbpath)
# 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
# connection.isolation_level = None
cursor = connection.cursor()

# 全行をlistで返す
cursor.execute( "select * from keyword_search_terms" )
#cursor.execute( "PRAGMA TABLE_INFO(urls);" )
#cursor.execute( "select name from sqlite_master where type='table';" )
tmp = cursor.fetchall()
df1=pd.DataFrame(tmp)
print( tmp )
  #=> [('1', 'test1'), (2, 'test2'), (3, 'test3'), (4, 'test4')]
cursor.close()


