package com.example.demo.model;

import java.math.BigDecimal;

import jakarta.persistence.*;

@Entity
public class SellingLedger {
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	
	private Long soldProductId;
	
	private Integer soldProductQuantity;
	
	private BigDecimal soldProductActualPrice;
	
	private BigDecimal soldProductSellingPrice;
	
	private BigDecimal soldProductTax;
	
	private BigDecimal soldAmount;
	
	private String productName;
	
	public Long getId() { return this.id; }
	
	public Long getSoldProductId() { return this.soldProductId; }
	public void setSoldProductId(Long soldProductId) { this.soldProductId = soldProductId; }
	
	public Integer getSoldProductQuantity() { return this.soldProductQuantity; }
	public void setSoldProductQuantity(Integer soldProductQuantity) { this.soldProductQuantity = soldProductQuantity; }
	
	public BigDecimal getSoldProductSellingPrice() { return this.soldProductSellingPrice; }
	public void setSoldProductSellingPrice(BigDecimal soldProductSellingPrice) { this.soldProductSellingPrice = soldProductSellingPrice; }
		
	public BigDecimal getSoldProductActualPrice() { return this.soldProductActualPrice; }
	public void setSoldProductActualPrice(BigDecimal soldProductActualPrice) { this.soldProductActualPrice = soldProductActualPrice; }
	
	public BigDecimal getSoldAmount() { return this.soldAmount; }
	public void setSoldAmount(BigDecimal soldAmount) { this.soldAmount = soldAmount; }
	
	public BigDecimal getProductTax() { return this.soldProductTax; }
	public void setSoldProductTax(BigDecimal soldProductTax) { this.soldProductTax = soldProductTax; }
	
	public String getProductName() { return this.productName; }
	public void setProductName(String productName) { this.productName = productName; }
	
	
}
