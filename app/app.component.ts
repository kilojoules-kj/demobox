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
  test:number | undefined;
  Buzzer:any;

  uptime_total:any;
  uptime_green:any;
  downtime_amber:any;
  downtime_red:any;

  ngOnInit() {
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
  simulateDistError = setInterval(() => {this.setDistValue(this.override_dist_value)}, 500)
  setDistValue = (value: number) => {
    if (value > 600) {
      this.setTagValue("error_alert", 1);
    }
  }

  // this is for getting temp value
  getTempValue = setInterval(() => {this.temp_value = this.getTagValue("temperature")}, 3000);

  // get and calculate the percentage of time that green led is up
  calculateUptime = setInterval(() => {
    this.uptime_green = this.getTagValue("uptime_green");
    this.uptime_total = this.getTagValue("uptime_total");
  }, 7000);

  calculateDowntime = setInterval(() => {
    this.downtime_amber = this.getTagValue("downtime_amber");
    this.uptime_total = this.getTagValue("uptime_total");
    //this.test = Number(this.downtime_amber) //(100*parseFloat(this.downtime_amber)/parseFloat(this.uptime_total))
  }, 7000);

  calculateErrortime = setInterval(() => {
    this.downtime_red = this.getTagValue("downtime_red");
    this.uptime_total = this.getTagValue("uptime_total");
  }, 7000);

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