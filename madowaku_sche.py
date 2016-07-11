
# -*- coding: utf-8 -*-

if __name__ == '__main__':

    from urllib2 import urlopen
    from bs4 import BeautifulSoup
    from urllib2 import HTTPError
    from urllib2 import URLError
    import re

    def search_word(text, pattern):
        try:
            word = re.search(pattern, text).group()
            word = re.search("\d*(:|,)\d*", word).group()
        except:
            word = "NULL"  # 正規表現に引っかからない場合
        return word

    url = "http://madowaku.com/schedule.1606.html"
    try:
        html = urlopen(url)
    except HTTPError as e:  # サーバ落ちた時とかのエラーとか
        print(e)
    except URLError as e:
        print("The server colud not be found")

    bsObj = BeautifulSoup(html, "html.parser")
    children = bsObj.find("tbody").findChildren("tr")
    line = 0
    for child in children:
        event = child.findAll("td")
        event_day_st = event[0].get_text().encode('utf-8')
        if line == 0:
            year_month = event_day_st
            # print year_month
            print "year", re.search("[0-9０-９]*(?=年)", year_month).group()
            print "month", re.search("[0-9０-９]*(?=月)", year_month).group()
            line += 1
            continue
        if line == 1:
            line += 1
            continue

        print "day", re.match("\d*", event_day_st).group()
        if re.match("\d*(\(|（).*(\)|）)", event_day_st) is None:  # 日付フォーマットになってるか確認します　１日に2個イベントあるとき
            print "aaaaa"
            continue

        abstract = event[2].get_text().encode('utf-8')
        # if event[2].find("br") is not None:
        #     print "brtest"
        #     abstract2 = event[2].findAll
        print "abstract", abstract
        detail = event[3].get_text().encode('utf-8')
        print "detail", detail
#  冗長　tables[table,table,table...]tableの中にl三つの<td>段落が入ってるよ。
#    tables = []
#    for table in child:
#        one_table = []
#        for one_tr in table.findAll("tr"):
#            for one_td in one_tr.findAll("td"):
#                one_table.append(one_td)
#        tables.append(one_table)

# 　正規表現置き場
        open_pattern = r"(開場)\d*:\d*"
        start_pattern = r"(開演)\d*:\d*"
        today_cost_pattern = r"(当日)\d*,\d*円"
        pre_cost_pattern = r"(前売)\d*,\d*円"

        open_time = search_word(detail, open_pattern)
        start_time = search_word(detail, start_pattern)
        today_cost = search_word(detail, today_cost_pattern)
        event_cost = search_word(detail, pre_cost_pattern)
        print "題名:",abstract
        print "会場:", open_time, "開演:", start_time, "当日:", today_cost, "前売:", event_cost
        print "============================================"
#    josidoru = 0  # 女子ドルフラグ
#    for table in tables:
#        if josidoru == 0:
#            josidoru = 1
#            continue
#        event_day = table[0].findAll('a')[0].get("name")
#        artist_name = table[0].findAll('a')[1].get_text().encode('utf-8')
#        try:
#            event_name = table[0].findAll("br")[1] \
#            .get_text().encode('utf-8').strip()  # stripはbr削除
#        except:
#            event_name = artist_name  # タイトルがない場合はアーティスト名をタイトルとする
#        print event_day, artist_name, event_name
#        detail = table[2].get_text().encode('utf-8')
#        open_time = search_word(detail, open_pattern)
#        start_time = search_word(detail, start_pattern)
#        today_cost = search_word(detail, today_cost_pattern)
#        event_cost = search_word(detail, pre_cost_pattern)
#        print open_time, start_time, today_cost, event_cost
