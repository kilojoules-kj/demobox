import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, Subject } from "rxjs";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  constructor(private http: HttpClient) {

  }
  title = "Angular";

  x:any;
  temp_value:any;
  override_dist_value!: number;
  uptime_percentage!:number;
  downtime_percentage!: number;
  errortime_percentage!:number;

  ngOnInit() {
    this.getTempValue;
    this.simulateDistError;
    this.errorCheck;
    this.calculateUptime;
    this.calculateDowntime;
    this.calculateErrortime;
  }

  //this pops up a page to stop further input if a error is detected
  errorCheck = setInterval(() => {
    let Buzzer:any = this.getTagValue("Buzzer"); 
    if (Buzzer == 1) {
      // error overlay
      console.log("ERROR TRIGGER, STOP OPERATION!")
    }; 
  }, 1000)

  // this is to simulate a dist sensor error
  simulateDistError = setInterval(() => {this.setDistValue(this.override_dist_value)}, 1000)
  setDistValue = (value: number) => {
    if (value > 600) {
      this.setTagValue("error_alert", 1);
    }
  }

  // this is for getting temp value
  getTempValue = setInterval(() => {this.temp_value = this.getTagValue("temperature")}, 1000);

  // get and calculate the percentage of time that green led is up
  calculateUptime = setInterval(() => {
    let uptime_green = this.getTagValue("uptime_green");
    let uptime_total = this.getTagValue("uptime_total");
    this.uptime_percentage = (uptime_green / uptime_total) *100;
  }, 1000);

  calculateDowntime = setInterval(() => {
    let uptime_amber = this.getTagValue("uptime_green");
    let uptime_total = this.getTagValue("uptime_total");
    this.downtime_percentage = (uptime_amber / uptime_total) *100;
  }, 1000);

  calculateErrortime = setInterval(() => {
    let uptime_red = this.getTagValue("uptime_green");
    let uptime_total = this.getTagValue("uptime_total");
    this.errortime_percentage = (uptime_red / uptime_total) *100;
  }, 1000);

  lightcontrol(tagname: string) {
    this.setTagValue("towerlight_green", 0);
    this.setTagValue("towerlight_amber", 0);
    this.setTagValue("towerlight_red", 0);
    this.setTagValue(tagname, 1);
  }

  motorOff = true;
  motorOn = false;

  motor_toggle_on() {
    if (this.motorOn == false) {
      this.motor_toggle()
    }
    this.lightcontrol("towerlight_green");
    this.setTagValue("Motor", 1);
  }

  motor_toggle_off() {
    if (this.motorOff == false) {
      this.motor_toggle()
    }
    this.lightcontrol("towerlight_amber");
    this.setTagValue("Motor", 0);
  }
  
  motor_toggle() {
    this.motorOn = !this.motorOn;
    this.motorOff = !this.motorOff;
  }
  
  nav_button_toggle() {
    // do nothing yet
  }

  getTagValue = (tagname:string) => {
    let JsonValues = (json:any) => {
      let res:any = json["Values"][0]["Value"]
      return res;
    }
    let body = JSON.stringify({
      "Tags":[{
        "Name":tagname
      }]
    })

    let obs = this.http.post('http://192.168.1.51/WaWebService/Json/GetTagValue/FirstProj', body, {
      headers: {'Content-Type': 'application/json', 'Authorization': 'YWRtaW46'}
    });
    obs.subscribe((response) => { 
      this.x = (JsonValues(response));
    });
    return this.x;
  }

  setTagValue = (tagname:string, value:number) => {
    let body = JSON.stringify({
      "Tags":[{
        "Name":tagname,
        "Value":value
      }]
    });
    console.log(body)
    let obs = this.http.post('http://192.168.1.51/WaWebService/Json/SetTagValue/FirstProj', body, {
      headers: {'Content-Type': 'application/json', 'Authorization': 'YWRtaW46'}
    });
    obs.subscribe((response) => console.log(response));
  }
}