package mercadona_prueba.dto;
import java.util.List;

public record AptitudesForSeccion
(
    String nombreSeccion,
    List<AptitudDTO> aptitudesNecesarias
) {}