# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 13:37:35 2018

@author: shuichi

spreadsheet setteing : https://qiita.com/akabei/items/0eac37cb852ad476c6b9

spreadsheet function : https://tanuhack.com/python/library-gspread/
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


if __name__ == "__main__":
    credentials = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet.json', scope)
    gc = gspread.authorize(credentials)
    workbook = gc.open('gspread_sample')
    worksheet = workbook.sheet1
    print(workbook.title)	#スプレッドシートのタイトルを取得する
    print(workbook.id)		#スプレッドシートキーを取得する
    
    # １．ラベルを指定してセルの値を取得する
    cell_value = worksheet.acell('B1').value
    
    # ２．行番号と列番号を指定してセルの値を取得する（左：行番号、右：列番号）
    cell_value = worksheet.cell(1, 2).value
    
    # ３．ラベルを指定して複数セルの値を一次元配列に格納する
    range1 = worksheet.range('A1:B10')
    
    data=["time","value"]
    worksheet.append_row(data)
    
    