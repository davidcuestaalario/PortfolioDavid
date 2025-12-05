package com.example.model;

import jakarta.persistence.*;
import lombok.Data; 
import java.time.LocalDateTime;

@Entity
@Table(name = "T_USER")
@Data
public class User 
{
	
	// ---------------- ATRIBUTOS ---------------- //

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String password;

    @Column(nullable = false)
    private String role;

    @Column(nullable = false)
    private Boolean blocked = false;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    // --------------- CONSTRUCTOR --------------- //

    @PrePersist
    protected void onCreate() 
    {
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() 
    {
        this.updatedAt = LocalDateTime.now();
    }
}