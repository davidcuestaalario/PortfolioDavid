package com.example.filter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.core.annotation.Order;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.time.LocalDateTime;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

// Este es el filtro que cuenta el numero de accesos de una misma IP y lo bloquea si supera el limite establecido
// Queremos que este sea el PRIMER filtro. Dado que si alguien ataca, lo bloqueamos antes de gastar recursos en Logs o Autenticación. 
@Component
@Order(1) 
public class RateLimitFilter extends OncePerRequestFilter 
{

	// --------------- DEPENDENCIAS --------------- //

	// ----------------- VARIABLES ---------------- //
	
    // Numero máximo de peticiones
    private static final int MAX_REQUESTS = 10;
    
    // Almacén en memoria: IP -> Datos de control
    // Usamos ConcurrentHashMap porque en una API pueden entrar muchas peticiones a la vez (hilos concurrentes) y ConcurrentHashMap es "thread-safe"
    private final Map<String,RequestControl> cache = new ConcurrentHashMap<>();

    // Clase interna sencilla para guardar los datos
    private static class RequestControl 
    {
        int count;
        LocalDateTime expirationTime;
        public RequestControl( int count , LocalDateTime expirationTime ){ this.count = count; this.expirationTime = expirationTime; }
    }

    // ---------------- FILTRADO ----------------- //
    
    @Override
    protected void doFilterInternal( HttpServletRequest request , HttpServletResponse response , FilterChain filterChain ) throws ServletException , IOException
    {
        // Obtener la IP del cliente
        String ipClient = request.getRemoteAddr();

        // Limpieza (Opcional pero recomendada): 
        // Si la entrada actual ha caducado, la borramos para empezar de cero
        // (compute es una operación atómica de Java Maps)
        cache.compute( ipClient , ( key , control ) -> 
        {
            // Si no existe o no es vcalido, Creamos uno nuevo con una petición y expiración en un minuto
            if( control == null || LocalDateTime.now().isAfter(control.expirationTime) ) 
            {
                return new RequestControl(1, LocalDateTime.now().plusMinutes(1));
            }
            // Si existe y es válido, Aumentamos el contador
            control.count++;
            return control;
        });

        // Verificamos si se pasó del límite
        RequestControl currentControl = cache.get(ipClient);
        if (currentControl.count > MAX_REQUESTS) 
        {
            // Bloqueamos la peticion y devolvemos error 429 (Too Many Requests)
            response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
            // Mostramos un mensaje indicando lo sucedido
            response.getWriter().write("Has excedido el limite de 10 peticiones por minuto.");
            // Cortamos la ejecución para no llamar al filtro de autentificacion
            return; 
        }

        // Si hemos llegado hasta aqui es porque aun estamos dentro de los limites
        // Llamamos al siguiente filtro
        filterChain.doFilter(request, response);
    }
}