package mercadona_prueba.dto;

/** 
 * Informe con las horas faltantes de una Seccion
 * Contiene el nombre de la seccion y el numero de horas que le faltan a la seccion
 */
public record SeccionFaltaDTO
(
    String nombreSeccion,
    Integer horasFaltantes
) {}