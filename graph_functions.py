import restjson_functions as rest
import time
import json

myobj = rest.myclass()

class myclass():
    #sensor 1 2 red
    #sensor 3 4 amber
    #sensor 5 6 green
    t_start = time.time()
    const_time = myobj.receive_restful("uptime_total")
    const_time = const_time["Values"][0]["Value"]

    def __init__(self, tag_receive, tag_send):
        self.tag_receive = tag_receive
        self.tag_send = tag_send
        self.counter = False
        self.sensor_start = None
        self.sensor_end = None
        self.sensor_uptime = None
        self.const_time = myobj.receive_restful(self.tag_send)
        self.const_time = self.const_time["Values"][0]["Value"]

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
            if self.counter == False:
                self.sensor_start  = time.time()
                self.counter = True
            self.sensor_end = time.time()
        if self.counter == True:
            self.sensor_uptime = self.sensor_end - self.sensor_start
            if data <= 200:
                self.counter = False
            
            myobj.write_restful(self.tag_send, self.sensor_uptime + self.const_time)
    
    def total(self):
        t_end = None
        t_end = time.time()
        return((t_end-myclass.t_start)+myclass.const_time)

    def datetime(self):
        datetime = []

        datetime.append(time.gmtime()[0])
        datetime.append("-")
        datetime.append(time.gmtime()[1])
        datetime.append("-")
        datetime.append(time.gmtime()[2])
        datetime.append(" ")
        datetime.append(time.gmtime()[3])
        datetime.append(":")
        datetime.append(time.gmtime()[4])
        datetime.append(":")
        datetime.append(time.gmtime()[5])
        datetimeStr = "".join(map(str, datetime))
        
        return datetimeStr