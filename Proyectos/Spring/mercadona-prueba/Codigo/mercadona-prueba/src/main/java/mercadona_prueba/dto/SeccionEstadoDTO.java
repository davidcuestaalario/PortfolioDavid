package mercadona_prueba.dto;
import java.util.List;

/** 
 * Un informe con el estado de una seccion
 * Contiene el nombre de la seccion y un listado de los estados de cada uno de los trabajadores de la seccion
 */
public record SeccionEstadoDTO
(
    String nombreSeccion,
    List<TrabajadorEstadoDTO> trabajadores
) {}