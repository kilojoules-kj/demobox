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
  constructor(private http: HttpClient) {
    
  }

  ngOnInit() {

    let body = JSON.stringify({
      "Result":{
              "Ret":0,
              "Total":2
      },
      "Projects":[{
              "ID":3,
              "Name":"Express",
              "Description":"Express Project"
      },
      {
              "ID":2,
              "Name":"WaScada",
              "Description":"WaScada Project"
      }]
    });

    let obs = this.http.get('http://192.168.1.51/WaWebService/Json/ProjectList', {
      headers: {'Content-Type': 'application/json', 'Authorization': 'YWRtaW46'}
    });
    obs.subscribe((response) => console.log(response))
  }
}