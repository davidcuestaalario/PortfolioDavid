package com.example.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.dto.UserRequestDTO;
import com.example.dto.UserResponseDTO;
import com.example.mapper.UserMapper;
import com.example.model.User;
import com.example.repository.UserRepository;

import java.util.List;
import java.util.Optional;

@Service
public class UserService 
{
	// --------------- DEPENDENCIAS --------------- //

    private final UserRepository userRepository;
    private final UserMapper userMapper;

    // --------------- CONSTRUCTOR --------------- //
    
    @Autowired
    public UserService( UserRepository userRepository , UserMapper userMapper ) 
    {
        this.userRepository = userRepository;
        this.userMapper = userMapper;
    }

    // --------------- OPERACIONES --------------- //

    // BUSQUEDAS
    
    /**
     * Obtener usuarios con filtros opcionales.
     * Si no llegan filtros, devuelve todos.
     */
    @Transactional(readOnly = true)
    public List<UserResponseDTO> findAllUsers( String role, String username ) 
    {
        // Inicializamos una nueva lista de usuarios
    	List<User> users;
    	// Si el rol y el nombre no estan vacios
        if( role != null && username != null ) 
        {
            users = userRepository.findByRoleAndUsernameContainingIgnoreCase(role, username);
        } 
        // Si el rol no esta vacio pero el usuario si, Buscamos por rol
        else if (role != null) 
        {
            users = userRepository.findByRole(role);
        } 
        // Si el usuario no esta vacio pero el rol si, Buscamos por nombre
        else if (username != null) 
        {
            users = userRepository.findByUsernameContainingIgnoreCase(username);
        } 
        // Si tanto el rol como el nombre estan vacios, No aplicamos filtros
        else 
        {
            users = userRepository.findAll();
        }
        // Devolvemos la lista de usuarios filtrados
        return userMapper.toDto(users);
    }

    // Obtener un usuario por ID
    @Transactional(readOnly = true)
    public Optional<UserResponseDTO> findUserById(Long id) 
    {
    	// Si existe lo convierte a DTO para devolverlo
        return userRepository.findById(id).map(userMapper::toDto);
    }

    // CREAR
    
    @Transactional
    public UserResponseDTO createUser(UserRequestDTO userDto) 
    {
        // Convertimos el DTO de entrada a Entidad de base de datos
        User user = userMapper.toEntity(userDto);
        // Guardamos en BD
        User savedUser = userRepository.save(user);
        // Devolvemos el DTO de respuesta (sin contraseña)
        return userMapper.toDto(savedUser);
    }
    
    // EDITAR 
    
    // Actualizar completamente un usuario
    @Transactional
    public Optional<UserResponseDTO> updateUser(Long id, UserRequestDTO userDetails) 
    {
        return userRepository.findById(id).map( user -> 
        {
            // Actualizamos los campos
            user.setUsername(userDetails.getUsername());
            // Solo actualizamos contraseña si viene una nueva
            if (userDetails.getPassword() != null && !userDetails.getPassword().isEmpty()) 
            {
                user.setPassword(userDetails.getPassword());
            }
            
            user.setRole(userDetails.getRole());
            
            // si el valor de bloqueo no tiene valor no lo actualizamos
            if( userDetails.getBlocked() != null) { user.setBlocked(userDetails.getBlocked()); }

            // Guardamos los cambios
            User updatedUser = userRepository.save(user);
            return userMapper.toDto(updatedUser);
        });
    }

    // Bloquear un usuario
    @Transactional
    public Optional<UserResponseDTO> blockUser(Long id) 
    {
        return userRepository.findById(id).map(user -> 
        {
            user.setBlocked(true);
            User savedUser = userRepository.save(user);
            return userMapper.toDto(savedUser);
        });
    }
}