package com.example.demo.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.model.Transcript;

public interface TranscriptRepository extends JpaRepository<Transcript, Long>{
	Transcript findByid(Long id);
	Transcript findTopByOrderByIdDesc();

}
