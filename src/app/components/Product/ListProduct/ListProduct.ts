import { Component } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Component({
    selector: 'list-product-component',
    templateUrl: 'ListProduct.html',
    standalone: false
})

export class ListProductComponent {
    products:any [] = [] 

    constructor(private http: HttpClient){
        this.http.get<any[]>('http://localhost:8080/api/db/product/list').subscribe(
            response => {
                this.products = response
            }
        )
    }

    getProducts() {
        
    }

}