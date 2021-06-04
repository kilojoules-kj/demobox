import restjson_functions as rest
import time
import json
import math

myobj = rest.myclass()

class myclass():
    #sensor 1 2 red
    #sensor 3 4 amber
    #sensor 5 6 green
    t_start = time.time()
    const_time = myobj.receive_restful("uptime_total")
    const_time = const_time["Values"][0]["Value"]

    def __init__(self, tag_receive, tag_send, tag_datetime = None):
        self.tag_receive = tag_receive
        self.tag_send = tag_send
        self.tag_datetime = tag_datetime
        self.counter = False
        self.sensor_start = None
        self.sensor_end = None
        self.sensor_uptime = None
        self.const_time = None
        self.SEC = None
        self.MIN = None
        self.HR = None

    def uptime(self):
        try:
            data = myobj.receive_restful(self.tag_receive)
            data = data["Values"][0]["Value"]
        except (TypeError, json.JSONDecodeError):
            print("No or Wrong JSON data")
            return
        except Exception:
            print("generic error, please check")
            return
        if data > 200:
            button_on = Buttons("uptime_green", "datetime_green")
            button_off = Buttons("downtime_amber", "datetime_amber")
            button_error = Buttons("downtime_red", "datetime_red")
            

    def total(self):
        t_end = None
        t_end = time.time()
        SEC = math.floor((t_end - myclass.t_start) + myclass.const_time)
        MIN = math.floor(SEC/60)
        HR = math.floor(MIN/60)
        myobj.write_restful_text("datetime_total", myclass.datetime(self, SEC%60, MIN%60, HR))
        return((t_end-myclass.t_start)+myclass.const_time)

    def datetime(self, seconds, minutes, hours):
        datetime = []
        if len(str(hours)) < 2:
            datetime.append("0")
        datetime.append(hours)
        datetime.append(":")
        if len(str(minutes)) < 2:
            datetime.append("0")
        datetime.append(minutes)
        datetime.append(":")
        if len(str(seconds)) < 2:
            datetime.append("0")
        datetime.append(seconds)
        datetimeStr = "".join(map(str, datetime))
        
        return datetimeStr


class Buttons:
    def __init__(self, tag_send, tag_datetime = None):
        self.tag_send = tag_send
        self.tag_datetime = tag_datetime
        # mark the start time down first
        self.time_start = time.time()

    def __del__(self):
        # mark the end time
        self.time_end = time.time()
        self.time_duration = self.time_end - self.time_start
        # print out the duration when the object is destroyed
        print(self.time_duration)
        data = myobj.receive_restful("downtime_red")
        myobj.write_restful(self.tag_send, (self.time_duration)+data)

        const_time = myobj.receive_restful(self.tag_send)
        const_time = self.const_time["Values"][0]["Value"]
        self.SEC = math.floor(self.time_duration + const_time)
        self.MIN = math.floor(self.SEC/60)
        self.HR = math.floor(self.MIN/60)
        myobj.write_restful_text(self.tag_datetime, myclass.datetime(self, self.SEC%60, self.MIN%60, self.HR))