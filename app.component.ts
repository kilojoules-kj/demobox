import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'myproject';

  public On:boolean = false;
  public Off:boolean = false;

  public buttonName:any = 'On';

  ngOnInit () {  }

  toggle() {
    this.Off = !this.Off;

    // CHANGE THE NAME OF THE BUTTON.
    //if(this.Off)  
      //this.buttonName = "On";
    //else
      //this.buttonName = "Off";
  }
  toggle1() {
    this.On = !this.On;

    // CHANGE THE NAME OF THE BUTTON.
    //if(this.On)  
      //this.buttonName = "On";
    //else
      //this.buttonName = "Off";
  }

}





