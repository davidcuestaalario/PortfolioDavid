package com.example.model;

import jakarta.persistence.*;
import lombok.Data; 
import java.time.LocalDateTime;

@Entity
@Table(name = "T_SESSION")
@Data
public class Session 
{

	// ---------------- ATRIBUTOS ---------------- //
	
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // Relación ManyToOne: Muchas sesiones pueden pertenecer a un usuario
    @ManyToOne(fetch = FetchType.LAZY) 
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(nullable = false, unique = true)
    private String token; // Crucial para la autenticación

    @Column(name = "ip_address", nullable = false)
    private String ipAddress;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(nullable = false)
    private Boolean active = true; 

    // --------------- CONSTRUCTOR --------------- //

    @PrePersist
    protected void onCreate() {
        this.createdAt = LocalDateTime.now();
    }
}