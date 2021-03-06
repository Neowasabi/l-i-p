
# -*- coding: utf-8 -*-

if __name__ == '__main__':

    from urllib2 import urlopen
    from bs4 import BeautifulSoup
    from urllib2 import HTTPError
    from urllib2 import URLError
    import re
    import sys
    import time
    import mysql_lip
    import Event
    reload(sys)
    sys.setdefaultencoding("utf-8")
    mysql = mysql_lip.Mysql()
# 　正規表現置き場
    open_pattern = r"(開場)\d*:\d*"
    start_pattern = r"(開演)\d*:\d*"
    today_cost_pattern = r"(当日)\d*,\d*円"
    pre_cost_pattern = r"(前売)\d*,\d*円"

#  EventList
    EventList = []
#timeStamp
    format = "%Y-%m-%d"
    time = time.strftime(format)

    def search_time(text, pattern):
        try:
            word = re.search(pattern, text).group()
            word = re.search("\d*\:\d*", word).group()
        except:
            word = "00:00"  # 正規表現に引っかからない場合
        return word

    def search_cost(text, pattern):
        try:
            word = re.search(pattern, text).group()
            word = re.search("\d*\,\d*", word).group()
            word = word.replace(",", "")  # 値段のカンマ取り除いてます。
        except:
            word = "null"  # 正規表現に引っかからない場合
        return word

    date = "1607"  # 後に引数でもらう
    year = date[:2]
    month = date[2:]
    url = "http://madowaku.com/schedule." + date + ".html"
    try:
        html = urlopen(url)
    except HTTPError as e:  # サーバ落ちた時とかのエラーとか
        print(e)
    except URLError as e:
        print("The server colud not be found")

    bsObj = BeautifulSoup(html, "html.parser", from_encoding='utf-8')
    children = bsObj.find("tbody").findChildren("tr")
    line = 0
    for child in children:
        eventClass = Event.Event("h000", url, time, url)
        event = child.findAll("td")
        event_day_st = event[0].get_text().encode('utf-8')
        if line == 0:  # 最初の行はスルー
            year_month = event_day_st
            print "year", re.search("\d*(?=年)", year_month).group()
            print "month", re.search("\d*(?=月)", year_month).group()
            line += 1
            continue

        if re.match("\d*(\(|（).*(\)|）)", event_day_st) is None:  # 日付フォーマットになってるか確認します　１日に2個イベントあるとき
            event_day_st = re.search("\d*", event_day_st).group()
            abstract = event[2].get_text()
            if event[1].find("br") is None:  # 一行しかないイベント
                event_name = abstract
                artist_name = abstract
            else:
                event_name = event[1].findAll("br")[0].get_text().encode("utf-8")
                # event[2]から題名を消したやつがartist_nameです
                # tagの構造上これしか思いつきませんでした。
                tmp = event[1].get_text()
                artist_name = tmp.replace(event_name, "").encode("utf-8")

                detail = event[2].get_text().encode('utf-8')
                open_time = search_time(detail, open_pattern)
                start_time = search_time(detail, start_pattern)
                today_cost = search_cost(detail, today_cost_pattern)
                event_cost = search_cost(detail, pre_cost_pattern)
# デバッグ用
#                print "day", re.match("\d*", event_day_st).group()
#                print "題名:", event_name
#                print "アーティスト", artist_name
#                print "会場:", open_time, "開演:", start_time, "当日:", today_cost, "前売:", event_cost
#                print "============================================"
                if len(event_day_st) == 1:
                    eventClass.event_day = "20" + year + "-" + month + "-0" + event_day_st
                else:
                    eventClass.event_day = "20" + year + "-" + month + "-" + event_day_st
                tmp = event_name.strip()
                eventClass.event_name = tmp.strip("'")
                eventClass.artist_name = artist_name
                eventClass.open_time = open_time
                eventClass.start_time = start_time
                eventClass.event_cost_int = today_cost
                eventClass.event_cost = event_cost
                eventClass.remarks = detail

                print eventClass.event_name
                EventList.append(eventClass)
            continue

        event_day_st = re.search("\d*", event_day_st).group()
        abstract = event[2].get_text().encode('utf-8')
        if event[2].find("br") is None:  # 一行しかないイベント
            event_name = abstract
            artist_name = abstract
        else:

            event_name = event[2].findAll("br")[0].get_text().encode('utf-8')
            # event[2]から題名を消したやつがartist_nameです
            # tagの構造上これしか思いつきませんでした。
            tmp = event[2].get_text()
            artist_name = tmp.replace(event_name, "")

        detail = event[3].get_text().encode('utf-8')
        open_time = search_time(detail, open_pattern)
        start_time = search_time(detail, start_pattern)
        today_cost = search_cost(detail, today_cost_pattern)
        event_cost = search_cost(detail, pre_cost_pattern)
# デバッグ用
#        print "day", re.match("\d*", event_day_st).group()
#        print "題名:", event_name.strip()
#        print "アーティスト", artist_name
#        print "会場:", open_time, "開演:", start_time, "当日:", today_cost, "前売:", event_cost
#        print "============================================"
        if len(event_day_st) == 1:
            eventClass.event_day = "20" + year + "-" + month + "-0" + event_day_st
        else:
            eventClass.event_day = "20" + year + "-" + month + "-" + event_day_st
        eventClass.artist_name = artist_name.encode('utf-8')
        tmp = event_name.strip()
        eventClass.event_name = tmp.strip("'")
        eventClass.open_time = open_time
        eventClass.start_time = start_time
        eventClass.event_cost_int = today_cost
        eventClass.event_cost = event_cost
        eventClass.remarks = detail
        EventList.append(eventClass)
    mysql.insertSql(EventList)
