package com.example.service;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;

import com.example.dto.SessionResponseDTO;
import com.example.mapper.SessionMapper;
import com.example.model.Session;
import com.example.model.User;
import com.example.repository.SessionRepository;
import com.example.repository.UserRepository;

import java.util.Arrays;
import java.util.List;
import java.util.Optional;

@ExtendWith(MockitoExtension.class)
public class SessionServiceTest 
{

	// --------------- DEPENDENCIAS --------------- //
	
    @Mock private UserRepository userRepository;
    @Mock private SessionRepository sessionRepository;
    @Mock private SessionMapper sessionMapper;

    @InjectMocks
    private SessionService sessionService;
    
	// --------------- TEST LOGIN --------------- //
	
    @Test
    void testLogin_Success() 
    {
        // PREPARACION
        String username = "admin";
        String password = "password123";
        String ip = "127.0.0.1";
        // Simulamos un usuario válido en BD
        User user = new User();
        user.setUsername(username);
        user.setPassword(password); // La contraseña coincide
        user.setBlocked(false);     // No está bloqueado
        // Simulamos la sesión guardada
        Session savedSession = new Session();
        savedSession.setId(1L);
        savedSession.setToken("token-generado-uuid");
        // Simulamos el DTO de respuesta
        SessionResponseDTO responseDTO = new SessionResponseDTO();
        responseDTO.setToken("token-generado-uuid");
        // Mocks behavior
        Mockito.when(userRepository.findByUsername(username)).thenReturn(user);
        // Cuando guarde cualquier sesión, devuelve la nuestra
        Mockito.when(sessionRepository.save(Mockito.any(Session.class))).thenReturn(savedSession);
        Mockito.when(sessionMapper.toDto(savedSession)).thenReturn(responseDTO);
        Optional<SessionResponseDTO> result = sessionService.login(username, password, ip);
        // VERIFICACION
        Assertions.assertTrue(result.isPresent());
        Assertions.assertEquals("token-generado-uuid", result.get().getToken());
        // Verificamos que se guardó la sesión
        Mockito.verify(sessionRepository).save(Mockito.any(Session.class));
    }

    @Test
    void testLogin_WrongPassword() 
    {
        // PREPARACION
        String username = "admin";
        User user = new User();
        user.setUsername(username);
        user.setPassword("admin123"); 
        // ENTRENAMIENTO
        Mockito.when(userRepository.findByUsername(username)).thenReturn(user);
        // Intentamos login con contraseña INCORRECTA
        Optional<SessionResponseDTO> result = sessionService.login(username, "passwordMala", "127.0.0.1");
        // VERIFICACION
        Assertions.assertTrue(result.isEmpty());
        // Asegurar que NO se guardó ninguna sesión
        Mockito.verify(sessionRepository, Mockito.never()).save(Mockito.any());
    }

    @Test
    void testLogin_UserBlocked() 
    {
        // PREPARACION
        String username = "bloqueado";
        User user = new User();
        user.setUsername(username);
        user.setPassword("password123");
        user.setBlocked(true); // ¡Usuario bloqueado!
        // ENTRENAMIENTO
        Mockito.when(userRepository.findByUsername(username)).thenReturn(user);
        // Login con contraseña correcta pero usuario bloqueado
        Optional<SessionResponseDTO> result = sessionService.login(username, "password123", "127.0.0.1");
        // VERIFICACION 
        Assertions.assertTrue(result.isEmpty());
        Mockito.verify(sessionRepository, Mockito.never()).save(Mockito.any());
    }

	// --------------- TEST LOGOUT --------------- //
	
    @Test
    void testLogout_Success() 
    {
        // PREPARACION
        String token = "mi-token-secreto";
        Session activeSession = new Session();
        activeSession.setToken(token);
        activeSession.setActive(true);
        // Simulamos que encontramos la sesión
        Mockito.when(sessionRepository.findByTokenAndActive(token, true)).thenReturn(activeSession);
        // VERIFICACION 
        boolean result = sessionService.logout(token);
        Assertions.assertTrue(result);
        Assertions.assertFalse(activeSession.getActive()); // Debe haber cambiado a false en memoria
        Mockito.verify(sessionRepository).save(activeSession); // Debe haberse guardado el cambio
    }

    @Test
    void testLogout_NotFound() 
    {
        // PREPARACION
        String token = "token-falso";
        // Simulamos que NO encontramos nada
        Mockito.when(sessionRepository.findByTokenAndActive(token, true)).thenReturn(null);
        // VERIFICACION 
        boolean result = sessionService.logout(token);
        Assertions.assertFalse(result);
        Mockito.verify(sessionRepository, Mockito.never()).save(Mockito.any());
    }

    @Test
    void testLogoutAllUserSessions() 
    {
        // PREPARACION
        Long userId = 1L;
        // Creamos dos sesiones activas falsas
        Session s1 = new Session(); s1.setActive(true);
        Session s2 = new Session(); s2.setActive(true);
        List<Session> sessions = Arrays.asList(s1, s2);
        // ENTRENAMIENTO
        Mockito.when(sessionRepository.findByUserIdAndActive(userId, true)).thenReturn(sessions);
        // VERIFICACION 
        int count = sessionService.logoutAllUserSessions(userId);
        Assertions.assertEquals(2, count);
        Assertions.assertFalse(s1.getActive()); // Verificamos que las desactivó
        Assertions.assertFalse(s2.getActive());    
        // Verificamos que guardó la lista entera
        Mockito.verify(sessionRepository).saveAll(sessions);
    }
}