import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

// HTTP request for REST api
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

// UI UX stuff from material 
import { MatSliderModule } from '@angular/material/slider';
import {MatButtonModule} from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatTabsModule } from '@angular/material/tabs';
import { MatCardModule } from '@angular/material/card';

//for temperature scale
//import { MatProgressBarModule } from '@angular/material/progress-bar'
import {MatProgressBarModule} from '@angular/material/progress-bar'

// Bootstrap
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';

//for ngmodel slider and temp
import { FormsModule } from '@angular/forms';

@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatSliderModule,
    MatButtonModule,
    MatButtonToggleModule,
    HttpClientModule,
    MatTabsModule,
    MatCardModule,
    NgbModule,
    MatProgressBarModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
