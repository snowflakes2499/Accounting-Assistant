import { CommonModule } from "@angular/common";
import { NgModule } from "@angular/core";
import { ListProductComponent } from "./ListProduct/ListProduct";
import { CreateProductComponent } from "./CreateProduct/CreateProduct";
import { DeleteProductComponent } from "./DeleteProduct/DeleteProduct";
import { UpdateProductComponent } from "./UpdateProduct/UpdateProduct";
import { FormsModule } from "@angular/forms";
@NgModule({
    declarations: [
        ListProductComponent, 
        CreateProductComponent, 
        DeleteProductComponent,
        UpdateProductComponent
    ],
    imports: [CommonModule, FormsModule],    
    exports: [
        ListProductComponent, 
        CreateProductComponent, 
        DeleteProductComponent,
        UpdateProductComponent
    ]

})

export class ProductModule {}