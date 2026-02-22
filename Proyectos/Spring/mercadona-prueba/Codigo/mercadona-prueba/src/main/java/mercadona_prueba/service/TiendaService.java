package mercadona_prueba.service;

import mercadona_prueba.dto.AptitudDTO;
import mercadona_prueba.dto.AptitudesForSeccion;
import mercadona_prueba.dto.AptitudesForTienda;
import mercadona_prueba.model.Aptitud;
import mercadona_prueba.model.Seccion;
import mercadona_prueba.model.Tienda;
import mercadona_prueba.repository.SeccionRepository;
import mercadona_prueba.repository.TiendaRepository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class TiendaService 
{
    // -- ----------------- --
    // -- TODO DEPENDENCIAS --
    // -- ----------------- --
    
    private final TiendaRepository tiendaRepository;
    private final SeccionRepository seccionRepository;

    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
    
    public TiendaService
    (
    	TiendaRepository tiendaRepository, 
    	SeccionRepository seccionRepository) 
    {
        this.tiendaRepository = tiendaRepository;
        this.seccionRepository = seccionRepository;
    }

    // -- -------------- --
    // -- TODO BUSQUEDAS --
    // -- -------------- --
    
    // -- ------------ --
    // -- TODO GUARDAR --
    // -- ------------ --
    
    // -- ------------- --
    // -- TODO ELIMINAR --
    // -- ------------- --
    
    // -- ---------- --
    // -- TODO OTROS --
    // -- ---------- --
    
    /**
     * Genera los reportes de detalles de aptitudes necesarias para una tienda rellenando desde base de datos esta estrcutura:
	 * AptitudesForTienda
	   ^ codigo de la tienda
	   ^ nombre de la tienda
	   ^ Listado de aptitudes por seccion
	     - nombre_seccion
	     - listado de aptitudes necesarias
	       > nombre de la aptitud
     * @param codigoTienda codigo de la tienda de la que generamos el informe
     * @return Reporte de de detalles de aptitudes necesarias para la tienda indicada o RuntimeException si no existia el codigo de la tienda
     */
    public AptitudesForTienda obtenerDetalleTienda(Integer codigoTienda) 
    {
        // Buscamos la tienda y si no existe mandamos una excepcion
        Tienda tienda = tiendaRepository.findById(codigoTienda).orElseThrow(() -> new RuntimeException("Tienda no encontrada"));
        // Recuperamos un listado con todas las secciones
        List<Seccion> todasLasSecciones = seccionRepository.findAll();
        // Creamos una nueva lista vacia para las aptitudes de la tienda
        List<AptitudesForSeccion> listaSeccionesTienda = new ArrayList<>();
        // Para cada seccion
        for( Seccion iSeccion : todasLasSecciones ) 
        {
        	 // Creamos una nueva lista vacia para las aptitudes de la seccion
            List<AptitudDTO> listaAptitudesSeccion = new ArrayList<>();
            // Para cada aptitud requerida para en la seccion
            for( Aptitud aptitud : iSeccion.getAptitudesRequeridas()) 
            {
            	// Anadimos la aptitud a la lista de aptitudes para la seccion
            	listaAptitudesSeccion.add(new AptitudDTO(aptitud.getNombre()));
            }
            // Anadimos la lista de las aptitudes de la seccion a las aptitudes de la tienda
            listaSeccionesTienda.add( new AptitudesForSeccion( iSeccion.getNombre(), listaAptitudesSeccion) );
        }
        // Devolvemos el DTO de las aptitudes de la tienda
        return new AptitudesForTienda( tienda.getCodigo() , tienda.getNombre() , listaSeccionesTienda );
    }
}