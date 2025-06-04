import { Component } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Component({
  selector: 'list-ledger-component',
  templateUrl: 'ListLedger.html',
  standalone: false
})
export class ListLedgerComponent {
  ledgers: any[] = [];
  products: any[] = [];
  constructor(private http: HttpClient) {
    this.getLedgers();
  }

  getLedgers() {
    this.http.get<any[]>('http://localhost:8080/api/db/product/list').subscribe( 
      productResponse => {
        this.products = productResponse;
        console.log("Fetched Products:", this.products);
  
        this.http.get<any[]>('http://localhost:8080/api/db/product/sell').subscribe( 
          ledgerResponse => {
            console.log("Fetched Ledgers:", ledgerResponse);
  
            this.ledgers = ledgerResponse.map(ledger => {
              const matchedProduct = this.products.find(p => +p.id === +ledger.soldProductId);
              return {
                ...ledger,
                productName: matchedProduct ? matchedProduct.productName : ''
              };
            }).sort((a, b) => b.id - a.id);;
  
            console.log("Mapped Ledgers:", this.ledgers);
          },
          error => {
            console.error("Error fetching ledgers", error);
          }
        );
      },
      error => {
        console.error("Error fetching products", error);
      }
    );
  }
  
  

}
