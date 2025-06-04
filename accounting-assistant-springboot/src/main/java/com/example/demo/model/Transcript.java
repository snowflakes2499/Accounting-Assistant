package com.example.demo.model;

import jakarta.persistence.*;

@Entity
public class Transcript {
	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
	private Long id;
	private String  Transcript;
	
    public Long getId() { return id; }

	public String getTranscript() {return this.Transcript;}
	public void setTranscript(String Transcript) {this.Transcript = Transcript;}
}
