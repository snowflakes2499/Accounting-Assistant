package com.example.demo.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.model.SellingLedger;

public interface SellingLedgerRepository extends JpaRepository<SellingLedger, Long>{
	SellingLedger findByid(Long id);
}
