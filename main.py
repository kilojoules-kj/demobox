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
    if data != 0:
        # basic default display of error
        myobj.lightcontrol("towerlight_red")
        myobj.write_restful("Motor", 0)
        myobj.write_restful("Clear_counter0", 1)
        myobj.write_restful("Clear_counter1", 1)
        myobj.write_restful("Buzzer", 1)
        
        # this function loops indefinitely until the green button is pressed
        check_loop(t_start)
        # then it return
        
        myobj.write_restful("Buzzer", 0)


def check_loop(t_start):
    obj1 = graph.storeTime()
    while True:
        try:
            # push button
            data = myobj.receive_restful("Counter_channel0")
            # membrane button
            data2 = myobj.receive_restful("4051counter_channel0")

            t_end = time.time()
            myobj.write_restful("downtime_red", ((t_end - obj1.getTime()) + myobj.receive_restful("downtime_red")))
        except (TypeError, json.JSONDecodeError):
            print("No or Wrong JSON data")
            return
        except Exception:
            print("generic error, please check")
            return
        if data != 0 or data2 != 0:
            myobj.write_restful("error_alert", 0)
            time.sleep(0.3)
            return
        else:
            print("waiting for input")
                    

async def on_function():
    try:
        # push button
        data = myobj.receive_restful("Counter_channel0")
        # membrane button
        data2 = myobj.receive_restful("4051counter_channel0")
    except Exception:
        print("generic error, please check")
        return
    if data != 0 or data2 != 0:
        myobj.lightcontrol("towerlight_green")
        myobj.write_restful("Motor", 1)
        myobj.write_restful("Clear_counter0", 1)
    

async def off_function():
    try:
        # push button
        data = myobj.receive_restful("Counter_channel1")
        # membrane button
        data2 = myobj.receive_restful("4051counter_channel1")
    except Exception:
        print("generic error, please check")
        return
    if data != 0 or data2 != 0:
        myobj.lightcontrol("towerlight_amber")
        myobj.write_restful("Motor", 0)
        myobj.write_restful("Clear_counter1", 1)        


async def temp_error():
    try:
        data = myobj.receive_restful("temperature")
    except Exception:
        print("generic error, please check")
        return
    if data > 29:
        myobj.write_restful("error_alert", 1)


async def dist_error():
    try:
        data = myobj.receive_restful("distance_sensor")
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

        #myobj2.uptime()
        #myobj3.uptime()
        #myobj4.uptime()

        if myobj.receive_restful("s100_tag5") > 200:
            button_on = graph.Buttons("uptime_green", "datetime_green")
        if myobj.receive_restful("s100_tag4") > 200:
            button_off = graph.Buttons("downtime_amber", "datetime_amber")
        if myobj.receive_restful("s100_tag2") > 200:
            button_error = graph.Buttons("downtime_red", "datetime_red")    

        myobj.write_restful("uptime_total", myobj2.total())
        print("current memeory usage: ", psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

if __name__ == "__main__":
    main()
