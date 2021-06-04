import time
import asyncio
import json
import restjson_functions as rest
import math

myobj = rest.myclass()

class Buttons:
    def __init__(self):
        # mark the start time down first
        self.time_start = time.time()

    def __del__(self):
        # mark the end time
        self.time_end = time.time()
        self.time_duration = self.time_end - self.time_start
        # print out the duration when the object is destroyed
        print(self.time_duration)
        data = myobj.receive_restful("downtime_red")
        myobj.write_restful("downtime_red", (self.time_duration)+data)


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
        try:
            # initialise the object and start counting time
            buttons = Buttons()
        except Exception:
            pass
        myobj.lightcontrol("towerlight_green")
        myobj.write_restful("4051clear_counter0", 1)


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
    if data > 0:
        myobj.lightcontrol("towerlight_amber")
        myobj.write_restful("4051clear_counter1", 1)
        try:
            del buttons
        except Exception:
            pass


def main():
    loop = asyncio.get_event_loop()

    while True:
        try:
            loop.run_until_complete(asyncio.gather(on_function(), off_function()))
        except RuntimeError:
            print("RuntimeError")


if __name__ == "__main__":
    main()