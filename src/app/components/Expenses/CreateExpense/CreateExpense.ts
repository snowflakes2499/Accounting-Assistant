import { Component, EventEmitter, Output } from "@angular/core";
import { HttpClient } from "@angular/common/http";
@Component({
    selector: 'create-expense-component',
    templateUrl: 'CreateExpense.html',
    standalone: false
})

export class CreateExpenseComponent {

    @Output() private formSubmitted = new EventEmitter<void>();
    product = {
        productName: '',
        productPrice: 0,
        productQuantity: 0,
        productTax: 0
    };

    constructor(private http:HttpClient){};

    createProduct() {
        this.http.post('http://localhost:8080/api/db/expense/create',this.product).subscribe(
            response => {
                alert('Product created')
                this.formSubmitted.emit();
            }
        )
    }
}