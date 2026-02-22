package mercadona_prueba.controller;

import mercadona_prueba.dto.AsignacionRequestDTO;
import mercadona_prueba.dto.TrabajadorRequestDTO;
import mercadona_prueba.dto.TrabajadorResponseDTO;
import mercadona_prueba.mapper.TrabajadorMapper;
import mercadona_prueba.model.Trabajador;
import mercadona_prueba.service.TrabajadorService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

// Esta clase responderá peticiones web (REST)
// La ruta base para todo este controlador es /api/trabajadores

@RestController 
@RequestMapping("/api/trabajadores") 
public class TrabajadorController 
{
    // -- ----------------- --
    // -- TODO DEPENDENCIAS --
    // -- ----------------- --
    
    private final TrabajadorService trabajadorService;
    private final TrabajadorMapper trabajadorMapper;
    
    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
    
    public TrabajadorController(TrabajadorService trabajadorService, TrabajadorMapper trabajadorMapper) 
    {
        this.trabajadorService = trabajadorService;
        this.trabajadorMapper = trabajadorMapper;
    }

    // -- -------------- --
    // -- TODO CONSULTAS --
    // -- -------------- --

    @GetMapping
    public ResponseEntity<List<TrabajadorResponseDTO>> obtenerTodos() 
    {
        List<TrabajadorResponseDTO> respuesta = trabajadorService.obtenerTodos()
                .stream()
                .map(trabajadorMapper::toResponseDTO)
                .collect(Collectors.toList());
        return ResponseEntity.ok(respuesta);
    }

    // -- ------------- --
    // -- TODO CREACIÓN --
    // -- ------------- --

    @PostMapping
    public ResponseEntity<TrabajadorResponseDTO> crearTrabajador(@RequestBody TrabajadorRequestDTO dto) 
    {
        Trabajador trabajador = trabajadorMapper.toEntity(dto);
        Trabajador trabajadorGuardado = trabajadorService.guardarTrabajador(trabajador, dto.codigoTienda());
        return ResponseEntity.status(HttpStatus.CREATED).body(trabajadorMapper.toResponseDTO(trabajadorGuardado));
    }

    // -- ------------ --
    // -- TODO EDICIÓN --
    // -- ------------ --

    @PutMapping("/{dni}")
    public ResponseEntity<TrabajadorResponseDTO> editarTrabajador(@PathVariable String dni, @RequestBody TrabajadorRequestDTO dto) 
    {
        Trabajador trabajador = trabajadorMapper.toEntity(dto);
        // Aseguramos que el DNI de la URL manda sobre el del cuerpo
        trabajador.setDni(dni); 
        Trabajador trabajadorActualizado = trabajadorService.guardarTrabajador(trabajador, dto.codigoTienda());
        return ResponseEntity.ok(trabajadorMapper.toResponseDTO(trabajadorActualizado));
    }

    // -- ------------ --
    // -- TODO BORRADO --
    // -- ------------ --

    @DeleteMapping("/{dni}")
    public ResponseEntity<Void> eliminarTrabajador(@PathVariable String dni) 
    {
        trabajadorService.eliminarTrabajador(dni);
        return ResponseEntity.noContent().build();
    }

    // -- -------------- --
    // -- TODO ASIGNAR   --
    // -- -------------- --

    @PostMapping("/{dni}/asignaciones")
    public ResponseEntity<String> asignarSeccion(@PathVariable String dni, @RequestBody AsignacionRequestDTO dto) 
    {
        trabajadorService.asignarTrabajadorToSeccion(dni, dto.nombreSeccion(), dto.horas());
        return ResponseEntity.ok("Operación de asignación procesada correctamente para el trabajador " + dni);
    }
}