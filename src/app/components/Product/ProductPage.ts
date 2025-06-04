import { Component } from "@angular/core";
import { ProductModule } from "./ProductModule";
import { CommonModule } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { EventEmitter, Output } from "@angular/core";
import { FormsModule } from "@angular/forms";

@Component({
    selector: 'product-component',
    templateUrl: 'ProductPage.html',    
    imports: [ProductModule, CommonModule, FormsModule]
})

export class ProductComponent {
    products:any [] = [] 

    selectedComponent: string = 'list';

    @Output() private formSubmitted = new EventEmitter<void>();
    product = {
        productName: '',
        productPrice: 0,
        sellingPrice: 0,
        productQuantity: 0,
        productTax: 0,
    };

    constructor(private http: HttpClient){
        this.http.get<any[]>('http://localhost:8080/api/db/product/list').subscribe(
            response => {
                this.products = response
            }
        )
    }

    createProduct() {
        this.http.post('http://localhost:8080/api/db/product/create',this.product).subscribe(
            response => {
                alert('Product created')
                this.formSubmitted.emit();
            }
        )
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

    updateProduct(product: any) {
        this.http.post('http://localhost:8080/api/db/product/update', product).subscribe(
            response => {
                alert('Product updated')
                this.listProducts();
            }
        )
    }    


    getProducts() {
        
    }
}