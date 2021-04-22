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
 
  test = () => {
    console.log("test")
  }

  getTagValue = (tagname:string) => {
    let body = JSON.stringify({
      "Tags":[{
        "Name":tagname
      }]
    })

    let obs = this.http.get('http://192.168.1.51/WaWebService/Json/ProjectList', {
      headers: {'Content-Type': 'application/json', 'Authorization': 'YWRtaW46'}
    });
    obs.subscribe((response) => console.log(response))
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
    obs.subscribe((response) => console.log(response))
  }
}