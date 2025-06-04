import { CommonModule } from "@angular/common";
import { Component } from "@angular/core";
import { ApiService } from "../../services/api.service";
import { HomeComponent } from "../Home/Home";
import { HttpClient } from "@angular/common/http";
import { interval, Subscription } from "rxjs";
import { switchMap, takeWhile, timeout } from "rxjs/operators";

@Component({
  selector: 'voice-button-component',
  templateUrl: 'VoiceButton.html',
  styleUrl: 'VoiceButton.css',
  imports: [CommonModule]
})
export class VoiceComponent {
  isProcessing: boolean = false;
  isRecording = false;
  statusText = '';
  showStatus = false;
  transcript: string = "";
  selectedLanguage: string = ''; // default language
  private pollingSubscription!: Subscription;

  constructor(private apiService: ApiService, private http: HttpClient) { }

  ngOnInit(): void {
    
    this.http.get<any>('http://localhost:8080/api/db/operation', {params:{
      operation: "language"
    }}).subscribe(
      response => {
        this.selectedLanguage = response.status
      }
    )
    
   }

  toggleRecording(): void {
    if (!this.isRecording) {
      this.startRecording();
    } else {
      this.stopRecording();
    }
  }

  startRecording(): void {
    this.isRecording = true;
    this.statusText = 'Listening...';
    this.showStatus = true;
    this.apiService.startRecording().subscribe(
      response => {
        console.log("Response: ", response)
      },
      error => {
        console.log("Error: ", error)
      }
    );
    setTimeout(() => {
      this.stopRecording();

    }, 21000); // Auto-stop after 15 seconds
  }

  toggleLanguage(language: string): void {
    this.selectedLanguage = language;
    console.log('Language changed to:', language);

    this.http.post<any>('http://localhost:8080/api/db/operation', {
      operation: "language",
      status: language
    }).subscribe(
      response => {}
    )
  }
  
  undoAction(){
    this.http.get<any>('http://localhost:8000/api/recoversnap/').subscribe(
      response => {
        setTimeout(()=>{
          window.location.reload()
        },1000)
      }
    )
  }

  checkProcessingStatus(): void {
    this.pollingSubscription = interval(2000).pipe(
      switchMap(() =>
        this.http.get<any>('http://localhost:8080/api/db/operation', {params:{
          operation: 'processing'
        }})
      ),
      // Convert string comparison to match the string "false"
      takeWhile(response => response.status !== "false", true)
    ).subscribe(
      response => {
        if (response.status === "false") {
          this.isProcessing = false;
          this.statusText = "Processing complete";
          this.http.get<any>('http://localhost:8080/api/db/transcript').subscribe(
            response => {
              this.transcript = response.transcript;
            }
          );
          setTimeout(() => {
            this.showStatus = false;
            // window.location.reload()
          }, 3000);
        }
      },
      error => {
        console.error('Polling Error:', error);
        this.statusText = 'Error while checking status';
        this.isProcessing = false;
        this.showStatus = false;
      }
    );
  }

  stopRecording(): void {
    this.isRecording = false;
    // Use "true" string value instead of boolean
    this.http.post<any>('http://localhost:8080/api/db/operation', {
      operation: "processing",
      status: "true"
    }).subscribe(
      response => {
        this.isProcessing = true;
        this.statusText = "Processing...";
        this.showStatus = true;
        // Start polling to check the status of the operation
        this.checkProcessingStatus();
        setTimeout(() => {
          this.http.get<any>('http://localhost:8080/api/db/transcript').subscribe(
            response => {
              this.transcript = response.transcript;
            }
          );
        }, 30000);
      },
      error => {
        console.error('Error during operation start:', error);
        this.statusText = 'Error starting operation';
        this.isProcessing = false;
      }
    );
  }
}