package com.example.mapper;

import org.springframework.stereotype.Component;

import com.example.dto.UserRequestDTO;
import com.example.dto.UserResponseDTO;
import com.example.model.User;

import java.util.List;
import java.util.stream.Collectors;

@Component
public class UserMapper 
{

    // ------------- DTO a ENTIDAD ------------- //
    
    /**
     * Convierte un UserRequestDto a la entidad User.
     */
    public User toEntity( UserRequestDTO dto ) 
    {
    	// Si el dto es nulo, finalizamos el procedimiento
        if (dto == null) { return null; }
        // Generamsos una nueva entidad
        User entity = new User();
        // Mapeo directo de los campos del DTO
        entity.setUsername(dto.getUsername());
        entity.setPassword(dto.getPassword());
        entity.setRole(dto.getRole());
        
        // Si el campo 'blocked' no se incluye en el DTO, mantenemos el valor por defecto de la entidad (false)
        if (dto.getBlocked() != null) {
            entity.setBlocked(dto.getBlocked());
        }

        return entity;
    }

    // ------------- ENTIDAD a DTO ------------- //
    
    /**
     * Convierte la entidad User a un UserResponseDTO.
     */
    public UserResponseDTO toDto( User entity ) 
    {
    	// Si la entidad es nula, finalizamos el procedimiento
        if (entity == null) { return null; }
        // Generamos un nuevo Usuario
        UserResponseDTO dto = new UserResponseDTO();
        // Mapeo de campos para la respuesta
        dto.setId(entity.getId());
        dto.setUsername(entity.getUsername());
        dto.setRole(entity.getRole());
        dto.setBlocked(entity.getBlocked());
        dto.setCreatedAt(entity.getCreatedAt());
        dto.setUpdatedAt(entity.getUpdatedAt());
        
        return dto;
    }
    
    /**
     * Convierte una lista de entidades User a una lista de UserResponseDTOs.
     */
    public List<UserResponseDTO> toDto(List<User> entities) 
    {
        return entities.stream()
            .map(this::toDto)
            .collect(Collectors.toList());
    }
}