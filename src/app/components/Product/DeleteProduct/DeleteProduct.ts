import { Component } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Component({
    selector: 'delete-product-component',
    templateUrl: 'DeleteProduct.html',
    standalone: false
})

export class DeleteProductComponent {

    products: any[] = []

    constructor(private http: HttpClient){
        this.listProducts();
    }

    deleteProduct(id:string) {
        this.http.post('http://localhost:8080/api/db/product/delete', {'id': id}).subscribe(
            response => {
                alert('Product deleted')
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