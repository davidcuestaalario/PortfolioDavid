package com.example.filter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.time.LocalDateTime;

// Est e es el filtro que registra los accesos al sistema y los muestra por LOG
// utilizamos anotaciónes de Lombok para generar automáticamente el objeto 'log'
// Queremos que este sea el SEGUNDO filtro, justo despues del detector de limites
@Component
@Order(2) 
@Slf4j 
public class RequestLogFilter extends OncePerRequestFilter 
{
    // ---------------- FILTRADO ----------------- //
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException , IOException 
    {
        // Registrar la entrada (Timestamp, Método, URI)
        log.info("ENTRADA -> Timestamp: {} | Método: {} | Endpoint: {}" , LocalDateTime.now() , request.getMethod() , request.getRequestURI() );

        // Dejar pasar la petición al siguiente eslabón (otro filtro o el controlador)
        long startTime = System.currentTimeMillis();
        filterChain.doFilter(request, response);
        long duration = System.currentTimeMillis() - startTime;

        // Registrar la salida (Código de estado y tiempo que tardó)
        log.info("SALIDA  <- Status: {} | Tiempo: {} ms" ,  response.getStatus() , duration);
    }
}