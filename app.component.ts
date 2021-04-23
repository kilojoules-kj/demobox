import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from "rxjs";
import { ApiService } from './api.service';

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

  ngOnInit() {
    this.myFunction;
  }

  myFunction = setInterval(() => {this.getTagValue("s100_tag2")}, 3000);
    
  JsonValues = (json:any) => {
    let res:any = json["Values"]["0"]["Value"]  
    return res;
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