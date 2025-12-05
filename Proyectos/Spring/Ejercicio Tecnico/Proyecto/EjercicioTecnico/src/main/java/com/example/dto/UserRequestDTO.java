package com.example.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;

/**
 * Las clases DTO se utilizan como paquetes de infromación de transferencia entre los distintos modulos de la aplicacion
 * La clase UserRequestDto contiene toda la informacion necesaria para operar sobre los usuarios
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserRequestDTO 
{
	// ---------------- ATRIBUTOS ---------------- //

    private String username;
    private String password; 
    private String role;     
    private Boolean blocked;
}
