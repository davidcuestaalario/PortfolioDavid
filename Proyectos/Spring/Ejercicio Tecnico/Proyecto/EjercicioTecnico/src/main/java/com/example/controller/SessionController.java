package com.example.controller;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.example.dto.LoginRequestDTO;
import com.example.dto.SessionResponseDTO;
import com.example.service.SessionService;

import java.util.List;

@RestController
@RequestMapping("/api/sessions")
public class SessionController 
{
	// --------------- DEPENDENCIAS --------------- //

    private final SessionService sessionService;

    // --------------- CONSTRUCTOR --------------- //
    
    @Autowired
    public SessionController(SessionService sessionService) 
    {
        this.sessionService = sessionService;
    }

    // --------------- ABRIR SESION -------------- //

    @PostMapping("/login")
    public ResponseEntity<SessionResponseDTO> login(@RequestBody LoginRequestDTO loginDto, HttpServletRequest request) 
    {
        // Obtenemos la IP desde la petición HTTP (requisito funcional)
        String ipAddress = request.getRemoteAddr();

        // Llamamos al servicio
        return sessionService.login(loginDto.getUsername(), loginDto.getPassword(), ipAddress)
                .map(session -> new ResponseEntity<>(session, HttpStatus.OK))
                .orElseGet(() -> new ResponseEntity<>(HttpStatus.UNAUTHORIZED)); // 401 si falla la auth
    }

    // -------------- CERRAR SESION -------------- //
    
    /**
     * Cerrar sesión una session
     * POST /api/sessions/logout?token=XXXXX
     */
    @PostMapping("/logout")
    public ResponseEntity<Void> logout(@RequestParam("token") String token) 
    {
        boolean closed = sessionService.logout(token);
        if (closed) 
        {
            return ResponseEntity.ok().build(); // 200 OK
        } 
        else 
        {
            return ResponseEntity.notFound().build(); // 404 Si el token no existe o ya estaba cerrada
        }
    }

    /**
     * Cerrar todas las sesiones de un usuario.
     * POST /api/sessions/logout-all?userId=123
     */
    @PostMapping("/logout-all")
    public ResponseEntity<String> logoutAll(@RequestParam("userId") Long userId) 
    {
        int count = sessionService.logoutAllUserSessions(userId);
        return ResponseEntity.ok("Se han cerrado " + count + " sesiones para el usuario " + userId);
    }
    
    // ---------------- BUSQUEDAS ---------------- //

    /**
     * Listar sesiones activas.
     * GET /api/sessions
     */
    @GetMapping
    public ResponseEntity<List<SessionResponseDTO>> getActiveSessions() 
    {
        return ResponseEntity.ok(sessionService.findAllActiveSessions());
    }
}