package mercadona_prueba.dto;
import java.util.List;

/** 
 * Un informe con el estado de una tienda
 * Contiene el nombre de la tienda y un listado de los estados de cada seccion de la tienda
 */
public record ReporteEstadoDTO
(
    String nombreTienda,
    List<SeccionEstadoDTO> secciones
) {}