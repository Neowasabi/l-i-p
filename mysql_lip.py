
# -*- coding: utf-8 -*-
import MySQLdb
import sys


class Mysql(object):

    def __init__(self):

        reload(sys)
        sys.setdefaultencoding('utf-8')
        try:
            #            self.connector = MySQLdb.connect(host='mysql533.db.sakura.ne.jp', db="l-i-p_live", user='l-i-p', passwd='smzo7gg8', charset='utf8')
            print "success"
        except:
            print "fail"

    def insert_sql(self,EventList):
        for Event in EventList:
            cursor = self.connect.cursor()
            sql_insert = "insert into live_test(event_name,event_day,day_segment,open_time,start_time,over_time,event_cost,event_cost_int,hall_id,address,artist_name,event_pic,event_url,getted_date,getted_url,remarks1)values("+Event.event_name+","+Event.event_day+","+Event.day_segment+","+Event.open_time+","+Event.start_time+","+Event.over_time+","+Event.event_cost+","+Event.event_cost_int+","+Event.hall_id+","+Event.address+","+Event.artist_name+","+Event.event_pic+","+Event.event_url+","+Event.getted_date+","+Event.getted_url+","+Event.remarks+")"

            cursor.execute(sql_insert)
            self.connector.commit()
        sql = "select * from auto"
        cursor.execute(sql)
        result = cursor.fetchall()

        for test in result:
            print test

    def classTest(self, EventList):
        for Event in EventList:
            print Event.__dict__

    def selectAll(self):
        cursor = self.connect.cursor()
        sql = "select * from auto"
        cursor.execute(sql)
        result = cursor.fetchall()

        for test in result:
            print test
