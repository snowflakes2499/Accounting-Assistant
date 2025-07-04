package com.example.demo.repository;

import java.sql.Date;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.model.Expense;

public interface ExpenseRepository extends JpaRepository<Expense, Long>{
	Expense findByid(Long id);
	List<Expense> findAllByDateBetween(Date from, Date to);

}
