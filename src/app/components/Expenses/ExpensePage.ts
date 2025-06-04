import { Component } from "@angular/core";
import { ExpenseModule } from "./ExpenseModule";
import { CommonModule } from "@angular/common";
import { HttpClient } from "@angular/common/http";
import { EventEmitter, Output } from "@angular/core";
import { FormsModule } from "@angular/forms";

@Component({
    selector: 'expense-component',
    templateUrl: 'ExpensePage.html',    
    imports: [ExpenseModule, CommonModule, FormsModule]
})

export class ExpenseComponent {
    expenses:any [] = [] 

    selectedComponent: string = 'list';

    @Output() private formSubmitted = new EventEmitter<void>();
    expense = {
        productName: '',
        productPrice: 0,
        productQuantity: 0,
        productTax: 0
    };

    constructor(private http: HttpClient){
        this.http.get<any[]>('http://localhost:8080/api/db/expense/list').subscribe(
            response => {
                this.expenses = response
            }
        )
    }

    createProduct() {
        this.http.post('http://localhost:8080/api/db/expense/create',this.expense).subscribe(
            response => {
                alert('Product created')
                this.formSubmitted.emit();
            }
        )
    }

    deleteProduct(id:string) {
        this.http.post('http://localhost:8080/api/db/expense/delete', {'id': id}).subscribe(
            response => {
                alert('Product deleted')
                this.listProducts();
            }
        )
    }

    listProducts(){
        this.http.get<any[]>('http://localhost:8080/api/db/expense/list').subscribe(
            response => {
                this.expenses = response;
            }
        )
    }

    updateProduct(expense: any) {
        this.http.post('http://localhost:8080/api/db/expense/update', expense).subscribe(
            response => {
                alert('Product updated')
                this.listProducts();
            }
        )
    }    


    getProducts() {
        
    }
}