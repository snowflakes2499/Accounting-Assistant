import { Component } from "@angular/core";
import { LedgerModule } from "./LedgerModule";
import { CommonModule } from "@angular/common";
@Component({
    selector: 'ledger-component',
    templateUrl: 'LedgerPage.html',    
    imports: [LedgerModule, CommonModule]
})

export class LedgerComponent {
    selectedComponent: string = 'list';
}