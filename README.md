## DemoBox

Description:

First project in internship. Basic button control to start and stop motor. Connect to advantech webaccess for backend. Use rest api or mqtt to retrieve and write data. Connect thermocouple and distance sensor. Implement a error state that trigger if thermocouple or distance sensor is out of range.

=================================================

#This documentation will document all the functions in the script and how the script is ran to accomplish its task.
#The goal is to send control signals to motor through Advantech WebAccess and do some background calculations.

===========================================

**restjson_functions.py**:
The most important file aside from main.py, this file contains the class and member functions needed to establish REST api. It imports json and requests.

Class `myclass` contains all the member functions related to REST api.
When initialising an object of `myclass`, the object will have a default `self.header` that is set to authenticate for WebAccess. It is possible to modify the header to anything else.

The dictionary `led_status` is to keep check of all the lights with respectively keys corresponding to the tag name set in WebAccess

Member functions:
- *lightcontrol(self, name)*
This function controls the lights by setting all values in led_status to 0, then 1 to the value of the key specified by user. It loops the size of led_status and calls the REST function to send the control signal to WebAccess. 
To call, a string argument of 'name' must be passed, this 'name' has to be one of the key defined in led_status. Whichever 'name' is passed into the argument will be the light that is switched on.
Usage Example: lightcontrol(self, 'towerlight_green')

- *receive_restful(self, name)*
This function is a REST api call. POST requires a body of JSON or XML to format the response. It will return the resulting response in JSON unless there is an error.
To call,  a string argument of 'name' must be passed, this 'name' should correspond to a tag that is set in WebAccess. 
Usage Example: receive_restful(self, 'Counter_channel0')

- *write_restful(self, name, value)*
This function is a REST api call. POST requires a body of JSON or XML to format the reponse. It will set the value of the tag specified to 'value' in the argument unless there is an error.
To call, a string argument of 'name' and a numerical argument of 'value' must be passed, this 'name' should correspond to a tag that is set in WebAccess.
Usage Example: write_restful(self, 'Motor', 1)

- *write_restful_text(self, name, string)*
This function is a REST api call. POST requires a body of JSON or XML to format the reponse. It will set the string value of the tag specified to 'string' in the argument unless there is an error.
To call, a string argument of 'name' and a string argument of 'string' must be passed, this 'name' should correspond to a tag that is set in WebAccess.
Usage Example: write_restful_text(self, 'datetime', 'just a string')

=========================================

**graph_functions.py**:
This file contain member functions and variables related to graphing. It imports json, time and restjson_functions.

'myobj' is an object of class 'myclass' from restjson_functions.py

Class 'myclass' contains all the member functions related to calculation of uptime and date.
To create an object of myclass, 2 arguments must be passed, 'tag_receive' and 'tag_send'. These tags are to specify which tag to read from and write to, 'tag_receive' will read from tag, 'tag_send' will write to tag, 'tag_datetime' is optional unless provided will write string to tag.
When initialising an object of myclass, the object have self.tag_receive, self.tag_send, self.tag_datetime, self.counter = False and self.sensor_start, self.sensor.end, self.sensor_uptime, self.const_time, self.HR, self.MIN, self.SEC set to = None. 
It is recommended that the attributes be left untouched.
AFter the object is created, 't_start' = time.time() is run to mark down the time that the object is created.

Member functions:
- *uptime(self)*
This function will read the value that is in 'tag_receive' from receive_restful and calculate the sensor uptime. 
After it gets value from the JSON reponse, it compares value to 200, 200 is the decided sensor threshold for led On or Off, above 200 and led is on, below 200 and led is off. 
First, it determine the start by checking that value is above 200.
If value is above 200, check self.counter == False, set self.sensor_end, calculate self.sensor_uptime, set self.SEC = self.sensor_uptime + self.const_time, calculate self.MIN, calculate self.HR, pass SEC MIN HR into datetime(), POST results from datetime() into tag. If not <200, set self.counter = False
If self.counter is False, set self.sensor_start, flip the self.counter to True, get self.const_time.
Call as usual
Usage Example: uptime()

- *total(self)*
This function determines the total amount run time since program start and return the amount of time.
Everytime main program runs a loop, this function is ran and 't_end' is updated.
Calculate SEC by 't_end' - 'myclass.t_start' + myclass.const_time. Calculate MIN by SEC/60. Calculate HR by MIN/60
Call datetime() and pass SEC, MIN, HR
Write to 'datetime_total' and return SEC.
Call as usual
Usage Example: total()

- *datetime()*
This function gets format data into datetime format for graphs then return it.
It create an array 'datetime', append the time char and date char into the array and joins the char into a string. 
To call, 3 numerical arguments must be passed.
Usage Example: datetime(20,20,20)

================================================

**main.py**:
This file contains the main functionalities of the program as well as background processes. It imports json, asyncio, os, psutil, tkinter, tkinter.tix, tkinter.messagebox and multiprocessing.
It also import the 2 libraries that was custom made, restjson_functions and graph_functions.
This program is run asynchronously to allow for concurrency.

'myobj' is an object of class 'myclass' from restjson_functions.py

Functions:
- *error_state()*
This is the function that will be triggered if a sensor value passes its safety threshold. It read value from 'error_alert' via receive_restful. 
If value is not 0, turn towerlight to red, turn off the motor, clear the input counters, sound the buzzer and run a infinite loop, check_loop().
Once check_loop() return and the function can continue, turn off the buzzer.
Call as usual
Usage Example: error_state()

- *on_function()*
This function reads value from 'Counter_channel0' via receive_restful and check if value is > 0.
Turn towerlight to green, turn on motor and clear input counter channel 0.
Call as usual
Usage Example: on_function()

- *off_function()*
This function reads value from 'Counter_channel1' via receive_restful and check if value is > 0.
Turn towerlight to amber, turn off motor and clear counter channel 1.

- *check_loop()*
This function will only be triggered by another function for error checking. 
This is a loop that run infinitely and read from 'Counter_channel0' until it detects 'Counter_channel0' > 0.
If value > 0, set 'error_alert' to 1 via write_restful and return.
Call as usual
Usage Example: check_loop()

- *temp_error()*
This function reads value from 'temperature' via receive_restful and check if value > 29.
29 is the decided threshold for the thermocouple. 
If value > 29, set 'error_alert' to 1 via write_restful.
Call as usual
Usage example: temp_error()

- *dist_error()*
This function reads value from 'distance_sensor' via receive_restful and check if value < 600.
600 is the decided threshold for the distance sensor 
If value < 600, set 'error_alert' to 1 via write_restful.
Call as usual
Usage example: dist_error()

- *main()*
This function contains the essentials including creation of objects and asyncio loop.

'myobj2' is an object of class 'myclass' from graph_functions.py
'myobj3' is an object of class 'myclass' from graph_functions.py
'myobj4' is an object of class 'myclass' from graph_functions.py
Create 3 objects for each of the towerlight colours, green, amber, red. 
Pass the arguments for 'tag_receive' corresponding sensor tag that measures the led, 'tag_send' corresponding tag to store the values., 'tag_datetime' corresponding tag to store string values.

'loop' is a asyncio loop which will execute the asynchronous coroutine at once. 

Run startup protocol.
Reset both input counters to 0, make sure the motor is off and start the twoerlight at amber.

Create a infinite loop and run the asyncio loop.
myobj2.uptime() is for uptime of green led.
myobj3.uptime() is for uptime of amber led.
myobj4.uptime() is for uptime of red led.
Update total run time and datetime.
Print the current amount of memory that is being used by the program.

=========================================================================

deprecated stuff:

- *display()*
This function was originally meant to create virtual buttons using tkinter but it is now deprecated after the switch to Angular.

multiprocessing:
Initally, multiprocessing is required for the main loop and the virtual buttons loop to run at the same time. But it is no longer needed.
