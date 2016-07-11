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
    mysql = mysql_lip.Mysql()
    print sys.argv[0]

    EventList = []
    url = "http://www.questmusic.co.jp/force/schedule/index.php"
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
    children = bsObj.findAll("table", {"width": "498"})

    for child in children:
        eventClass = Event.Event("h001", url, time, url)
        #　題名  題名は題名が書いてあるロゴのaltに入っているのでそれをみています。ロゴの幅が271であることを利用(対処療法)
        event_name = child.find("img", {"width": "271"})
        eventClass.event_name = event_name["alt"]
#        print event_name["alt"]

        # 日付
        event_day = child.find("td", {"class": "gmenu-s"}).get_text()
        tmp_day = event_day[:8]
        eventClass.event_day = tmp_day.encode('utf-8')
#        print eventClass.event_day
        # 画像
        tmp = child.find("img", alt=re.compile(".*jpg"))
        try:
            img = tmp["alt"]
            getImg(img) 
            tmp_pic = "/home/l-i-p/www/img/"+img
            eventClass.event_pic = tmp_pic.encode('utf-8')
        except:  # 写真がないとき
            pass
        # 開場、開演、前売、当日、ドリンク代
        Inf = child.findAll("td", {"class": "gmenu"})
        eventClass.open_time = Inf[0].get_text().encode('utf-8')
        eventClass.start_time = Inf[1].get_text().encode('utf-8')

        maeuri = Inf[2].get_text()
        drink = Inf[4].get_text()
        tmp_event_cost = "前売:%sドリンク代:%s" % (maeuri, drink)
        eventClass.event_cost = tmp_event_cost.encode('utf-8') 
        tmp_cost_int = search_cost(Inf[3].get_text(), "")
        eventClass.event_cost_int = tmp_cost_int.encode('utf-8')
#        print eventClass.open_time
#        print eventClass.start_time
#        print eventClass.event_cost
#        print eventClass.event_cost_int

        # 問い合わせ
        address = child.find("td", {"class": "txtblock-m border_gray"})
#        print address.get_text()
        eventClass.address = address.get_text().encode('utf-8')

        # アーティストと備考
        txtblock = child.findAll("td", {"class": "border_gray txtblock-m"})
        eventClass.artist_name = txtblock[0].get_text().encode('utf-8')
        eventClass.remarks = txtblock[1].get_text().encode('utf-8')

#        print txtblock[0].get_text()
#        print txtblock[1].get_text()
        EventList.append(eventClass)
    mysql.insertSql(EventList)
