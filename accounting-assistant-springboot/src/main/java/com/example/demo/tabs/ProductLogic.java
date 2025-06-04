package com.example.demo.tabs;

import com.example.demo.model.Product;
import com.example.demo.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Optional;
//import java.util.Map;

import org.json.JSONObject;
import org.springframework.web.client.RestTemplate;

@Component
public class ProductLogic {

    private static final String PRODUCT_TEMPLATE_PATH = "src/main/resources/templates/Product.txt";

    @Autowired
    private ProductRepository productRepository;

    public void appropriateFunction(String transcript) {
        try {
            String prompt = Files.readString(Paths.get(PRODUCT_TEMPLATE_PATH));
            prompt += "\nNow extract from: '" + transcript + "'";

            System.out.println("\n\nThe prompt is:\n" + prompt);

            // API request to Ollama
            String OLLAMA_URL = "http://localhost:11434/api/generate";
            RestTemplate restTemplate = new RestTemplate();

            JSONObject requestBody = new JSONObject();
            requestBody.put("model", "mistral");
            requestBody.put("prompt", prompt);
            requestBody.put("stream", false);

            JSONObject response = new JSONObject(
                restTemplate.postForObject(OLLAMA_URL, requestBody.toString(), String.class)
            );

            String outputText = response.optString("response", "").trim();
            System.out.println("Output text: " + outputText);

            JSONObject jsonOutput = new JSONObject(outputText);

            if (jsonOutput.has("operation") && jsonOutput.has("data")) {
                String operation = jsonOutput.getString("operation").trim().toLowerCase();
                JSONObject data = jsonOutput.getJSONObject("data");

                switch (operation) {
                    case "create_product" -> createProduct(data);
                    case "update_product" -> updateProduct(data);
                    case "delete_product" -> deleteProduct(data);
                    case "read_product" -> readProduct(data);
                    default -> System.out.println("Unknown operation: " + operation);
                }
            } else {
                System.out.println("Invalid JSON structure: 'operation' or 'data' not found");
            }

        } catch (IOException e) {
            System.out.println("Error reading prompt file: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Error during function execution: " + e.getMessage());
        }
    }

    private void createProduct(JSONObject data) {
        Product product = new Product();
        product.setProductName(data.optString("product_key", "").toLowerCase());
        product.setProductPrice(BigDecimal.valueOf(data.optDouble("price", 0)));
        product.setProductQuantity(data.optInt("quantity", 0));
        product.setProductTax(BigDecimal.valueOf(data.optDouble("tax", 0)));

        productRepository.save(product);
        System.out.println("Product created: " + product.getProductName());
    }

    private void updateProduct(JSONObject data) {
        String productName = data.optString("product_key", "").toLowerCase();
        Optional<Product> optionalProduct = productRepository.findByProductName(productName);

        if (optionalProduct.isPresent()) {
            Product product = optionalProduct.get();
            if (data.has("price")) {
                product.setProductPrice(BigDecimal.valueOf(data.getDouble("price")));
            }
            if (data.has("tax")) {
                product.setProductTax(BigDecimal.valueOf(data.getDouble("tax")));
            }
            productRepository.save(product);
            System.out.println("Product updated: " + productName);
        } else {
            System.out.println("No product found with name: " + productName);
        }
    }

    private void deleteProduct(JSONObject data) {
        String productName = data.optString("product_key", "").toLowerCase();
        Optional<Product> product = productRepository.findByProductName(productName);

        if (product.isPresent()) {
            productRepository.delete(product.get());
            System.out.println("Product deleted: " + productName);
        } else {
            System.out.println("No product found with name: " + productName);
        }
    }

    private void readProduct(JSONObject data) {
        String productName = data.optString("product_key", "").toLowerCase();
        Optional<Product> product = productRepository.findByProductName(productName);

        product.ifPresentOrElse(
            p -> System.out.println("Product Details:\n" +
                "Name: " + p.getProductName() + "\n" +
                "Price: ₹" + p.getProductPrice() + "\n" +
                "Quantity: " + p.getProductQuantity() + "\n" +
                "Tax: ₹" + p.getProductTax()),
            () -> System.out.println("No product found with name: " + productName)
        );
    }
}
