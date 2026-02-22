package mercadona_prueba.excepciones;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.HashMap;
import java.util.Map;

// NOTA:
// Esta clase es  como un vigilante. Se queda escuchando en toda la aplicación y, 
// si algún controlador lanza un IllegalArgumentException o un RuntimeException, 
// lo atrapa, extrae el mensaje personalizado y lo devuelve en formato JSON con un código de error adecuado

/**
 * Esta clase manejará los errores de todos los controladores
 */
@RestControllerAdvice 
public class GlobalExceptionHandler 
{
    // Atrapa los errores de validación de negocio (las horas, etc.)
    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<Map<String, String>> handleIllegalArgumentException(IllegalArgumentException ex) 
    {
        Map<String, String> respuesta = new HashMap<>();
        // Extraemos el mensaje personalizado
        respuesta.put("error", ex.getMessage()); 
        // Devolvemos un 400 (Petición incorrecta del usuario)
        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(respuesta);
    }

    // Atrapa los errores de cuando no encontramos algo en la BD (Trabajador no encontrado, etc.)
    @ExceptionHandler(RuntimeException.class)
    public ResponseEntity<Map<String, String>> handleRuntimeException(RuntimeException ex) 
    {
        Map<String, String> respuesta = new HashMap<>();
        // Extraemos el mensaje personalizado
        respuesta.put("error", ex.getMessage());
        // Devolvemos un 404 (No encontrado)
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(respuesta);
    }
}