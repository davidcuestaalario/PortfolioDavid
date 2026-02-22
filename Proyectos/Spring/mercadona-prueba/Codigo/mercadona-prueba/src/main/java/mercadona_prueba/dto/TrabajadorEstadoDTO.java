package mercadona_prueba.dto;

/** 
 * Informe de estado de un trabajador 
 * Contiene el nombre completo del trabajador y las horas que realiza
 */
public record TrabajadorEstadoDTO
(
    String nombreCompleto, 
    Integer horas
) {}