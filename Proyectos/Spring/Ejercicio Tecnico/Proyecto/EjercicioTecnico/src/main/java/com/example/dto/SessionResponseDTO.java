package com.example.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SessionResponseDTO 
{
	// ---------------- ATRIBUTOS ---------------- //
	
    private Long id;
    private String token;
    private Long userId; // Devolvemos solo el ID del usuario, no el objeto entero
    private String ipAddress;
    private LocalDateTime createdAt;
    private Boolean active;
}