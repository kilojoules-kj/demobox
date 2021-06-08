import json
import math
import restjson_functions as rest
import asyncio
import graph_functions as graph
import os
import psutil
import time

from multiprocessing import Process

myobj = rest.myclass()

async def error_state():
    data = myobj.receive_restful("error_alert")
    if data != 0:
        # basic default display of error
        myobj.lightcontrol("towerlight_red")
        myobj.write_restful("Motor", 0)
        myobj.write_restful("4051clear_counter0", 1)
        myobj.write_restful("4051clear_counter1", 1)
        myobj.write_restful("Clear_counter0", 1)
        myobj.write_restful("Clear_counter1", 1)
        myobj.write_restful("Buzzer", 1)
        
        # this function loops indefinitely until the green button is pressed
        check_loop(time.time(), myobj.receive_restful("downtime_red"))
        # then it return
        
        myobj.write_restful("Buzzer", 0)


def check_loop(t_start, static_time):
    while True:
        try:
            data = myobj.receive_restful("Counter_channel0") # push button
            data2 = myobj.receive_restful("4051counter_channel0") # membrane button

            seconds = math.floor((time.time() - t_start) + static_time)
            minutes = math.floor(seconds/60)
            hours = math.floor(minutes/60)

            myobj.write_restful("downtime_red", seconds)

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
            myobj.write_restful_text("datetime_red", datetimeStr)
        
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
        data = myobj.receive_restful("Counter_channel0") # push button
        data2 = myobj.receive_restful("4051counter_channel0") # membrane button
    except Exception:
        print("generic error, please check")
        return
    if data != 0 or data2 != 0:
        myobj.lightcontrol("towerlight_green")
        myobj.write_restful("Motor", 1)
        myobj.write_restful("Clear_counter0", 1)
    

async def off_function():
    try:
        data = myobj.receive_restful("Counter_channel1") # push button
        data2 = myobj.receive_restful("4051counter_channel1") # membrane button
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
    loop = asyncio.get_event_loop()

    myobj.write_restful("Motor", 0)
    myobj.write_restful("4051clear_counter0", 1)
    myobj.write_restful("4051clear_counter1", 1)
    myobj.write_restful("Clear_counter0", 1)
    myobj.write_restful("Clear_counter1", 1)
    myobj.lightcontrol("towerlight_amber")

    myobj_total = graph.Buttons()

    while True:
        try:
            loop.run_until_complete(asyncio.gather(on_function(), off_function(), temp_error(), dist_error(), error_state()))
        except RuntimeError:
            print("RuntimeError")

        if myobj.receive_restful("s100_tag5") > 200:
            button_on = graph.Buttons("uptime_green", "datetime_green") # for green
        if myobj.receive_restful("s100_tag4") > 200:
            button_off = graph.Buttons("downtime_amber", "datetime_amber") # for amber
        
        myobj_total.total() # get total amount of time the code has been running

        print("current memeory usage: ", psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

if __name__ == "__main__":
    main()