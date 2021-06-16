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

The dictionary `led_status` is to keep check of all the lights with respectively keys corresponding to the tag name set in WebAccess.

Member functions:
- `lightcontrol(self, name)`
This function controls the lights by setting all values in led_status to 0, then 1 to the value of the key specified by user. It loops the size of led_status and calls the REST function to send the control signal to WebAccess. 
To call, a string argument of 'name' must be passed, this 'name' has to be one of the key defined in led_status. Whichever 'name' is passed into the argument will be the light that is switched on.
Usage Example: lightcontrol(self, 'towerlight_green')

- `receive_restful(self, name)`
This function is a REST api call. POST requires a body of JSON or XML to format the response. It will return the resulting response in JSON unless there is an error.
To call,  a string argument of 'name' must be passed, this 'name' should correspond to a tag that is set in WebAccess. 
Usage Example: receive_restful(self, 'Counter_channel0')

- `write_restful(self, name, value)`
This function is a REST api call. POST requires a body of JSON or XML to format the reponse. It will set the value of the tag specified to 'value' in the argument unless there is an error.
To call, a string argument of 'name' and a numerical argument of 'value' must be passed, this 'name' should correspond to a tag that is set in WebAccess.
Usage Example: write_restful(self, 'Motor', 1)

- `write_restful_text(self, name, string)`
This function is a REST api call. POST requires a body of JSON or XML to format the reponse. It will set the string value of the tag specified to 'string' in the argument unless there is an error.
To call, a string argument of 'name' and a string argument of 'string' must be passed, this 'name' should correspond to a tag that is set in WebAccess.
Usage Example: write_restful_text(self, 'datetime', 'just a string')

=========================================

**graph_functions.py**:
This file contain member functions and variables related to graphing. It imports json, time and restjson_functions.

`myobj` is an object of class `myclass` from restjson_functions.py

Class `Buttons` contains all the member functions related to calculation of uptime and date.
The class will store a value of total_time when ran at the beginning.
To create an object of `Buttons`, 2 arguments must be passed, 'tag_send' and 'tag_datetime'. These tags are to specify which tag to read from and write to, 'tag_send' will read and write to tag, 'tag_datetime' will write a string to tag.
When initialising an object of myclass, the object have self.tag_send, self.tag_datetime, self.time_start.
After the object is created, 'self.time_start' = time.time() is run to mark down the time that the object is created.

When the object is deleted, it marks down the time and calculate the duration that object has been alive. Round downs the float into a whole number then divide by 60 to get minutes and divide by 60 again to get hours. Finally it will attempt to update the tags corresponding to one that uses seconds and other uses datetime format.

Member functions:
- `total(self)`
This function determines the total amount run time since program start and return the amount of time.
Everytime main program runs a loop, this function is ran and 't_end' is updated.
Calculate SEC by 't_end' - 'myclass.t_start' + Buttons.total_time. Calculate MIN by SEC/60. Calculate HR by MIN/60
Write to 'uptime_total' with SEC and 'datetime_total' with datetime().
Call as usual
Usage Example: total()

- `datetime()`
This function gets format data into datetime format for graphs then return it.
It create an array 'datetime', append the time char and date char into the array and joins the char into a string. 
To call, 3 numerical arguments must be passed.
Usage Example: datetime(20,20,20)

================================================

**main.py**:
This file contains the main functionalities of the program as well as background processes. It imports json, asyncio, os, psutil, tkinter, tkinter.tix, tkinter.messagebox and multiprocessing.
It also import the 2 libraries that was custom made, restjson_functions and graph_functions.
This program is run asynchronously to allow for concurrency.

`myobj` is an object of class `myclass` from restjson_functions.py

Functions:
- `error_state()`
This is the function that will be triggered if a sensor value passes its safety threshold. It read value from 'error_alert' via receive_restful. 
If value is not 0, turn towerlight to red, turn off the motor, clear the input counters, sound the buzzer and run a infinite loop, check_loop().
Once check_loop() return and the function can continue, turn off the buzzer.
Call as usual
Usage Example: error_state()

- `check_loop()`
This function will only be triggered by another function for error checking. 
It will update time and dateime for red for as long as the loop is running.
This is a loop that run infinitely and read from 'Counter_channel0' and '4051counter_channel0' and check if either value is > 0.
If value > 0, set 'error_alert' to 0 via write_restful and return.
There is a 0.3s delay to give time for *REST*.
Call as usual
Usage Example: check_loop()

- `on_function()`
This function reads value from 'Counter_channel0' and '4051counter_channel0' via receive_restful and check if either value is > 0.
Turn towerlight to green, turn on motor and clear input counters.
Call as usual
Usage Example: on_function()

- `off_function()`
This function reads value from 'Counter_channel1' and '4051counter_channel1' via receive_restful and check if either value is > 0.
Turn towerlight to amber, turn off motor and clear input counters.
Call as usual
Usage Example: off_function()

- `temp_error()`
This function reads value from 'temperature' via receive_restful and check if value > 29.
29 is the decided threshold for the thermocouple. 
If value > 29, set 'error_alert' to 1 via write_restful.
Call as usual
Usage example: temp_error()

- `dist_error()`
This function reads value from 'distance_sensor' via receive_restful and check if value < 600.
600 is the decided threshold for the distance sensor 
If value < 600, set 'error_alert' to 1 via write_restful.
Call as usual
Usage example: dist_error()

- `main()`
This function contains the essentials including creation of objects and asyncio loop. Run startup protocol.
Reset both input counters to 0, make sure the motor is off and start the twoerlight at amber.
Create a `Buttons` object for total time. Create a infinite loop and run the asyncio loop.
'loop' is a asyncio loop which will execute the asynchronous coroutine at once. 
If green or amber LED is on, their respective object will be created with the arguments for time and datetime.
Run total()
Update total run time and datetime.
Print the current amount of memory that is being used by the program.

=========================================================================

deprecated stuff:

- `display()`
This function was originally meant to create virtual buttons using tkinter but it is now deprecated after the switch to Angular.

- `multiprocessing`
Initally, multiprocessing is required for the main loop and the virtual buttons loop to run at the same time. But it is no longer needed.
