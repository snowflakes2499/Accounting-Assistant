import { Component } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { FormsModule } from "@angular/forms";
@Component({
    selector: 'update-ledger-component',
    templateUrl: 'UpdateLedger.html',
    standalone: false
})

export class UpdateLedgerComponent {
    products: any[] = []
    product = {
        id: null,
        productName: null,
        productPrice: null,
        productQuantity: null,
        productTax: null,
    }
    constructor(private http: HttpClient){
        this.listProducts();
    }

    
    updateProduct(product: any) {
        this.http.post('http://localhost:8080/api/db/product/update', product).subscribe(
            response => {
                alert('Product updated')
                this.listProducts();
            }
        )
    }    

    listProducts(){
        this.http.get<any[]>('http://localhost:8080/api/db/product/list').subscribe(
            response => {
                this.products = response;
            }
        )
    }
}