import { CommonModule } from "@angular/common";
import { Component, OnInit } from "@angular/core";
import { LoansModule } from "./LoansModule";
import { HttpClient } from '@angular/common/http';

@Component({
    selector: 'loan-component',
    templateUrl : 'Loans.html',
    styleUrl: 'Loans.css',
    imports: [CommonModule, LoansModule]
})

export class LoanComponent implements OnInit {
    transactions: any[] = [];
  isLoading = true;
  error: string = '';

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchTransactions();
  }

  fetchTransactions(): void {
    this.http.get<any[]>('http://localhost:8080/api/db/transactions/list').subscribe({
      next: data => {
        this.transactions = data.filter(tx => tx.loanType && tx.loanAmount > 0)
        .sort((a, b) => b.id - a.id);
        this.isLoading = false;
      },
      error: err => {
        this.error = 'Failed to load transactions.';
        this.isLoading = false;
        console.error(err);
      }
    });
  }
}