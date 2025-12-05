package com.example.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.example.dto.SessionResponseDTO;
import com.example.mapper.SessionMapper;
import com.example.model.Session;
import com.example.model.User;
import com.example.repository.SessionRepository;
import com.example.repository.UserRepository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Service
public class SessionService 
{
	// --------------- DEPENDENCIAS --------------- //

    private final UserRepository userRepository;
    private final SessionRepository sessionRepository;
    private final SessionMapper sessionMapper;

    // --------------- CONSTRUCTOR --------------- //
    
    @Autowired
    public SessionService( UserRepository userRepository , SessionRepository sessionRepository , SessionMapper sessionMapper ) 
    {
        this.userRepository = userRepository;
        this.sessionRepository = sessionRepository;
        this.sessionMapper = sessionMapper;
    }
    
    // --------------- ABRIR SESION -------------- //

    /**
     * Verifica credenciales y genera una nueva sesión con token.
     */
    @Transactional
    public Optional<SessionResponseDTO> login(String username, String password, String ipAddress) {
        // 1. Buscar usuario
        User user = userRepository.findByUsername(username);

        // 2. Validaciones básicas
        if (user == null) return Optional.empty();
        if (!user.getPassword().equals(password)) return Optional.empty(); // En producción usaríamos BCrypt
        if (user.getBlocked()) return Optional.empty();

        // 3. Generar Token único
        String token = UUID.randomUUID().toString();

        // 4. Crear y guardar la sesión
        Session session = new Session();
        session.setUser(user);
        session.setToken(token);
        session.setIpAddress(ipAddress);
        session.setActive(true);

        Session savedSession = sessionRepository.save(session);
        return Optional.of(sessionMapper.toDto(savedSession));
    }
    
    // -------------- CERRAR SESION -------------- //

    /**
     * Cerrar una sesión específica por token
     */
    @Transactional
    public boolean logout(String token) 
    {
        Session session = sessionRepository.findByTokenAndActive(token, true);
        if (session != null) {
            session.setActive(false);
            sessionRepository.save(session);
            return true;
        }
        return false;
    }

    /**
     * Cerrar todas las sesiones de un usuario
     */
    @Transactional
    public int logoutAllUserSessions(Long userId) 
    {
        List<Session> activeSessions = sessionRepository.findByUserIdAndActive(userId, true);
        activeSessions.forEach(s -> s.setActive(false));
        sessionRepository.saveAll(activeSessions);
        return activeSessions.size();
    }
    
    // ---------------- BUSQUEDAS ---------------- //

    /**
     * Listar las sesiones activas
     */
    @Transactional(readOnly = true)
    public List<SessionResponseDTO> findAllActiveSessions() 
    {
        return sessionMapper.toDto(sessionRepository.findByActive(true));
    }
}