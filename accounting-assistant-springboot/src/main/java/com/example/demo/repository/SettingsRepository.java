package com.example.demo.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.example.demo.model.Settings;

public interface SettingsRepository extends JpaRepository<Settings, String>{
	
	Settings findByoperation(String operation);

}
