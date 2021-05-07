import json
import restjson_functions as rest
import asyncio
import time
import math

status = False
myobj = rest.myclass()

async def on_function():
    try:
        data = myobj.receive_restful("4051counter_channel0")
        data = data["Values"][0]["Value"]
    except (TypeError, json.JSONDecodeError):
        print("No or Wrong JSON data")
        return
    except Exception:
        print("generic error, please check")
        return
    if data > 0:
        global status
        if status == False:
            status = True
            t_start = time.time()
        myobj.lightcontrol("towerlight_green")
        myobj.write_restful("4051clear_counter0", 1)
    if status == True:
        t_end = time.time()
    try:
        print(track+t_end-t_start)
        if t_end-t_start > track:
            track = t_end-t_start
    except Exception:
        pass  

async def off_function():
    try:
        data = myobj.receive_restful("4051counter_channel1")
        data = data["Values"][0]["Value"]
    except (TypeError, json.JSONDecodeError):
        print("No or Wrong JSON data")
        return
    except Exception:
        print("generic error, please check")
        return
    global status
    if data > 0:
        if status == True:
            status = False
        myobj.lightcontrol("towerlight_amber")
        myobj.write_restful("4051clear_counter1", 1)
    if status == False:
        print(track)

def main():
    loop = asyncio.get_event_loop()

    while True:
        try:
            loop.run_until_complete(asyncio.gather(on_function(), off_function()))
        except RuntimeError:
            print("RuntimeError")


if __name__ == "__main__":
    main()        