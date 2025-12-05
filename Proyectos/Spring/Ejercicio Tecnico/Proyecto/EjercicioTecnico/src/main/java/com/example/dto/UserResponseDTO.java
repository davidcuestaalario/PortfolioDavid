package com.example.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;

/**
 * Las clases DTO se utilizan como paquetes de infromación de transferencia entre los distintos modulos de la aplicacion
 * La clase UserResponseDto contiene toda la informacion no sensible para enviar datos al cliente sin comprometer datos como la contraseña
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserResponseDTO
{
    
    private Long id;
    private String username;
    private String role;
    private Boolean blocked;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

}