import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";

import { CreateLedgerComponent } from "./CreateLedger/CreateLedger";
import { ListLedgerComponent } from "./ListLedger/ListLedger";
import { UpdateLedgerComponent } from "./UpdateLedger/UpdateProduct";
import { DeleteLedgerComponent } from "./DeleteLedger/DeleteLedger";

import { FormsModule } from "@angular/forms";
@NgModule({
    declarations: [
        CreateLedgerComponent,
        ListLedgerComponent,
        UpdateLedgerComponent,
        DeleteLedgerComponent
    ],
    imports: [CommonModule, FormsModule],    
    exports: [
        CreateLedgerComponent,
        ListLedgerComponent,
        UpdateLedgerComponent,
        DeleteLedgerComponent
    ]

})

export class LedgerModule {}