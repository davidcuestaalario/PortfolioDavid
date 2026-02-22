package mercadona_prueba.mapper;

import mercadona_prueba.dto.TrabajadorRequestDTO;
import mercadona_prueba.dto.TrabajadorResponseDTO;
import mercadona_prueba.model.Trabajador;
import org.springframework.stereotype.Component;

@Component
public class TrabajadorMapper 
{
    // -- ------------ --
    // -- TODO ENTIDAD --
    // -- ------------ --
    
    /** Convierte lo que entra por Postman a nuestra Entidad */
    public Trabajador toEntity(TrabajadorRequestDTO dto) 
    {
        Trabajador trabajador = new Trabajador();
        trabajador.setDni(dto.dni());
        trabajador.setNombre(dto.nombre());
        trabajador.setApellidos(dto.apellidos());
        trabajador.setHorasContrato(dto.horasContrato());
        return trabajador;
    }
    
    // -- -------- --
    // -- TODO DTO --
    // -- -------- --

    /** Convierte nuestra Entidad a la respuesta limpia para el usuario */
    public TrabajadorResponseDTO toResponseDTO(Trabajador entity) 
    {
        String nombreTienda = ( entity.getTienda() != null ) ? entity.getTienda().getNombre() : "Sin Tienda";
        return new TrabajadorResponseDTO
        (
            entity.getDni(),
            entity.getNombre(),
            entity.getApellidos(),
            entity.getHorasContrato(),
            nombreTienda
        );
    }
}