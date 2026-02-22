package mercadona_prueba.dto;
import java.util.List;

/** 
 * Reporte de faltas de una tienda
 * Contiene el nombre de la tienda y un listado con las faltas de cada seccion de la tienda
 */
public record ReporteFaltasDTO
(
    String nombreTienda,
    List<SeccionFaltaDTO> seccionesConFaltas
) {}