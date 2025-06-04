import { Component } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Component({
    selector: 'list-expense-component',
    templateUrl: 'ListExpense.html',
    standalone: false
})

export class ListExpenseComponent {
    products:any [] = [] 

    constructor(private http: HttpClient){
        this.http.get<any[]>('http://localhost:8080/api/db/expense/list').subscribe(
            response => {
                this.products = response
            }
        )
    }

    getProducts() {
        
    }

}