#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 17:59:19 2018

@author: shuichi
"""

import os
import datetime
import time

if __name__ == '__main__':
    progress_s_time = datetime.datetime.today()
    print('実行開始時間(Start time)：' + str( progress_s_time.strftime("%Y/%m/%d %H:%M:%S") ))
    progress_s_time = time.time()
    
    result_list=[]
    with open("./userdic/janome_extracted.txt", mode='r') as f:
        line = f.readline() # 1行を文字列として読み込む(改行文字も含まれる)
        while line:
            line = f.readline()
            line1=line.split("\t")
            if line1[0].find(',') > -1:
                pass
            else:
                #format 表層形,左文脈ID,右文脈ID,コスト,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
                convertedtext="{0},,,1,名詞,一般,*,*,*,*,{0},,{0}".format(line1[0])
                result_list.append(convertedtext)
        #end while
    result_list.pop(-1)
    #saving
    allText = '\n'.join(result_list)
    with open("./userdic/converted_pre-dic.csv", mode='w') as f:
        f.write(allText)
    
    
    os.system('/usr/lib/mecab/mecab-dict-index -d /usr/lib/mecab/dic/mecab-ipadic-neologd/ -u ./userdic/myterm.dic -f utf-8 -t utf-8 ./userdic/converted_pre-dic.csv')
    progress_e_time = time.time()
    progress_i_time = progress_e_time - progress_s_time
    print( '実行時間(duration)：' + str(round(progress_i_time,1)) + "秒" )