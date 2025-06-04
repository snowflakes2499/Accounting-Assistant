import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { DebtComponent } from "./Debt/DebtComponent";
import { OweComponent } from "./Owe/OweComponent";

@NgModule({
    declarations: [DebtComponent, OweComponent],
    imports: [CommonModule],
    exports: [DebtComponent, OweComponent]
})

export class LoansModule {}