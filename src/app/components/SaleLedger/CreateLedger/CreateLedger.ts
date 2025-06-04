import { Component, EventEmitter, Output } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Component({
  selector: 'create-ledger-component',
  templateUrl: 'CreateLedger.html',
  standalone: false
})
export class CreateLedgerComponent {

  @Output() private formSubmitted = new EventEmitter<void>();

  ledger = {
    ledgerName: '',
    ledgerType: '',
    openingBalance: 0,
    currency: '',
    description: ''
  };

  constructor(private http: HttpClient) {}

  createLedger() {
    this.http.post('http://localhost:8080/api/db/ledger/create', this.ledger).subscribe(
      response => {
        alert('Ledger created successfully');
        this.formSubmitted.emit();
      },
      error => {
        alert('Failed to create ledger');
        console.error(error);
      }
    );
  }
}
