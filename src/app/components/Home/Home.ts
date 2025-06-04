import { Component, OnInit } from "@angular/core";
import { ApiService } from "../../services/api.service";
import { HttpClient } from '@angular/common/http';
import { CommonModule } from "@angular/common";

@Component({
    selector : 'home-page',
    templateUrl : 'Home.html',
    imports: [CommonModule]
})

export class HomeComponent implements OnInit{
    message: string= 'Suyash';
    greeting: string;
    loans: any[] = [];
    constructor(private apiService: ApiService, private http: HttpClient) {
        this.message = ""
        const hour = new Date().getHours();
        this.greeting = 'Good morning';
        if (hour >= 12 && hour < 17) {
            this.greeting = 'Good afternoon';
        } else if (hour >= 17) {
            this.greeting = 'Good evening';
        }
    }

    ngOnInit(): void {
        this.fetchLoans();
      }

    fetchLoans(): void {
        this.http.get<any[]>('http://localhost:8080/api/db/loans/list').subscribe({
          next: (data) => this.loans = data,
          error: (err) => console.error('Failed to fetch loans', err)
        });
      }     
    
    getTotalAmount() {
      return this.loans?.reduce((total, loan) => total + loan.loanAmount, 0) || 0;
    }
    
    getAverageAmount() {
      if (!this.loans || this.loans.length === 0) return 0;
      return (this.getTotalAmount() / this.loans.length).toFixed(2);
    }

    startRecording() {
        this.apiService.startRecording().subscribe
        (
            response => {
                this.message =  response.status
                console.log(response.status)
        }, error => {
            console.log("There is error: ", error)
        }
    )

    this.http.get<any>('http://localhost:8080/api/db/operation').subscribe(
      response => {
        
      }
    )
    }
}