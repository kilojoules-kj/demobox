import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { asapScheduler, Observable } from "rxjs";
import { ApiService } from './api.service';
import { ValueConverter } from '@angular/compiler/src/render3/view/template';
import { analyzeAndValidateNgModules, sanitizeIdentifier } from '@angular/compiler';
import { newArray } from '@angular/compiler/src/util';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})

export class AppComponent {
  // constructor(private http: HttpClient, public _name?:string) {
    
  // }

  constructor(private http: HttpClient) {

  }

  // get name() {
  //   return this._name;
  // }

  // set name(value) {
  //   this._name = value;
  // }
  
  x: any;
  override_dist_value!: number;

  ngOnInit() {
    this.myFunction;
    this.myFunction2;
    this.myFunction3;
  }

  // this is to stop further input if a error is detected
  myFunction3 = setInterval(() => {
    let Buzzer:any = this.getTagValue("Buzzer"); 
    if (Buzzer == 1) {
      console.log("stop")
    }; 
  }, 1000)

  // this is to simulate a dist sensor error - doesnt work yet
  myFunction2 = setInterval(() => {this.simulate_dist_error(this.override_dist_value)}, 2000)
  simulate_dist_error = (value: number) => {
    if (value > 600) {
      this.setTagValue("distance_sensor", 999);
    }
  }

  // this is for getting a tag value
  myFunction = setInterval(() => {this.getTagValue("s100_tag2"); }, 3000);
  JsonValues = (json:any) => {
    let res:any = json["Values"][0]["Value"]
    console.log(res)
    return res;
  }

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
    let body = JSON.stringify({
      "Tags":[{
        "Name":tagname
      }]
    })

    let obs = this.http.post('http://192.168.1.51/WaWebService/Json/GetTagValue/FirstProj', body, {
      headers: {'Content-Type': 'application/json', 'Authorization': 'YWRtaW46'}
    });
    obs.subscribe((response) => this.x = this.JsonValues(response));
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