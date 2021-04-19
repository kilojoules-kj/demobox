import restjson_functions as rest
import time

myobj = rest.myclass()

class myclass():
    #sensor 1 2 red
    #sensor 3 4 amber
    #sensor 5 6 green
    t_start = time.time()

    def __init__(self, tag_receive, tag_send):
        self.tag_receive = tag_receive
        self.tag_send = tag_send
        self.counter = 0
        self.sensor_start = None
        self.sensor_end = None
        self.sensor_uptime = None

    def uptime(self):
        try:
            data = myobj.receive_restful(self.tag_receive)
            data = data["Values"]
            #print(data)
            for x in data:
                value = x["Value"]
                if value >= 200:
                    if self.counter != 1:
                        self.sensor_start  = time.time()
                        self.counter = 1
                if self.counter == 1:
                    if value <= 200:
                        self.sensor_end = time.time()
                        self.counter = 0
                        self.sensor_uptime = self.sensor_end - self.sensor_start
                        myobj.write_restful(self.tag_send, self.sensor_uptime)
        except (TypeError):
            print("No or Wrong JSON data")            

    def total(self):
        t_end = None
        t_end = time.time()
        return(t_end-myclass.t_start)
