import { NgModule } from "@angular/core"
import { BrowserModule } from "@angular/platform-browser"
import { AppRoutingModule } from "./app.routing.module"
import { AppComponent } from "./app.component"
import { HttpClientModule } from "@angular/common/http"
import { VoiceComponent } from "./components/VoiceButton/VoiceButton"

@NgModule({
    declarations: [
        AppComponent
    ],
    imports : [
        AppRoutingModule,
        BrowserModule,
        HttpClientModule,
        VoiceComponent
    ],
    bootstrap: [AppComponent]
})

export class AppModule {}