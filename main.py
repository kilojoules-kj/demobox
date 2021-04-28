import json
import restjson_functions as rest
import asyncio
import graph_functions as graph
import os
import psutil
import tkinter 
import tkinter.tix as tix
import tkinter.messagebox as messagebox

from multiprocessing import Process

myobj = rest.myclass()

async def error_state():
    data = myobj.receive_restful("error_alert")
    data = data["Values"][0]["Value"]
    if data != 0:
        myobj.lightcontrol("towerlight_red")
        myobj.write_restful("Motor", 0)
        myobj.write_restful("Clear_counter0", 1)
        myobj.write_restful("Clear_counter1", 1)
        myobj.write_restful("Buzzer", 1)
        check_loop()
        myobj.write_restful("Buzzer", 0)

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
            return
        else:
            print("waiting")
        
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
    myobj2 = graph.myclass("s100_tag5", "uptime_green")
    myobj3 = graph.myclass("s100_tag4", "downtime_amber")
    myobj4 = graph.myclass("s100_tag2", "downtime_red")

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
        myobj.write_restful("datetime", myobj2.datetime())
        print("current memeory usage: ", psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)

def display():
    def setPlace(window,x, y,w=0,h=0):
        if (w==0  or  h==0):
            w = window.winfo_width() #Get window width (unit: pixel)
            h = window.winfo_height() #Get window height (unit: pixel)
        window.geometry('{}x{}+{}+{}'.format(w, h, x, y))

    def RunSample(w):
        top = tix.Label(w, padx=20, pady=10, bd=1, relief=tix.RAISED, anchor=tix.CENTER, text='This box controls the functions for the demo box')
        box = tix.ButtonBox(w)
    
        myobj = rest.myclass()
        
        def digital_on_function():
            myobj.lightcontrol("towerlight_green")
            myobj.write_restful("Motor", 1)
            myobj.write_restful("Clear_counter0", 1)

        def digital_off_function():
            myobj.lightcontrol("towerlight_amber")
            myobj.write_restful("Motor", 0)
            myobj.write_restful("Clear_counter1", 1)    

        """ def quit():
            ans=messagebox.askyesno('Tk.messagebox prompt','Do you want to end the program?') #OK/Cancel, return value True/False
            if ans==True:
                w.destroy()   """
        
        box.add('on', text='On', underline=0, width=5,
            command=digital_on_function)
        box.add('off', text='Off', underline=0, width=5,
            command=digital_off_function)    
        box.pack(side=tix.BOTTOM, fill=tix.X)
        top.pack(side=tix.TOP, fill=tix.BOTH, expand=1)

    root = tix.Tk()
    RunSample(root)
    top=tix.Toplevel(root)
    root.update()
    root.title('Tix.ButtonBox Demo') #Method of setting window title in Tkinter
    setPlace(root,100,100)
    top.title('Tix.ButtonBox Demo') #Method of setting window title in Tkinter
    setPlace(top,100,300)

    def helloCallBack():
        print("Hello World")

    root.mainloop()

if __name__ == "__main__":
    main()
    #P1 = Process(target=main)
    #P2 = Process(target=display)
    #P1.start()
    #P2.start()
    #P1.join()
    #P2.join()
