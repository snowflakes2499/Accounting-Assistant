import { Component, EventEmitter, Output } from "@angular/core";
import { HttpClient } from "@angular/common/http";
@Component({
    selector: 'create-product-component',
    templateUrl: 'CreateProduct.html',
    standalone: false
})

export class CreateProductComponent {

    @Output() private formSubmitted = new EventEmitter<void>();
    product = {
        productName: '',
        productPrice: 0,
        productQuantity: 0,
        productTax: 0
    };

    constructor(private http:HttpClient){};

    createProduct() {
        this.http.post('http://localhost:8080/api/db/product/create',this.product).subscribe(
            response => {
                alert('Product created')
                this.formSubmitted.emit();
            }
        )
    }
}