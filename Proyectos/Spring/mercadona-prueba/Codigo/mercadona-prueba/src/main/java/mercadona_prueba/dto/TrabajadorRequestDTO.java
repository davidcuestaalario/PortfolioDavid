package mercadona_prueba.dto;

public record TrabajadorRequestDTO
(
    String dni,
    String nombre,
    String apellidos,
    Integer horasContrato,
    Integer codigoTienda
) {}