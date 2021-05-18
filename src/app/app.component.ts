import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, Subject } from "rxjs";
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  constructor(private http: HttpClient) {

  }
  title = "Angular";

  temp_value:any;
  motor_value: any;
  override_dist_value!: number;
  Buzzer:any;

  uptime_total:any;
  uptime_green:any;
  downtime_amber:any;
  downtime_red:any;

  percentage_uptime = 0;
  percentage_downtime = 0;
  percentage_errortime = 0;

  ngOnInit() {
    this.getMotorValue;
    this.getTempValue;
    this.simulateDistError;
    this.errorCheck;
    this.calculateUptime;
    this.calculateDowntime;
    this.calculateErrortime;
  }

  Overlay = false;
  state = false;

  overlay_off() {
    this.Overlay = false;
  }

  overlay_on() {
    this.Overlay = true;
  }

  //this pops up a page to stop further input if a error is detected
  errorCheck = setInterval(() => {
    this.getTagValue("Buzzer"); 
    
    if (this.Buzzer == 1) {
      // error overlay
      console.log("ERROR TRIGGER, STOP OPERATION!");
      if (this.state == false) {
        this.overlay_on()
        this.state = true;
      }
    } else {
      this.state = false;
      this.overlay_off()
    } 
  }, 300)

  // this is to simulate a dist sensor error
  simulateDistError = setInterval(() => {
    if (this.override_dist_value > 600) {
      this.setTagValue("error_alert", 1);
    }
  }, 500)

  // this is for getting temp value
  getTempValue = setInterval(() => {this.getTagValue("temperature")}, 5000);
  
  // get and calculate the percentage of time that green led is up
  calculateUptime = setInterval(() => {
    this.getTagValue("uptime_green");
    this.getTagValue("uptime_total");

    let value:number = +this.uptime_green;
    this.percentage_uptime = 100*value/this.uptime_total;
  }, 2500);

  calculateDowntime = setInterval(() => {
    this.getTagValue("downtime_amber");
    this.getTagValue("uptime_total");

    let value:number = +this.downtime_amber;
    this.percentage_downtime = 100*value/this.uptime_total;
  }, 2500);

  calculateErrortime = setInterval(() => {
    this.getTagValue("downtime_red");
    this.getTagValue("uptime_total");

    let value:number = +this.downtime_red;
    this.percentage_errortime = 100*value/this.uptime_total;
  }, 2500);

  lightcontrol(tagname: string) {
    this.setTagValue("towerlight_green", 0);
    this.setTagValue("towerlight_amber", 0);
    this.setTagValue("towerlight_red", 0);
    this.setTagValue(tagname, 1);
  }

  getMotorValue = setInterval(() => {
    this.getTagValue("Motor")

    if (this.motor_value == 1) {
      this.motorOn = true;
      this.motorOff = false;
    } else {
      this.motorOff = true;
      this.motorOn = false;
    }
  }, 300);

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
  
  nav_button = false;

  nav_button_toggle() {
    this.nav_button = !this.nav_button;
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
      switch (tagname) {
        case "temperature":
          this.temp_value = (JsonValues(response));
          break;
        case "uptime_green":
          this.uptime_green = (JsonValues(response));        
          break;
        case "downtime_amber":
          this.downtime_amber = (JsonValues(response));
          break;
        case "downtime_red":
          this.downtime_red = (JsonValues(response));
          break;
        case "uptime_total":
          this.uptime_total = (JsonValues(response));
          break;
        case "Buzzer":
          this.Buzzer = (JsonValues(response));
          break;
        case "motor":
        this.motor_value = (JsonValues(response));
        }
    });
  }

  setTagValue = (tagname:string, value:number) => {
    let body = JSON.stringify({
      "Tags":[{
        "Name":tagname,
        "Value":value
      }]
    });
    let obs = this.http.post('http://192.168.1.51/WaWebService/Json/SetTagValue/FirstProj', body, {
      headers: {'Content-Type': 'application/json', 'Authorization': 'YWRtaW46'}
    });
    obs.subscribe((response) => console.log(response));
  }
}