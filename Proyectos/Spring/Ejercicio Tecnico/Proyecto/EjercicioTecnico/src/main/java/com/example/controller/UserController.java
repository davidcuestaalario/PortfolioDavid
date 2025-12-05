package com.example.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.example.dto.UserRequestDTO;
import com.example.dto.UserResponseDTO;
import com.example.service.UserService;

import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController 
{
	// --------------- DEPENDENCIAS --------------- //

    @Autowired
    private UserService userService;
    
    // --------------- CONSTRUCTOR --------------- //
    
    // ------------- OBTENER USUARIOS  ----------- //

    // POST /api/users?role=ADMIN&username=juan
    @GetMapping
    public ResponseEntity<List<UserResponseDTO>> getAllUsers
    (
        @RequestParam( value = "role" , required = false) String role,
        @RequestParam( value = "username" , required = false) String username
    ) 
    {
        // Llamamos al servicio pasando los parámetros (que pueden ser null)
        List<UserResponseDTO> users = userService.findAllUsers( role , username );
        return ResponseEntity.ok(users);
    }
    
    // -------------- CREAR USUARIOS  ------------ //
    
    @PostMapping
    public ResponseEntity<UserResponseDTO> createUser(@RequestBody UserRequestDTO userDto) 
    {
        UserResponseDTO createdUser = userService.createUser(userDto);
        return new ResponseEntity<>(createdUser, HttpStatus.CREATED);
    }

    // -------------- EDITAR USUARIOS  ----------- //
    
    @PutMapping("/{id}")
    public ResponseEntity<UserResponseDTO> updateUser(@PathVariable("id") Long id, @RequestBody UserRequestDTO userDetails) 
    {
        return userService.updateUser(id, userDetails)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    // ------------ BLOQUEAR USUARIOS  ----------- //
    
    @PatchMapping("/{id}/block")
    public ResponseEntity<UserResponseDTO> blockUser(@PathVariable("id") Long id) 
    {
        return userService.blockUser(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }
}