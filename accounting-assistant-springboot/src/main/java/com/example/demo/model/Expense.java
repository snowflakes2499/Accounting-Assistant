package com.example.demo.model;

import java.sql.Date;

import jakarta.persistence.*;

@Entity
public class Expense {

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	
	private String description;
	
	private Date date;
	
	private Integer amount;
	
	public Long getId() {return this.id;}
	
	public Date getDate() {return this.date;}
	public void setDate(Date date) { this.date = date; }

	public Integer getAmount() { return this.amount; }
	public void setAmount(Integer amount) { this.amount = amount; }
	
	public String getDescription() { return this.description;}
	public void setDescription(String description) { this.description = description; }
	
}
