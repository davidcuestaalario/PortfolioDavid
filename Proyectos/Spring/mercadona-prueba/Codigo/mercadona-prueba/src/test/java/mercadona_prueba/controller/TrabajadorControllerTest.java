package mercadona_prueba.controller;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doThrow;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.Collections;

import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.bean.override.mockito.MockitoBean;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import mercadona_prueba.mapper.TrabajadorMapper;
import mercadona_prueba.model.Trabajador;
import mercadona_prueba.service.TrabajadorService;

@WebMvcTest(TrabajadorController.class) // Levanta SOLO la capa web
public class TrabajadorControllerTest 
{
    // -- --------- --
    // -- TODO MOKS --
    // -- --------- --
    
    // No queremos tocar la base de datos real en los tests unitarios.
	// Falsificamos Postman
    @Autowired private MockMvc mockMvc; 
    // Falsificamos el servicio
    @MockitoBean private TrabajadorService trabajadorService; 
    // Falsificamos el mapper
    @MockitoBean private TrabajadorMapper trabajadorMapper; 

    // -- -------------------- --
    // -- TODO ASIGNAR SECCION --
    // -- -------------------- --
    
    @Test
    void asignarSeccion_LlamadaCorrecta_Devuelve200OK() throws Exception 
    {
        // Creamos un JSON que simula la petición del cliente
        String jsonBody = """
            {
                "nombreSeccion": "Horno",
                "horas": 4
            }
            """;
        
        // Simulamos un POST y esperamos un HTTP 200 OK
        mockMvc.perform(post("/api/trabajadores/11111111A/asignaciones")
                .contentType(MediaType.APPLICATION_JSON)
                .content(jsonBody))
                .andExpect(status().isOk())
                .andExpect(content().string("Operación de asignación procesada correctamente para el trabajador 11111111A"));
    }

    @Test
    void asignarSeccion_ReglaDeNegocioRota_Devuelve400BadRequest() throws Exception 
    {
    	// Creamos un JSON que simula la petición del cliente
        String jsonBody = """
            {
                "nombreSeccion": "Horno",
                "horas": 20
            }
            """;
        // Indicamos a Mokito que cuando el service intente asignar al trabajador, lance un error
        doThrow(new IllegalArgumentException("El trabajador no tiene suficientes horas disponibles")).when(trabajadorService).asignarTrabajadorToSeccion(anyString(), anyString(), anyInt());

        // Simulamos el POST y esperamos que el GlobalExceptionHandler lo cace y devuelva HTTP 400
        mockMvc.perform(post("/api/trabajadores/11111111A/asignaciones")
                .contentType(MediaType.APPLICATION_JSON)
                .content(jsonBody))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.error").value("El trabajador no tiene suficientes horas disponibles"));
    }

    // -- ----------------------- --
    // -- TODO: OBTENER USUARIOS  --
    // -- ----------------------- --

    @Test
    void obtenerTodos_DevuelveListaY200OK() throws Exception 
    {
    	// Indicamos a Mokito que el servicio devuelve una lista vacía
        Mockito.when(trabajadorService.obtenerTodos()).thenReturn(Collections.emptyList());
        // Ejecutamos esperamos un 200 OK
        mockMvc.perform(get("/api/trabajadores")).andExpect(status().isOk());
    }

    // -- ----------------------- --
    // -- TODO: CREAR TRABAJADOR  --
    // -- ----------------------- --

    @Test
    void crearTrabajador_DatosValidos_Devuelve201Created() throws Exception 
    {
    	// Creamos un JSON que simula la petición del cliente
        String jsonBody = """
            {
                "dni": "12345678A",
                "nombre": "Nuevo",
                "apellidos": "Trabajador",
                "horasContrato": 8,
                "codigoTienda": 1
            }
            """;
        // Creamos un nuevo trabajador vacio
        Trabajador trabajadorFalso = new Trabajador();
        // Indicamos a Mokito que cuando busque un trabajador lo encuentre
        Mockito.when(trabajadorMapper.toEntity(any())).thenReturn(trabajadorFalso);
        Mockito.when(trabajadorService.guardarTrabajador(any(), anyInt())).thenReturn(trabajadorFalso);

        // Simulamos POST y esperamos un 201 Created
        mockMvc.perform(post("/api/trabajadores")
                .contentType(MediaType.APPLICATION_JSON)
                .content(jsonBody))
                .andExpect(status().isCreated());
    }

    @Test
    void editarTrabajador_DatosValidos_Devuelve200OK() throws Exception 
    {
    	// Creamos un JSON que simula la petición del cliente
        String jsonBody = """
            {
                "nombre": "Editado",
                "apellidos": "Trabajador",
                "horasContrato": 4,
                "codigoTienda": 1
            }
            """;
        // Creamos un nuevo trabajador vacio
        Trabajador trabajadorFalso = new Trabajador();
        // Indicamos a Mokito que cuando busque un trabajador lo encuentre
        org.mockito.Mockito.when(trabajadorMapper.toEntity(any())).thenReturn(trabajadorFalso);
        org.mockito.Mockito.when(trabajadorService.guardarTrabajador(any(), anyInt())).thenReturn(trabajadorFalso);

        // Simulamos PUT a la URL con el DNI y esperamos 200 OK
        mockMvc.perform(put("/api/trabajadores/12345678A")
                .contentType(MediaType.APPLICATION_JSON)
                .content(jsonBody))
                .andExpect(status().isOk());
    }

    // -- -------------------------- --
    // -- TODO: ELIMINAR TRABAJADOR  --
    // -- -------------------------- --

    @Test
    void eliminarTrabajador_DniValido_Devuelve204NoContent() throws Exception 
    {
        // Simulamos un DELETE y esperamos 204 No Content (el estándar de borrado en REST)
        mockMvc.perform(delete("/api/trabajadores/12345678A")).andExpect(status().isNoContent());
    }
}