
import MySQLdb


class Mysql(object):

    def __init__(self):
        try:
            self.connector = MySQLdb.connect(host='mysql533.db.sakura.ne.jp', db="l-i-p_live", user='l-i-p', passwd='smzo7gg8', charset='utf8')
            print "success"
        except:
            print "fail"

    def insert_sql(self):
        cursor = self.connect.cursor()
        sql_insert = "insert into auto(name) values('test2')"
        cursor.execute(sql_insert)
        self.connector.commit()
        sql = "select * from auto"
        cursor.execute(sql)
        result = cursor.fetchall()

        for test in result:
            print test

    def classTest(self, EventList):
        for Event in EventList:
            print Event.event_name
        print Event.event_name

    def selectAll(self):
        cursor = self.connect.cursor()
        sql = "select * from auto"
        cursor.execute(sql)
        result = cursor.fetchall()

        for test in result:
            print test
