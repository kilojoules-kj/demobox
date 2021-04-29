import json
import requests

class myclass():
    controlstatus = None

    led_status = {"towerlight_green":None, "towerlight_amber":None, "towerlight_red":None}

    def __init__(self):
        #custom header
        self.header = {'Content-Type': 'application/json', 'Authorization': 'YWRtaW46'}

    def lightcontrol(self, name):   
        #set all values to 0    
        myclass.led_status = dict.fromkeys(myclass.led_status, 0)
        #set the selected value to 1
        myclass.led_status[name] = 1

        for x in myclass.led_status:
            myclass.write_restful(self, x , myclass.led_status.get(x))

        """ for x in enumerate(myclass.led_status.items()):
            print(x) """    

    def receive_restful(self, name):
        #the body of the json
        body = json.dumps({
            "Tags":[{
                "Name":name
            }]
        })

        #make a connection with requests
        try:
            response = requests.post('http://192.168.1.51/WaWebService/Json/GetTagValue/FirstProject', headers = self.header, data = body)
        except requests.exceptions.ConnectionError:
            print("Connection Error, please check WebAccess")
            return
        except Exception:
            print("generic error, please check")
            return
        return response.json()

    def write_restful(self, name, value):
        body = json.dumps({
            "Tags":[{
                "Name":name,
                "Value":value
            }]
        })

        try:
            response = requests.post('http://localhost/WaWebService/Json/SetTagValue/FirstProject', headers = self.header, data = body)
        except requests.exceptions.ConnectionError:
            print("Connection Error, please check WebAccess")
            return
        except Exception:
            print("generic error, please check")
            return    
        if response == 200:
            print("Successful write REST")
