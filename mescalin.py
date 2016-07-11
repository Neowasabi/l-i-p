# -*- coding: utf-8 -*-
from urllib2 import urlopen
import urllib2
from bs4 import BeautifulSoup
from urllib2 import HTTPError
from urllib2 import URLError

import re
import os
import sys
import time

import Event
import mysql_lip
# 　正規表現置き場
open_pattern = r"(開場)\d*:\d*"
start_pattern = r"(開演)\d*:\d*"
today_cost_pattern = r"(当日)\d*,\d*円"
pre_cost_pattern = r"(前売)\d*,\d*円"


def search_time(text, pattern):
    try:
        word = re.search(pattern, text).group()
        word = re.search("\d*\:\d*", word).group()
    except:
        word = "00:00"  # 正規表現に引っかからない場合
    return word


def search_cost(text, pattern):
    try:
        #        word = re.search(pattern, text).group()
        word = re.search("\d*\,\d*", text).group()
        word = word.replace(",", "")  # 値段のカンマ取り除いてます。
    except:
        word = "null"  # 正規表現に引っかからない場合
    return word


def getImg(url):
    print os.getcwd()
#    print os.chdir('./Scraping/img/')
    print os.chdir('./../www/img/')
    # print os.getcwd()
    localfile = open(os.path.basename(url), 'wb')
    img_url = "http://www.questmusic.co.jp/force/up_image/" + url
    print "test", img_url
    img = urllib2.urlopen(img_url)
    localfile.write(img.read())
    localfile.close()
    print os.chdir('../../')
if __name__ == '__main__':
    # timeStamp
    format = "%Y-%m-%d"
    time = time.strftime(format)
    # mysql
#    mysql = mysql_lip.Mysql()
    print sys.argv[0]

    EventList = []
    url = "http://mescalin-drive.com/schedule//201607/02.html"
    try:
        html = urlopen(url)
    except HTTPError as e:  # サーバ落ちた時とかのエラーとか
        print(e)
    except URLError as e:
        print("The server colud not be found")

    bsObj = BeautifulSoup(html, "html.parser")
    """
    木構造になっていない。対処療法として幅が498のtableを一つのイベントとします
    ↓↓↓
    """
