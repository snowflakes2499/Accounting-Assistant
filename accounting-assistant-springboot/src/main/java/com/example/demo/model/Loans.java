package com.example.demo.model;

import jakarta.persistence.*;

@Entity
public class Loans {
	
	@Id
	private String personName;
		
	private String loanType;
	
	private Integer loanAmount;
	
	private String description;
	
	private String email;
	
	public String getdescription() {return this.description;}
	public void setdescription(String description) {this.description = description;}
	
	public String getPersonName() { return this.personName; }
	public void setPersonName(String personName) { this.personName = personName; }
	
	public String getLoanType() { return this.loanType; }
	public void setLoanType(String loanType) { this.loanType = loanType; }

	public String getEmail() { return this.email; }
	public void setEmail(String email) { this.email= email; }
			
	public Integer getLoanAmount(){ return this.loanAmount; }
	public void setLoanAmount(Integer loanAmount) { this.loanAmount= loanAmount; }
}
