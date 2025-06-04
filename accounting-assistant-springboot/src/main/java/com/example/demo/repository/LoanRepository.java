package com.example.demo.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.model.Loans;

public interface LoanRepository extends JpaRepository<Loans, String>{
	Loans findBypersonName(String personName);	
}
