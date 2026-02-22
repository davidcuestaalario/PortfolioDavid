package mercadona_prueba.service;

import mercadona_prueba.dto.*;
import mercadona_prueba.model.Asignacion;
import mercadona_prueba.model.Seccion;
import mercadona_prueba.model.Tienda;
import mercadona_prueba.repository.AsignacionRepository;
import mercadona_prueba.repository.SeccionRepository;
import mercadona_prueba.repository.TiendaRepository;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

// NOTA:
// Esta clase realizara los cálculos de los reportes con un coste prácticamente lineal
// Como en el ejemplo las secciones son constantes (No se prevé que pasen a existir más)
// Podemos decir que el coste será lineal con las asignaciones O(Asignaciones) 
// No obstante el coste real es O(Asignaciones*Secciones) 
// Esto implica que si el número de secciones pudiera crecer, estos métodos para calcular los reportes serian demasiado costosos 
// La forma de proceder en este caso sería utilizar un HasMap que garantice que solo se recorra cada asignación una vez

/**
 * Esta clase se encarga de recabar los datos de los informes de estado y los informes de falta de horas para una tienda. 
 */
@Service
public class ReporteService 
{
    // -- ----------------- --
    // -- TODO DEPENDENCIAS --
    // -- ----------------- --
    
    private final TiendaRepository tiendaRepository;
    private final SeccionRepository seccionRepository;
    private final AsignacionRepository asignacionRepository;

    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
    
    public ReporteService
    (
    	TiendaRepository tiendaRepository, 
    	SeccionRepository seccionRepository, 
    	AsignacionRepository asignacionRepository
    ) 
    {
        this.tiendaRepository = tiendaRepository;
        this.seccionRepository = seccionRepository;
        this.asignacionRepository = asignacionRepository;
    }

    // -- ----------------------------- --
    // -- TODO REPORTE DE ESTADO        --
    // -- ----------------------------- --
    
    /**
     * Genera los reportes de estados rellenando desde base de datos esta estrcutura:
     * ReporteEstadoDTO
		^ nombre_tienda
		^ Listado de Estados Seccion (SeccionEstadoDTO)
		  - nombre_seccion
		  - listado de estados de trabajadores (TrabajadorEstadoDTO)
		    > nombre_trabajador
			> horas del trabajador en la seccion
     * @param codigoTienda codigo de la tienda de la que generamos el informe
     * @return Reporte de estado para la tienda indicada o RuntimeException si no existia el codigo de la tienda
     */
    public ReporteEstadoDTO generarReporteEstado( Integer codigoTienda ) 
    {
    	// Buscamos la tienda, Si no existe lanzamos una excepcion
        Tienda tienda = tiendaRepository.findById(codigoTienda).orElseThrow(() -> new RuntimeException("Tienda no encontrada"));
        // Buscamos todas las secciones contempladas en la BD
        List<Seccion> todasLasSecciones = seccionRepository.findAll();
        // Buscamos todas las asignaciones de todos los trabajadores para la tienda selecionada
        List<Asignacion> asignacionesTienda = asignacionRepository.findByTrabajadorTiendaCodigo(codigoTienda);

        // Construimos el estado de las secciones para la tienda indicada
        List<SeccionEstadoDTO> seccionesDTO = construirEstadoSecciones(todasLasSecciones, asignacionesTienda);
        // Contruimos el reposte de estado para la tienda indicada
        return new ReporteEstadoDTO( tienda.getNombre() , seccionesDTO );
    }

    private List<SeccionEstadoDTO> construirEstadoSecciones( List<Seccion> pListadoSecciones , List<Asignacion> pListadoAsignacionesTienda ) 
    {
    	// Inicializamos un listado vacio de estados de secciones
        List<SeccionEstadoDTO> listaEstadosSecciones = new ArrayList<>();
        // Para cada seccion
        for( Seccion iSeccion : pListadoSecciones) 
        {
        	// Construimos el listado de estados de trabajadores
            List<TrabajadorEstadoDTO> trabajadores = obtenerTrabajadoresParaSeccion( iSeccion.getNombre(),  pListadoAsignacionesTienda );
            // Anadimos el listado de estados de trabajadores al listado de estados para la seccion actual
            listaEstadosSecciones.add(new SeccionEstadoDTO( iSeccion.getNombre(), trabajadores));
        }
        // Devolvemos el listado de Estados de secciones
        return listaEstadosSecciones;
    }

    private List<TrabajadorEstadoDTO> obtenerTrabajadoresParaSeccion( String pNombreSeccion , List<Asignacion> pListaAsignacionesTienda ) 
    {
    	// Inicializamos un listado de Estados de trabajadores vacia
        List<TrabajadorEstadoDTO> listaEstadosTrabajadores = new ArrayList<>();
        // Para cada asignacion a la tienda
        for( Asignacion iAsignacion : pListaAsignacionesTienda ) 
        {
        	// Si la tienda pertenece a la seccion que estamos analizando
            if( iAsignacion.getSeccion().getNombre().equals( pNombreSeccion )) 
            {
            	// obtenemos el nombre completo del trabajador
                String nombreCompleto = iAsignacion.getTrabajador().getNombre() + " " + iAsignacion.getTrabajador().getApellidos();
                // Contruimos el estado del trabajador de la asignacion actual
                listaEstadosTrabajadores.add(new TrabajadorEstadoDTO(nombreCompleto, iAsignacion.getHorasAsignadas()));
            }
        }
        // Devolvemos el listado de Estados de trabajadores 
        return listaEstadosTrabajadores;
    }

    // -- ----------------------------- --
    // -- TODO REPORTE DE FALTAS        --
    // -- ----------------------------- --
    
    /**
     * Genera los reportes de faltas rellenando desde base de datos esta estrcutura:
     * ReporteFaltasDTO
	   ^ nombre_tienda
	   ^ Listado de Faltas de Seccion
		  - nombre_seccion
		  - horas que faltan en la seccion
     * @param codigoTienda codigo de la tienda de la que generamos el informe
     * @param isJPQL indica si la operacion se ejecuta con JPQL (true) o con memoria en java (false)
     * @return Reporte de faltas para la tienda indicada o RuntimeException si no existia el codigo de la tienda
     */
    public ReporteFaltasDTO generarReporteFaltas( Integer codigoTienda , boolean isJPQL ) 
    {
    	ReporteFaltasDTO reporte = null;
    	if( isJPQL ){ reporte = generarReporteFaltas_JPQL(codigoTienda); }
    	else{ reporte = generarReporteFaltas_MemoriaJava( codigoTienda ); }
    	return reporte;
    }
    
    /**
     * Genera los reportes de faltas rellenando desde base de datos esta estrcutura:
     * ReporteFaltasDTO
	   ^ nombre_tienda
	   ^ Listado de Faltas de Seccion
		  - nombre_seccion
		  - horas que faltan en la seccion
     * @param codigoTienda codigo de la tienda de la que generamos el informe
     * @return Reporte de faltas para la tienda indicada o RuntimeException si no existia el codigo de la tienda
     */
    private ReporteFaltasDTO generarReporteFaltas_JPQL( Integer codigoTienda ) 
    {
    	// Buscamos la tienda, Si no existe lanzamos una excepcion
        Tienda tienda = tiendaRepository.findById(codigoTienda).orElseThrow(() -> new RuntimeException("Tienda no encontrada"));
        // Ejecutamos la consulta JPQL de alto rendimiento
        List<Object[]> resultadosBD = seccionRepository.findFaltasByTienda(codigoTienda);
        // Convertimos el resultado crudo de la BD a nuestros DTOs limpios
        List<SeccionFaltaDTO> seccionesConFaltas = new ArrayList<>();
        for (Object[] fila : resultadosBD) 
        {
        	// Extraemos el nombre de la seccion
            String nombreSeccion = (String) fila[0];
            // Extraemos el calculo de las horas faltantes. La base de datos devuelve cálculos matemáticos como 'Long', lo pasamos a Integer
            Integer horasFaltantes = ( (Number) fila[1]).intValue(); 
            // Anadimos la seccion al reporte de faltas de la tienda
            seccionesConFaltas.add( new SeccionFaltaDTO( nombreSeccion , horasFaltantes ) );
        }
        // Generamos el reporte de faltas de la tienda
        return new ReporteFaltasDTO(tienda.getNombre(), seccionesConFaltas);
    }
    
    /**
     * Genera los reportes de faltas rellenando desde base de datos esta estrcutura:
     * ReporteFaltasDTO
	   ^ nombre_tienda
	   ^ Listado de Faltas de Seccion
		  - nombre_seccion
		  - horas que faltan en la seccion
     * @param codigoTienda codigo de la tienda de la que generamos el informe
     * @return Reporte de faltas para la tienda indicada o RuntimeException si no existia el codigo de la tienda
     */
    private ReporteFaltasDTO generarReporteFaltas_MemoriaJava( Integer codigoTienda ) 
    {
    	// Buscamos la tienda, Si no existe lanzamos una excepcion
        Tienda tienda = tiendaRepository.findById(codigoTienda).orElseThrow(() -> new RuntimeException("Tienda no encontrada"));
        // Buscamos todas las secciones contempladas en la BD
        List<Seccion> todasLasSecciones = seccionRepository.findAll();
        // Buscamos todas las asignaciones de todos los trabajadores para la tienda selecionada
        List<Asignacion> asignacionesTienda = asignacionRepository.findByTrabajadorTiendaCodigo(codigoTienda);

        // Construimos el estado de las faltas para la tienda indicada
        List<SeccionFaltaDTO> seccionesConFaltas = calcularFaltasSecciones( todasLasSecciones , asignacionesTienda );
        // Contruimos el reposte de faltas para la tienda indicada
        return new ReporteFaltasDTO(tienda.getNombre(), seccionesConFaltas);
    }

    private List<SeccionFaltaDTO> calcularFaltasSecciones( List<Seccion> pListadoSecciones, List<Asignacion> pListadoAsignacionesTienda ) 
    {
    	// Inicializamos un listado de Faltas de secciones vacia
        List<SeccionFaltaDTO> listaFaltas = new ArrayList<>();
        // Para cada seccion 
        for (Seccion seccion : pListadoSecciones )
        {
        	/// Calculamos las horas que estan cubiertas
            int horasCubiertas = sumarHorasSeccion( seccion.getNombre() , pListadoAsignacionesTienda );
            // Calculamos las horas que faltan por cubrir
            int horasFaltantes = seccion.getHorasNecesarias() - horasCubiertas;

            // Solo añadimos la sección si realmente le faltan horas
            if( horasFaltantes > 0 ){ listaFaltas.add(new SeccionFaltaDTO(seccion.getNombre(), horasFaltantes)); }
        }
        // Devolvemos el listado de faltas de la seccion
        return listaFaltas;
    }

    private int sumarHorasSeccion( String nombreSeccion , List<Asignacion> pListadoAsignacionesTienda ) 
    {
    	// Empezamos el conteo en cero
        int totalHoras = 0;
        // Para cada asignacion a la tienda
        for( Asignacion asignacion : pListadoAsignacionesTienda ) 
        {
        	// Si el nomrbe de la seccion coincide con la seccion que estamos analizando
            if (asignacion.getSeccion().getNombre().equals(nombreSeccion)) 
            {
            	// Sumamos las horas de la asignacion
                totalHoras += asignacion.getHorasAsignadas();
            }
        }
        // Devolvemos el conteo de horas
        return totalHoras;
    }
}