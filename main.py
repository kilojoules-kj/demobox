import json
import restjson_functions as rest
import asyncio
import graph_functions as graph
import os
import psutil

myobj = rest.myclass()

""" class main_class():
    def __init__(self):
        myobj.write_restful("Clear_counter0", 1)
        myobj.write_restful("Clear_counter1", 1)
        myobj.lightcontrol("towerlight_amber")
        myobj.write_restful("Motor", 0) """

#start up
myobj.write_restful("Clear_counter0", 1)
myobj.write_restful("Clear_counter1", 1)
myobj.lightcontrol("towerlight_amber")
myobj.write_restful("Motor", 0)

async def keep_alive():
    print("running")

async def on_function():
    try:
        data = myobj.receive_restful("Counter_channel1")
        data = data["Values"]
    except (TypeError, json.JSONDecodeError):
        print("No or Wrong JSON data")
        return
    except Exception:
        print("generic error, please check")
        return
    for x in data:
        if x["Value"] > 0:
            myobj.lightcontrol("towerlight_green")
            myobj.write_restful("Motor", 1)
            myobj.write_restful("Clear_counter1", 1)
    
async def off_function():
    try:
        data = myobj.receive_restful("Counter_channel0")
        data = data["Values"]
    except (TypeError, json.JSONDecodeError):
        print("No or Wrong JSON data")
        return
    except Exception:
        print("generic error, please check")
        return
    for x in data:
        if x["Value"] > 0:
            myobj.lightcontrol("towerlight_amber")
            myobj.write_restful("Motor", 0)
            myobj.write_restful("Clear_counter0", 1)        

def check_loop():
    while True:
        try:
            data = myobj.receive_restful("Counter_channel1")
            data = data["Values"]
        except (TypeError, json.JSONDecodeError):
            print("No or Wrong JSON data")
            return
        except Exception:
            print("generic error, please check")
            return
        for x in data:
            if x["Value"] > 0:
                return
            else:
                print("waiting")
        
async def temp_error():
    try:
        data = myobj.receive_restful("temperature")
        data = data["Values"]
    except (TypeError, json.JSONDecodeError):
        print("No or Wrong JSON data")
        return
    except Exception:
        print("generic error, please check")
        return
    for x in data:
        value = x["Value"]
        if value > 29:
            myobj.lightcontrol("towerlight_red")
            myobj.write_restful("Motor", 0)
            myobj.write_restful("Clear_counter0", 1)
            myobj.write_restful("Clear_counter1", 1)
            myobj.write_restful("Buzzer", 0)
            check_loop()
            myobj.write_restful("Buzzer", 1)
        
async def dist_error():
    try:
        data = myobj.receive_restful("distance_sensor")
        data = data["Values"]
    except (TypeError, json.JSONDecodeError):
        print("No or Wrong JSON data")
        return
    except Exception:
        print("generic error, please check")
        return
    for x in data:
        value = x["Value"]
        if value > 600:
            myobj.lightcontrol("towerlight_red")
            myobj.write_restful("Motor", 0)
            myobj.write_restful("Clear_counter0", 1)
            myobj.write_restful("Clear_counter1", 1)
            myobj.write_restful("Buzzer", 0)
            check_loop()
            myobj.write_restful("Buzzer", 1)
        
loop = asyncio.get_event_loop()

myobj2 = graph.myclass("s100_tag5", "uptime_green")
myobj3 = graph.myclass("s100_tag4", "downtime_amber")
myobj4 = graph.myclass("s100_tag2", "downtime_red")

while True:
    try:
        loop.run_until_complete(asyncio.gather(on_function(), off_function(), temp_error(), dist_error()))
    except RuntimeError:
        print("RuntimeError")
    myobj2.uptime()
    myobj3.uptime()
    myobj4.uptime()
    myobj.write_restful("uptime_total", myobj2.total())
    #myobj.write_restful("datetime", myobj2.datetime())
    print("current memeory usage: ", psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
