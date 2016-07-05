
# -*- coding: utf-8 -*-


class Event(object):  # こんなクラスのリストをmysqlに追加するモジュールに投げるとかどうですか
    event_name = None
    event_day = None
    day_segment = None
    open_time = None
    start_time = None
    over_time = None
    event_cost = None
    event_cost_int = None
    hall_id = None
    address = None
    artist_name = None
    event_pic = None
    event_url = None
    getted_date = None
    getted_url = None
    remarks = None

    def introduce(self):
        print self.event_name, self.artist_name
if __name__ == '__main__':

    from urllib2 import urlopen
    from bs4 import BeautifulSoup
    from urllib2 import HTTPError
    from urllib2 import URLError
    import re
    import sys
    import mysql_lip
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

    def search_word(text, pattern):
        try:
            word = re.search(pattern, text).group()
            word = re.search("\d*(:|,)\d*", word).group()
        except:
            word = "NULL"  # 正規表現に引っかからない場合
        try:
            word = int(word.replace(",", ""))
        finally:
            return word

    url = "http://madowaku.com/schedule.1607.html"
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
        eventClass = Event()
        event = child.findAll("td")
        event_day_st = event[0].get_text().encode('utf-8')
        if line == 0:
            year_month = event_day_st
            print "year", re.search("\d*(?=年)", year_month).group()
            print "month", re.search("\d*(?=月)", year_month).group()
            line += 1
            continue
        if re.match("\d*(\(|（).*(\)|）)", event_day_st) is None:  # 日付フォーマットになってるか確認します　１日に2個イベントあるとき
            abstract = event[2].get_text()
            if event[1].find("br") is None:
                event_name = abstract
                artist_name = abstract
            else:
                event_name = event[1].findAll("br")[0].get_text().encode("utf-8")
                # event[2]から題名を消したやつがartist_nameです
                # tagの構造上これしか思いつきませんでした。
                tmp = event[1].get_text()
                artist_name = tmp.replace(event_name, "").encode("utf-8")

                detail = event[2].get_text().encode('utf-8')
                open_time = search_word(detail, open_pattern)
                start_time = search_word(detail, start_pattern)
                today_cost = search_word(detail, today_cost_pattern)
                event_cost = search_word(detail, pre_cost_pattern)

                print "day", re.match("\d*", event_day_st).group()
                print "題名:", event_name
                print "アーティスト", artist_name
                print "会場:", open_time, "開演:", start_time, "当日:", today_cost, "前売:", event_cost
                print "============================================"
#  こっちでクラスの変数に代入できなかった
#                setattr(eventClass, artist_name, artist_name)
#                setattr(eventClass, event_name, event_name.strip())
#                setattr(eventClass, open_time, open_time)
#                setattr(eventClass, start_time, start_time)
#                setattr(eventClass, today_cost, today_cost)
#                setattr(eventClass, event_cost, event_cost)
                eventClass.artist_name = artist_name
                eventClass.event_name = event_name.strip()
                eventClass.open_time = open_time
                eventClass.start_time = start_time
                eventClass.today_cost = today_cost
                eventClass.event_cost = event_cost

                print eventClass.event_name
                EventList.append(eventClass)
            continue

        abstract = event[2].get_text().encode('utf-8')
        if event[2].find("br") is None:
            event_name = abstract
            artist_name = abstract
        else:

            event_name = event[2].findAll("br")[0].get_text().encode('utf-8')
            # event[2]から題名を消したやつがartist_nameです
            # tagの構造上これしか思いつきませんでした。
            tmp = event[2].get_text()
            artist_name = tmp.replace(event_name, "")

        detail = event[3].get_text().encode('utf-8')
        open_time = search_word(detail, open_pattern)
        start_time = search_word(detail, start_pattern)
        today_cost = search_word(detail, today_cost_pattern)
        event_cost = search_word(detail, pre_cost_pattern)

        print "day", re.match("\d*", event_day_st).group()
        print "題名:", event_name.strip()
        print "アーティスト", artist_name
        print "会場:", open_time, "開演:", start_time, "当日:", today_cost, "前売:", event_cost
        print "============================================"
#  こっちでクラスの変数に代入できませんでした
#        setattr(eventClass, artist_name, artist_name)
#        setattr(Event, event_name, event_name.strip())
#        setattr(eventClass, artist_name, artist_name)
#        setattr(eventClass, open_time, open_time)
#        setattr(eventClass, open_time, open_time)
#        setattr(eventClass, start_time, start_time)
#        setattr(eventClass, today_cost, today_cost)
#        setattr(eventClass, event_cost, event_cost)

        eventClass.artist_name = artist_name
        eventClass.event_name = event_name.strip()
        eventClass.open_time = open_time
        eventClass.start_time = start_time
        eventClass.today_cost = today_cost
        eventClass.event_cost = event_cost
        print eventClass.event_name
        EventList.append(eventClass)
#    mysql.classTest(EventList)
