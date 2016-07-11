
# -*- coding: utf-8 -*-
import MySQLdb
from MySQLdb import IntegrityError
from MySQLdb import InterfaceError
from MySQLdb import OperationalError 
import sys


class Mysql(object):
    """
    インスタンスを作るとmysqlに接続されます。
    あとはinsertSql(EventList)。
    insertの画面でエラーが出たら多分 intに文字列 とか 文字列に数値 とか YYYY-MM-DD の形になってないとか?
    """

    def __init__(self):

        reload(sys)
        sys.setdefaultencoding('utf-8')
        try:
            self.connector = MySQLdb.connect(host='###', db="l-i-p_test", user='###', passwd='###', charset='utf8')
            print "success"
        except:
            print "fail"

    def insertSql(self, EventList):
        for Event in EventList:
            try:#文字列の中に’があるとき用のエスケープ処理
                print "escape"
                Event.event_name = MySQLdb.escape_string(Event.event_name);
                Event.artist_name = MySQLdb.escape_string(Event.artist_name);
                Event.address = MySQLdb.escape_string(Event.address);
                Event.remarks = MySQLdb.escape_string(Event.remarks);
            except:
                pass
            cursor = self.connector.cursor()
            value = Event.event_name, Event.event_day, Event.day_segment, Event.open_time, Event.start_time, Event.over_time, Event.event_cost, Event.event_cost_int, Event.hall_id, Event.address, Event.artist_name, Event.event_pic, Event.event_url, Event.getted_date, Event.getted_url, Event.remarks
#            sql_insert = "insert into live_test(event_name,event_day,day_segment,open_time,start_time,over_time,event_cost,event_cost_int,hall_id,address,artist_name,event_pic,event_url,getted_date,getted_url,remarks)values('%s','%s',%s,'%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s')" % (value)
            sql_insert = "replace into event(event_name,event_day,day_segment,open_time,start_time,over_time,event_cost,event_cost_int,hall_id,address,artist_name,event_pic,event_url,getted_date,getted_url,remarks)values('%s','%s',%s,'%s','%s','%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s')" % (value)
            print sql_insert
            try:
                cursor.execute(sql_insert)
                print "succees"
                print Event.event_name
            except IntegrityError as e:
                print "追加済み",e
                print Event.event_name
            except OperationalError as e:
                print e
                print Event.event_name
            finally:
                print "========"
            self.connector.commit()

    def classTest(self, EventList):
        for Event in EventList:
            print Event.__dict__
