package com.example.filter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import com.example.model.Session;
import com.example.repository.SessionRepository;

import java.io.IOException;
import java.util.List;

@Component
@Order(2) // Se ejecuta después del log
public class AuthenticationFilter extends OncePerRequestFilter 
{

	// --------------- DEPENDENCIAS --------------- //

    @Autowired
    private SessionRepository sessionRepository;

    // --------------- CONSTRUCTOR --------------- //
    
    // Lista de endpoints PÚBLICOS que no requieren token
    private static final List<String> PUBLIC_ENDPOINTS = List.of(
            "/api/sessions/login", // El login debe ser público para poder entrar
            "/h2-console"          // La base de datos H2 debe ser accesible
    );

    // ---------------- FILTRADO ----------------- //
    
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException 
    {
        String requestURI = request.getRequestURI();

        // Comprobar si es un endpoint público
        // (Nota: para H2 usamos startsWith porque carga muchos recursos internos)
        boolean isPublic = PUBLIC_ENDPOINTS.stream().anyMatch(requestURI::equals) || requestURI.startsWith("/h2-console");
        
        // Si es pulblico
        if( isPublic ) 
        {
        	// Permitimos el paso sin realizar ninguna validacion de autentificacion
            filterChain.doFilter( request , response );
            return;
        }

        // Obtener el token del Header "Authorization"
        // El formato estándar es: "Authorization: Bearer <token>" cualquier otro formato lo pasaremos por invalido
        String authHeader = request.getHeader("Authorization");

        // Si no conseguimos el token o el token es de no autorizado
        if( authHeader == null || !authHeader.startsWith("Bearer ") ) 
        {
        	// Mandamos un mensaje de error de no autorizacion
            response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Falta token de autenticacion o formato incorrecto (Bearer <token>)");
            return;
        }

        // Extraer el token limpio (quitar la palabra "Bearer ")
        String token = authHeader.substring(7);

        // Validar el token contra base de datos
        Session session = sessionRepository.findByTokenAndActive(token, true);

        // Si no obtenemos ninguna session
        if (session == null) 
        {
        	// Mandamos un mensaje de error de no autorizacion
            response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Token invalido, expirado o sesion cerrada");
            return;
        }

        // Si hemos llegado hasta aqui todo está bien, continuamos
        filterChain.doFilter(request, response);
    }
}