import restjson_functions as rest
import time
import math

myobj = rest.myclass()

class Buttons:
    # object is created
    def __init__(self, tag_send = None, tag_datetime = None):
        self.tag_send = tag_send # this tag is for normal time in seconds
        self.tag_datetime = tag_datetime # this tag is for time converted into datetime format
        self.time_start = time.time() # mark the start time down first

    # object is deleted
    def __del__(self):
        self.time_duration = time.time() - self.time_start # calculate the time that object has been alive
        time_in_seconds = self.time_duration + myobj.receive_restful(self.tag_send) # get normal time

        # convert normal seconds time into bigger units of measurement
        self.SEC = math.floor(time_in_seconds)
        self.MIN = math.floor(self.SEC/60)
        self.HR = math.floor(self.MIN/60)

        try:
            myobj.write_restful(self.tag_send, time_in_seconds) # update the normal time
            myobj.write_restful_text(self.tag_datetime, Buttons.datetime(self, self.SEC%60, self.MIN%60, self.HR)) # update datetime
        except Exception:
            pass

    def total(self):
        t_end = time.time()
        SEC = math.floor((t_end - self.time_start) + myobj.receive_restful("uptime_total"))
        MIN = math.floor(SEC/60)
        HR = math.floor(MIN/60)
        myobj.write_restful("uptime_total", )
        myobj.write_restful_text("datetime_total", Buttons.datetime(self, SEC%60, MIN%60, HR))

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