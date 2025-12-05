package com.example.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

import com.example.model.User;

public interface UserRepository extends JpaRepository<User, Long> {

    // Spring Data JPA crea automáticamente la consulta SQL a partir de este nombre de método
    User findByUsername(String username);
    
    // Buscar usuarios que contengan el texto (ignorando mayúsculas/minúsculas)
    List<User> findByUsernameContainingIgnoreCase(String username);

    // Buscar usuarios por rol exacto
    List<User> findByRole(String role);
    
    // Buscar por rol Y parte del nombre
    List<User> findByRoleAndUsernameContainingIgnoreCase(String role, String username);

}