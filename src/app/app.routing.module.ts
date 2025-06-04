import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";
import { HomeComponent } from "./components/Home/Home";
import { ProductComponent } from "./components/Product/ProductPage";
import { LoanComponent } from "./components/Loans/Loans";
import { LedgerComponent } from "./components/SaleLedger/LedgerPage";
import { ExpenseComponent } from "./components/Expenses/ExpensePage";

const routes:Routes = [
    {path: '', redirectTo: '/home', pathMatch: 'full'},
    {path: 'home' , component: HomeComponent},
    {path: 'product', component: ProductComponent},
    {path: 'expense', component: ExpenseComponent},
    {path: 'loans', component: LoanComponent},
    {path: 'ledger', component:LedgerComponent}
]

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})

export class AppRoutingModule {

}