package mercadona_prueba.dto;

public record TrabajadorResponseDTO
(
    String dni,
    String nombre,
    String apellidos,
    Integer horasContrato,
    String nombreTienda
) {}