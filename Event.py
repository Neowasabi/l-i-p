# -*- coding: utf-8 -*-
class Event(object):
    """
インスタンス変数に取ってきた情報を突っ込んであげてください。
時間系の型はnullではなくとりあえず00:00を突っ込んでいます。(NULLが使えない)
    """

    def __init__(self, hall_id, event_url, getted_date, getted_url):
        # ここには取ってきたイベントの情報を
        self.event_name = "null"
        self.event_day = "00010101"  # YYYY-MM-DD
        self.day_segment = "null"
        self.open_time = "00:00"  # HH:MM
        self.start_time = "00:00"  # HH:MM
        self.over_time = "00:00"  # HH:MM
        self.event_cost = "null"
        self.event_cost_int = "null"
        self.address = "null"
        self.artist_name = "null"
        self.event_pic = "null"
        self.remarks = "null"
        # ここはライブハウスごとの情報を
        self.hall_id = hall_id
        self.event_url = event_url
        self.getted_date = getted_date
        self.getted_url = getted_url
