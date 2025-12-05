package com.example.mapper;

import org.springframework.stereotype.Component;

import com.example.dto.SessionResponseDTO;
import com.example.model.Session;

import java.util.List;
import java.util.stream.Collectors;

@Component
public class SessionMapper 
{

    // ------------- ENTIDAD a DTO ------------- //
    
    /** Convierte Entidad -> DTO */
    public SessionResponseDTO toDto( Session entity ) 
    {
        if (entity == null) { return null; }
        SessionResponseDTO dto = new SessionResponseDTO();
        dto.setId(entity.getId());
        dto.setToken(entity.getToken());
        
        // Obtenemos el ID del usuario de la relación
        if (entity.getUser() != null) { dto.setUserId(entity.getUser().getId()); }
        
        dto.setIpAddress(entity.getIpAddress());
        dto.setCreatedAt(entity.getCreatedAt());
        dto.setActive(entity.getActive());

        return dto;
    }

    /** Convierte Lista de Entidades -> Lista de DTOs */
    public List<SessionResponseDTO> toDto(List<Session> entities) 
    {
        return entities.stream().map(this::toDto).collect(Collectors.toList());
    }
    
}