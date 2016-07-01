# -*- coding: utf-8 -*-
from urllib2 import urlopen
import urllib2
from bs4 import BeautifulSoup
from urllib2 import HTTPError
from urllib2 import URLError
import re
import os
import sys

def search_word(text, pattern):
		try:
			word = re.search(pattern, text).group()
			word = re.search("\d*(:|,)\d*", word).group()
		except:
			word = "NULL"  # 正規表現に引っかからない場合
		return word

def getImg(url):
		print os.getcwd()
		print os.chdir('./Scraping/img/')
		# print os.getcwd()
		localfile = open(os.path.basename(url),'wb')
		img_url = "http://madowaku.com/"+ url
		img = urllib2.urlopen(img_url)
		localfile.write(img.read())
		localfile.close()
		print os.chdir('../../')

if __name__ == '__main__':
	print sys.argv[0]

	url = "http://madowaku.com/infomation.html"
	try:
		html = urlopen(url)
	except HTTPError as e:  # サーバ落ちた時とかのエラーとか
		print(e)
	except URLError as e:
		print("The server colud not be found")

	bsObj = BeautifulSoup(html, "html.parser")
	child = bsObj.find("center").findChildren("table")

	#  冗長　tables[table,table,table...]tableの中に三つの<td>段落が入ってるよ。
	tables = []
	for table in child:
		one_table = []
		for one_tr in table.findAll("tr"):
			for one_td in one_tr.findAll("td"):
				one_table.append(one_td)
		tables.append(one_table)

	# 　正規表現置き場
	open_pattern = r"(開場)\d*:\d*"
	start_pattern = r"(開演)\d*:\d*"
	today_cost_pattern = r"(当日)\d*,\d*円"
	pre_cost_pattern = r"(前売)\d*,\d*円"

	josidoru = 0  # 女子ドルフラグ
	for table in tables:
		if josidoru == 0:
			josidoru = 1
			continue
		try:
			event_day = table[0].findAll('a')[0].get("name")
			artist_name = table[0].findAll('a')[1].get_text().encode('utf-8')
			event_name = table[0].findAll("br")[1] \
			.get_text().encode('utf-8').strip()  # stripはbr削除
		except:
			event_name = artist_name  # タイトルがない場合はアーティスト名をタイトルとする
		print event_day, artist_name, event_name
		artist_name = table[0].findAll('br')[0].get_text().encode('utf-8').strip()
		img = table[1].find('img').get("src")
		print "imgtest", img
		getImg(img)
		try:
			event_name = table[0].findAll("br")[1] \
				.get_text().encode('utf-8').strip()  # stripはbr削除
		except:
			event_name = artist_name  # タイトルがない場合はアーティスト名をタイトルとする
		print event_day, "artist_name:", artist_name, "event_name:", event_name
		detail = table[2].get_text().encode('utf-8')
		open_time = search_word(detail, open_pattern)
		start_time = search_word(detail, start_pattern)
		today_cost = search_word(detail, today_cost_pattern)
		event_cost = search_word(detail, pre_cost_pattern)
		print open_time, start_time, today_cost, event_cost
		print ""
