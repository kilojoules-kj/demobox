import json
import restjson_functions as rest
import asyncio
import graph_functions as graph
import os
import psutil
import tkinter 
import tkinter.tix as tix
import tkinter.messagebox as messagebox
import time

from multiprocessing import Process

myobj = rest.myclass()

async def error_state():
    t_start = time.time()
    data = myobj.receive_restful("error_alert")
    data = data["Values"][0]["Value"]
    if data != 0:
        myobj.lightcontrol("towerlight_red")
        myobj.write_restful("Motor", 0)
        myobj.write_restful("Clear_counter0", 1)
        myobj.write_restful("Clear_counter1", 1)
        myobj.write_restful("Buzzer", 1)
        check_loop()
        t_end = time.time()
        myobj.write_restful("Buzzer", 0)
        data = myobj.receive_restful("downtime_red")
        data = data["Values"][0]["Value"]
        myobj.write_restful("downtime_red", (t_end-t_start)+data)
        

async def on_function():
    try:
        data = myobj.receive_restful("Counter_channel0")
        data = data["Values"][0]["Value"]
    except (TypeError, json.JSONDecodeError):
        print("No or Wrong JSON data")
        return
    except Exception:
        print("generic error, please check")
        return
    if data > 0:
        myobj.lightcontrol("towerlight_green")
        myobj.write_restful("Motor", 1)
        myobj.write_restful("Clear_counter0", 1)
    
async def off_function():
    try:
        data = myobj.receive_restful("Counter_channel1")
        data = data["Values"][0]["Value"]
    except (TypeError, json.JSONDecodeError):
        print("No or Wrong JSON data")
        return
    except Exception:
        print("generic error, please check")
        return
    if data > 0:
        myobj.lightcontrol("towerlight_amber")
        myobj.write_restful("Motor", 0)
        myobj.write_restful("Clear_counter1", 1)        

def check_loop():
    while True:
        try:
            data = myobj.receive_restful("Counter_channel0")
            data = data["Values"][0]["Value"]
        except (TypeError, json.JSONDecodeError):
            print("No or Wrong JSON data")
            return
        except Exception:
            print("generic error, please check")
            return
        if data > 0:
            myobj.write_restful("error_alert", 0)
            time.sleep(0.3)
            return
        else:
            print("waiting for input")
        
async def temp_error():
    try:
        data = myobj.receive_restful("temperature")
        data = data["Values"][0]["Value"]
    except (TypeError, json.JSONDecodeError):
        print("No or Wrong JSON data")
        return
    except Exception:
        print("generic error, please check")
        return
    if data > 29:
        myobj.write_restful("error_alert", 1)
          
async def dist_error():
    try:
        data = myobj.receive_restful("distance_sensor")
        data = data["Values"][0]["Value"]
    except (TypeError, json.JSONDecodeError):
        print("No or Wrong JSON data")
        return
    except Exception:
        print("generic error, please check")
        return
    if data > 600:
        myobj.write_restful("error_alert", 1)

def main():
    myobj2 = graph.myclass("s100_tag5", "uptime_green", "datetime_green")
    myobj3 = graph.myclass("s100_tag4", "downtime_amber", "datetime_amber")
    myobj4 = graph.myclass("s100_tag2", "downtime_red", "datetime_red")

    loop = asyncio.get_event_loop()

    myobj.write_restful("Motor", 0)
    myobj.write_restful("Clear_counter0", 1)
    myobj.write_restful("Clear_counter1", 1)
    myobj.lightcontrol("towerlight_amber")

    while True:
        try:
            loop.run_until_complete(asyncio.gather(on_function(), off_function(), temp_error(), dist_error(), error_state()))
        except RuntimeError:
            print("RuntimeError")

        myobj2.uptime()
        myobj3.uptime()
        myobj4.uptime()
        myobj.write_restful("uptime_total", myobj2.total())
        print("current memeory usage: ", psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

if __name__ == "__main__":
    main()
    #P1 = Process(target=main)
    #P2 = Process(target=display)
    #P1.start()
    #P2.start()
    #P1.join()
    #P2.join()
