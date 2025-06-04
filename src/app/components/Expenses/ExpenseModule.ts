import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { ListExpenseComponent } from "./ListExpense/ListExpense";
import { CreateExpenseComponent } from "./CreateExpense/CreateExpense";
import { DeleteExpenseComponent } from "./DeleteExpense/DeleteExpense";
import { UpdateExpenseComponent } from "./UpdateExpense/UpdateExpense";
import { FormsModule } from "@angular/forms";
@NgModule({
    declarations: [
        ListExpenseComponent, 
        CreateExpenseComponent, 
        DeleteExpenseComponent,
        UpdateExpenseComponent
    ],
    imports: [CommonModule, FormsModule],    
    exports: [
        ListExpenseComponent, 
        CreateExpenseComponent, 
        DeleteExpenseComponent,
        UpdateExpenseComponent
    ]

})

export class ExpenseModule {}