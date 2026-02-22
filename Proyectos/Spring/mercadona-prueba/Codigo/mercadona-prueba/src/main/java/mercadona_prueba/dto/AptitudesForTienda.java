package mercadona_prueba.dto;
import java.util.List;

public record AptitudesForTienda
(
    Integer codigo,
    String nombre,
    List<AptitudesForSeccion> secciones
) {}