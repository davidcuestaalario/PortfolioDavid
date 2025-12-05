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

@Component
@Order(1) // Este filtro se ejecuta primero
@Slf4j // Anotación de Lombok para generar automáticamente el objeto 'log'
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