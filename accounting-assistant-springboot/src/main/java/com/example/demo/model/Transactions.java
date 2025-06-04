package com.example.demo.model;

import jakarta.persistence.*;

@Entity
public class Transactions {

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	
	private String personName;
	
	private String loanType;
	
	private Integer loanAmount;
	
	private String description;

	
	public String getdescription() {return this.description;}
	public void setdescription(String description) {this.description = description;}
	
	public Long getid() { return this.id; }
	
	public String getPersonName() { return this.personName; }
	public void setPersonName(String personName) { this.personName = personName; }
	
	public String getLoanType() { return this.loanType; }
	public void setLoanType(String loanType) { this.loanType = loanType; }
		
	public Integer getLoanAmount(){ return this.loanAmount; }
	public void setLoanAmount(Integer loanAmount) { this.loanAmount= loanAmount; }
}
