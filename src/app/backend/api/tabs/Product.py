from django.conf import settings
from django.http import JsonResponse
import requests
import json
from api.constants import PRODUCT_TEMPLATE_PATH
from api.models import Product as ProductModel

INVOICE_NINJA_API_URL = settings.INVOICE_NINJA_API_URL
INVOICE_NINJA_API_TOKEN = settings.INVOICE_NINJA_API_TOKEN
MEDIA_ROOT = settings.MEDIA_ROOT


class Product: 
    
    def appropriate_function(self, transcript):
        
        # use the second NLP model to get the appropriate function
        # pass the transcript to the model
        # get the function name
        # call the function                         
        with open(PRODUCT_TEMPLATE_PATH) as f: prompt = f.read()

        prompt += f""" Now extract from: '{transcript}' """

        OLLAMA_URL = "http://localhost:11434/api/generate"

        # API request payload
        data = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }        

        # print(f"\n\nThe prompt is , {prompt} ")

        response = requests.post(OLLAMA_URL, json=data)            
        if response.status_code == 200:

            # print("\n\nModel output: ", response.json())
    
            # Extract the response text and parse it as JSON
            response_string = response.json().get("response", "").strip()
            output_texts = json.loads(response_string)
            print("Output TEXTS: ", output_texts)
            for output_text in output_texts: 
                print("Output text: ", output_text)
                json_output = output_text
                
                # Check if the required keys are present in the JSON output
                if "operation" in json_output and "data" in json_output:
                    operation = json_output.get("operation", "").strip().lower()
                    data = json_output.get("data", {})  # Corrected to retrieve "data" instead of "response"

                    # Map operations to corresponding functions
                    operation_map = {
                        "create_product": self.create_product,
                        "update_product": self.update_product,
                        "delete_product": self.delete_product,
                        "read_product": self.read_product,
                        "sell_product": self.sell_product
                    }

                    # Check if the operation is in the map and call the corresponding function
                    if operation in operation_map:
                        # print("Operation: ", operation)
                        # print("Data: ", data)
                        # Call the corresponding function with the data
                        operation_map[operation](data)
                    else:
                        print(f"Unknown operation: {operation}")
                else:
                    print("Invalid JSON structure: 'operation' or 'data' not found")
        else:
            print(f"API request failed with status code: {response.status_code}")

        return JsonResponse({"status": "Product appropriate function called"})
        

    def create_product(self, data):
        """Create a new product in the database."""        
        product_description = "This is a sample product."
        product_name = data.get('product_key', '').lower()
        product_price = data.get('price', 0)
        product_quantity = data.get('quantity', 0)
        product_tax = data.get('tax', 0)
        product_selling_price = data.get('selling_price', 0)

        product_data = {
            "productName": f"{product_name}",
            "productPrice": f"{product_price}",
            "productQuantity": f"{product_quantity}",
            "productTax": f"{product_tax}",
            "sellingPrice": f"{product_selling_price}"
        }

        print("Creating product.. ")
        print("Product data: ", product_data)
        # Send request to Invoice Ninja        

        if product_name:            
            response = requests.post('http://localhost:8080/api/db/product/create',json=product_data)
            print("The response is:  ", response)
            if response.status_code == 200:
                return JsonResponse({'message': 'Product created successfully'})
            return JsonResponse({'message': "error creating product"}, status=500)
        else:
            print("Error creating product status 500")
            return JsonResponse({'message': 'Failed to create product'}, status=500)

    def update_product(self, data):
        product_name = data.get('product_key', '').lower()
        product_price = data.get('price', 0)
        product_quantity = data.get('quantity', 0)
        product_tax = data.get('tax', 0)
        product_selling_price = data.get('selling_price', 0)
        update_fields = {}

        if product_selling_price != 0:
            update_fields['sellingPrice'] = data['selling_price']

        if product_price!=0:
            update_fields['productPrice'] = data['price']

        if product_quantity!=0:
            update_fields['productQuantity'] = data['quantity']

        if product_tax!=0:
            update_fields['productTax'] = data['tax']

        # update_fields['productPrice'] = data['price']

        # update_fields['productQuantity'] = data['productQuantity']

        # update_fields['productTax'] = data['tax']

        if update_fields:
                update_fields["id"] = product_name
                print("Update fields are: ", update_fields)
                LINK = "http://localhost:8080"
                response = requests.post(f"{LINK}/api/db/product/update",json=update_fields)
                if response.status_code == 200:
                    print(f"product(s) updated successfully.")
                    print(response.json().get("response", "").strip())
                else:
                    print("error updating product")
        else:
            print("No valid fields to update.")

    def delete_product(self, data):
        LINK = "http://localhost:8080"
        product = data.get('product_key', '').lower()
        response = requests.post(f"{LINK}/api/db/product/delete",json={"id":product})
        if response.status_code == 200:            
            print("Product deleted successfully")
        else:
            print("No product found with the given name.")

    def sell_product(self, data):
        product_name = data.get('product_key', '').lower()
        product_quantity = data.get('quantity', 0)
        product_data = {
            "id": f"{product_name}",
            "productQuantity": f"{product_quantity}",
        }
        response = requests.post('http://localhost:8080/api/db/product/sell',json=product_data)
        print("The response is:  ", response)
        if response.status_code == 200:
            print("Sold product")
            return JsonResponse({'message': 'Product created successfully'})

    def read_product(self, data):
        product_name = data.get('product_key', '').lower()

        response = requests.get(
            INVOICE_NINJA_API_URL,
            headers={
                'Content-Type': 'application/json',
                'X-API-TOKEN': INVOICE_NINJA_API_TOKEN,
            }
        )
        
        products = ProductModel.objects.filter(product_name=product_name)
        for product in products:
            print(f"Product Name: {product.product_name}\n"
            f"Price: ₹{product.product_price}\n"
            f"Quantity: {product.product_quantity}\n"
            f"Tax: ₹{product.product_tax}")



        if response.status_code == 200:
            # print(response.json())
            return JsonResponse({'message': 'Products fetched successfully'})
        else:
            print(response.text)
            return JsonResponse({'message': 'Failed to get products'}, status=500)    