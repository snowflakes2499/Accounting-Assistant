package com.example.demo.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.model.Transactions;

public interface TransactionRepository extends JpaRepository<Transactions, Long>{
	
	Transactions findByid(Long id);
	void deleteByid(Long id);
}
