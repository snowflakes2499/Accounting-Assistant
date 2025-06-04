package com.example.demo.model;


import jakarta.persistence.*;

@Entity
public class Settings {
	
	@Id
	private String operation;
	private String status;

	public String getOperation() { return this.operation; }
	public void setOperation(String operation) { this.operation = operation; }
	
	public String getStatus() { return this.status; }
	public void setStatus(String status) {this.status= status; }
}
