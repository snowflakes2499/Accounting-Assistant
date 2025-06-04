package com.example.demo.controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import com.example.demo.tabs.ProductLogic;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;
import com.example.demo.AccountingAssistantSpringbootApplication;
import com.example.demo.model.Expense;
import com.example.demo.model.Loans;
import com.example.demo.model.Product;
import com.example.demo.model.SellingLedger;
import com.example.demo.model.Settings;
import com.example.demo.model.Transcript;
import com.example.demo.model.Transactions;
import com.example.demo.repository.ExpenseRepository;
import com.example.demo.repository.LoanRepository;
import com.example.demo.repository.ProductRepository;
import com.example.demo.repository.SellingLedgerRepository;
import com.example.demo.repository.SettingsRepository;
import com.example.demo.repository.TransactionRepository;
import com.example.demo.repository.TranscriptRepository;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.sql.Date;

@RestController
@RequestMapping("/api/db")
public class DatabaseController {

    private final WebMvcConfigurer corsConfigurer;

    private final ProductLogic productLogic;

    private final AccountingAssistantSpringbootApplication accountingAssistantSpringbootApplication;
	
	private final ProductRepository productRepository;
	private final LoanRepository loansRepository;
	private final TranscriptRepository transcriptRepository; 
	private final TransactionRepository transactionRepository;
	private final SettingsRepository settingsRepository ;
	private final ExpenseRepository expenseRepository;
	private final SellingLedgerRepository sellingLedgerRepository;
	
	public DatabaseController(SellingLedgerRepository sellingLedgerRepository, ExpenseRepository expenseRepository, SettingsRepository settingsRepository, TransactionRepository transactionRepository, ProductRepository productRepository, LoanRepository loanRepository, TranscriptRepository transcriptRepository, AccountingAssistantSpringbootApplication accountingAssistantSpringbootApplication, ProductLogic productLogic, WebMvcConfigurer corsConfigurer) {
		this.productRepository = productRepository;
		this.loansRepository = loanRepository;
		this.accountingAssistantSpringbootApplication = accountingAssistantSpringbootApplication;
		this.productLogic = productLogic;
		this.transactionRepository = transactionRepository;
		this.transcriptRepository = transcriptRepository;
		this.settingsRepository = settingsRepository;
		this.expenseRepository = expenseRepository;
		this.sellingLedgerRepository = sellingLedgerRepository;
		this.corsConfigurer = corsConfigurer;
	}
	
	@GetMapping("/operation")
	public ResponseEntity<Settings> getOperation(@RequestParam Map<String, String> payload){
		String operation = payload.get("operation");
		Settings fetchedOperation = settingsRepository.findByoperation(operation);
		return ResponseEntity.ok(fetchedOperation);
	}
	
	@PostMapping("/operation")
	public ResponseEntity<Settings> setOperation(@RequestBody Settings settings){		
		Settings savedSettings = settingsRepository.save(settings);
		return ResponseEntity.ok(savedSettings);
	}
	
	@GetMapping("/transcript")
	public ResponseEntity<Transcript> getTranscript(){
		Transcript transcript = transcriptRepository.findTopByOrderByIdDesc();
		return ResponseEntity.ok(transcript);
	}
	@PostMapping("/transcript")
	public ResponseEntity<Transcript> saveTranscript(@RequestBody Transcript transcript) {
		transcriptRepository.save(transcript);
		return ResponseEntity.ok(transcript);
	}
	@GetMapping("/product/list")
	public ResponseEntity<List<Product>> getProducts() {
		List<Product> products = productRepository.findAll();
		return ResponseEntity.ok(products);
	}
	
	@PostMapping("/product/product")
	public ResponseEntity<Product> getProduct(@RequestBody Map<String, Long> payload) {
		Product product = productRepository.findByid(payload.get("id"));
		return ResponseEntity.ok(product);
	}
	
	@PostMapping("/product/create")
	public ResponseEntity<Product> createProduct(@RequestBody Product product) {
		Product savedProduct = productRepository.save(product);		
		return ResponseEntity.ok(savedProduct);
	}
	
	@PostMapping("/product/delete")
	public ResponseEntity<Map<String, String>> deleteProduct(@RequestBody Map<String, Long> payload){
		Long id = payload.get("id");
		productRepository.deleteById(id);	
		Map<String, String> response = new HashMap<>();
	    response.put("message", "Deleted product with id: " + id);
		return ResponseEntity.ok(response);
	}
	
//	@PostMapping("/product/update")
//	public ResponseEntity<?> updateProduct(@RequestBody Product product) {
//		
//		Long id = product.getId();
//		if(id != null) {
//			productRepository.save(product);
//			return ResponseEntity.ok(product);
//		}
//		return ResponseEntity.badRequest().body("Please provide product id!");				
//	}
	
	@GetMapping("/product/sell")
	public ResponseEntity<List<SellingLedger>> getSellProducts(){
		List<SellingLedger> soldProducts = sellingLedgerRepository.findAll();		
		return ResponseEntity.ok(soldProducts);
	}
	
	
	
	@PostMapping("/product/sell")
	public ResponseEntity<?> sellProduct(@RequestBody Map<String,String> payload){
		Long id = Long.valueOf(payload.get("id"));
		Integer quantity = Integer.valueOf(payload.get("productQuantity"));
		Product sellingProduct = productRepository.getById(id);
		String productName = sellingProduct.getProductName();
		Integer sellingProductQuantity = sellingProduct.getProductQuantity();
		BigDecimal sellingPrice = sellingProduct.getSellingPrice();
		BigDecimal actualPrice = sellingProduct.getProductPrice();
		BigDecimal productTax = sellingProduct.getProductTax();
		
		// Adding record to the the selling ledger
		SellingLedger soldProduct = new SellingLedger();						
		soldProduct.setSoldProductId(id);
		soldProduct.setSoldProductQuantity(quantity);
		soldProduct.setSoldProductSellingPrice(sellingPrice);
		soldProduct.setSoldProductActualPrice(actualPrice);
		soldProduct.setSoldProductTax(productTax);
		soldProduct.setProductName(productName);
		if(sellingProductQuantity>=quantity) {
			Integer soldQuantity = sellingProductQuantity-quantity;
			BigDecimal soldAmount = sellingPrice.multiply(BigDecimal.valueOf(quantity));
			soldAmount = soldAmount.add(soldAmount.multiply(productTax.divide(BigDecimal.valueOf(100))));
			sellingProduct.setProductQuantity(soldQuantity);			
			soldProduct.setSoldAmount(soldAmount);		
		}else {
			Integer soldQuantity = 0;
			BigDecimal soldAmount = sellingPrice.multiply(BigDecimal.valueOf(sellingProductQuantity));
			soldAmount = soldAmount.add(soldAmount.multiply(productTax.divide(BigDecimal.valueOf(100))));
			sellingProduct.setProductQuantity(soldQuantity);			
			soldProduct.setSoldAmount(soldAmount);
		}
		sellingLedgerRepository.save(soldProduct);
		productRepository.save(sellingProduct);
		return ResponseEntity.ok("done");
	}
	@PostMapping("/product/update")
	public ResponseEntity<?> updateProduct(@RequestBody Product product) {
		
		Long id = product.getId();
		if(id != null) {
			Product savedProduct = productRepository.getById(id);
			String productName = product.getProductName();
			BigDecimal productPrice = product.getProductPrice();
			BigDecimal sellingPrice = product.getSellingPrice();
			BigDecimal productTax = product.getProductTax();
			Integer quantity = product.getProductQuantity();
			
			if(sellingPrice!=null) {
				savedProduct.setSellingPrice(sellingPrice);
			}
			if(productName!=null) {
				savedProduct.setProductName(productName);
			}
			if(productPrice!=null) {
				savedProduct.setProductPrice(productPrice);	
			}
			if(productTax!=null) {
				savedProduct.setProductTax(productTax);
			}
			if(quantity!=null) {
				savedProduct.setProductQuantity(quantity);
			}
			
			productRepository.save(savedProduct);
			return ResponseEntity.ok(savedProduct);
		}
		return ResponseEntity.badRequest().body("Please provide product id!");
	}
	
	@GetMapping("/loans/list")
	public ResponseEntity<List<Loans>> getLoans() {
		List<Loans> allLoans = loansRepository.findAll();		
		return ResponseEntity.ok(allLoans);		
	}
	
	@PostMapping("/loans/loan")
	public ResponseEntity<Loans> getLoan(@RequestBody Map<String, String> payload) {
		Loans fetchedLoan = loansRepository.findBypersonName(payload.get("personName"));
		return ResponseEntity.ok(fetchedLoan);
	}
	
	@PostMapping("/loans/create")
	public ResponseEntity<Loans> createLoan(@RequestBody Loans loan) {
		loan.setPersonName(loan.getPersonName().toLowerCase());
		Loans createdLoan = loansRepository.save(loan);
		return ResponseEntity.ok(createdLoan);
	}
	
	@PostMapping("/loans/update")
	public ResponseEntity<?> updateLoan(@RequestBody Loans loan) {
		Loans person = loansRepository.getById(loan.getPersonName());
		if(person != null) {
			if(loan.getLoanAmount()!=null) {
				person.setLoanAmount(loan.getLoanAmount());
			}
			
//			loan.setPersonName(loan.getPersonName().toLowerCase());
			Loans updatedLoan = loansRepository.save(person);
			return ResponseEntity.ok(updatedLoan);
		}
		return ResponseEntity.badRequest().body("No Name provided!");
		
	}
	
	@GetMapping("/transactions/list")
	public ResponseEntity<List<Transactions>> getTransactions() {
		List<Transactions> allTransactions = transactionRepository.findAll();		
		return ResponseEntity.ok(allTransactions);		
	}
	
	@PostMapping("/transactions/create")
	public ResponseEntity<?> createTransaction(@RequestBody Transactions transaction) {
		Loans loan = loansRepository.getById(transaction.getPersonName());
		
		if(loan!=null) {
			transactionRepository.save(transaction);
			return ResponseEntity.ok(transaction);
		}
		return ResponseEntity.badRequest().body("Please provide accurate name!");				
	}
	
	
	@PostMapping("/transactions/delete")
	public ResponseEntity<Map<String, String>> deleteTransaction(@RequestBody Map<String, Long> payload) {
		Long id = payload.get("id");
		transactionRepository.deleteByid(id);	
		Map<String, String> response = new HashMap<>();
	    response.put("message", "Deleted product with id: " + id);
		return ResponseEntity.ok(response);						
	}
	
	
	@GetMapping("/expense/list")
	public ResponseEntity<List<Expense>> getExpenses() {
		List<Expense> expenses = expenseRepository.findAll();
		return ResponseEntity.ok(expenses);
	}
	
	@PostMapping("/expense/expense")
	public ResponseEntity<?> getExpense(@RequestBody Map<String, String> payload) {
		String from = payload.get("from");
		String to = payload.get("to");
		if(from != null && to!=null) {
			Date fromDate = Date.valueOf(from);
			Date toDate = Date.valueOf(to);
			List<Expense> allExpenses = expenseRepository.findAllByDateBetween(fromDate, toDate);
			return ResponseEntity.ok(allExpenses);
		}
		Expense expense = expenseRepository.findByid(Long.valueOf(payload.get("id")));
		return ResponseEntity.ok(expense);
	}
	
	@PostMapping("/expense/create")
	public ResponseEntity<Expense> createExpense(@RequestBody Expense expense) {
		Expense savedExpense = expenseRepository.save(expense);		
		return ResponseEntity.ok(savedExpense);
	}
	
	@PostMapping("/expense/delete")
	public ResponseEntity<Map<String, String>> deleteExpense(@RequestBody Map<String, Long> payload){
		Long id = payload.get("id");
		expenseRepository.deleteById(id);	
		Map<String, String> response = new HashMap<>();
	    response.put("message", "Deleted expense id: " + id);
		return ResponseEntity.ok(response);
	}
	

	@PostMapping("/expense/update")
	public ResponseEntity<?> updateProduct(@RequestBody Expense expense) {
		
		Long id = expense.getId();
		if(id != null) {
			Expense savedExpense = expenseRepository.findByid(id);
			String expenseDescription = expense.getDescription();
			Integer expenseAmount = expense.getAmount();
			Date expenseDate = expense.getDate();

			if(expenseDescription!=null) {
				savedExpense.setDescription(expenseDescription);	
			}
			if(expenseAmount!=null) {
				savedExpense.setAmount(expenseAmount);
			}
			if(expenseDate!=null) {
				savedExpense.setDate(expenseDate);
			}
			
			expenseRepository.save(savedExpense);
			return ResponseEntity.ok(savedExpense);
		}
		return ResponseEntity.badRequest().body("Please provide expense id!");
	}
	
}










