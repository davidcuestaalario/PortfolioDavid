package mercadona_prueba.service;

import mercadona_prueba.model.Aptitud;
import mercadona_prueba.model.Asignacion;
import mercadona_prueba.model.Seccion;
import mercadona_prueba.model.Tienda;
import mercadona_prueba.model.Trabajador;
import mercadona_prueba.repository.AsignacionRepository;
import mercadona_prueba.repository.SeccionRepository;
import mercadona_prueba.repository.TiendaRepository;
import mercadona_prueba.repository.TrabajadorRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/** 
 * Esta es la capa de negocio para los trabajadores.
 * Contendra toda la logica pesada de los trabajadores
 */
@Service 
public class TrabajadorService 
{
    // -- ----------------- --
    // -- TODO DEPENDENCIAS --
    // -- ----------------- --
    
    // Inyectamos los repositorios para interactuar con la base de datos
    private final TrabajadorRepository trabajadorRepository;
    private final TiendaRepository tiendaRepository;
    private final SeccionRepository seccionRepository;
    private final AsignacionRepository asignacionRepository;

    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
    
    public TrabajadorService
    (
    	TrabajadorRepository trabajadorRepository, 
    	TiendaRepository tiendaRepository,
        SeccionRepository seccionRepository, 
        AsignacionRepository asignacionRepository
    ) 
    {
        this.trabajadorRepository = trabajadorRepository;
        this.tiendaRepository = tiendaRepository;
        this.seccionRepository = seccionRepository;
        this.asignacionRepository = asignacionRepository;
    }

    // -- -------------- --
    // -- TODO BUSQUEDAS --
    // -- -------------- --
    
    /** Devuelve un listado con todos los trabajadores */
    public List<Trabajador> obtenerTodos() { return trabajadorRepository.findAll(); }
    /** Dado un DNI devuelve el trabajador que coincida */
    public Optional<Trabajador> obtenerPorDni(String dni) { return trabajadorRepository.findById(dni); }

    // -- ------------ --
    // -- TODO GUARDAR --
    // -- ------------ --
    
    /** 
     * Dado un trabajador, Actualiza la informacion del trabajador </br>
     * - El trabajador debe existir (pero esto ya se comprueba internamente)
     * @param pTrabajador
     * @return
     */
    public Trabajador guardarTrabajador( Trabajador pTrabajador ){ return guardarTrabajador( pTrabajador ,null ); }

    /**
     * Dado un trabajador y el codigo de la tienda en la que trabaja </br>
     * - Valida que la tienda existe </br>
     * - Valida que se cumple la restriccion de horas del trabajador </br>
     * Si se cumplen todas las validaciones </br> 
     * - Guarda al trabajador en BD </br>
     * Se puede utilizar null en el codigo de la tienda y en este caso se buscara la tienda en el trabajador que ya existia
     * Si no se encuentra el trabajador no funcionara dado que sin el codigo de la tienda solo se opta a actualizar datos del trabajador y no a crear un nuevo trabajador
     * @param trabajador = Trabajador que se pretende guardar
     * @param codigoTienda = Codigo de la tienda en la que trabaja
     * @return El trabajador guardado
     */
    public Trabajador guardarTrabajador( Trabajador pTrabajador , Integer pCodigoTienda ) 
    {
    	// GESTION DE LA TIENDA
    	// Si no nos pasan un codigo de tienda, Solo puede ser porque el trabajador ya existia.
        if( pCodigoTienda == null ) 
        {
            // Comprobamos si el trabajador ya existe en BD para saber si estamos actualizando o guardando uno nuevo
            Optional<Trabajador> trabajadorExistente = trabajadorRepository.findById(pTrabajador.getDni());
            // Si el trabajador existe, Es una actualziacion y deberia tener tienda asignada
            if( trabajadorExistente.isPresent() ) 
            {
            	// Identificamos la tienda del trabajador
            	Tienda tiendaExistente = trabajadorExistente.get().getTienda();
            	// Se la asignamos al nuevo trabajador
            	pTrabajador.setTienda(tiendaExistente);
            }
            // Si el trabajador no existe y no sabemos la tienda, No se puede actualizar
            else{ throw new IllegalArgumentException("El trabajador no existe y no se puede crear uno nuevo sin el codigo de la tienda"); }
        }
        // Si nos pasan un nuevo código de tienda
        else
        {
        	// Buscamos la tienda, Si no existe lanzamos una excepcion
            Tienda nuevaTienda = tiendaRepository.findById(pCodigoTienda).orElseThrow(() -> new RuntimeException("Tienda no encontrada"));
            // Asignamos la tienda al trabajador
            pTrabajador.setTienda(nuevaTienda);
        }
        
        // GESTION DE LAS HORAS DE CONTRATRATO
        // Si se superan las horas maximas (8), Lanzamos una excepcion
        if( pTrabajador.getHorasContrato() > 8 ){ throw new IllegalArgumentException("Las horas de contrato no pueden superar las 8h"); }
        // Calculamos las horas que el trabajador ya tiene asignadas
        int horasYaAsignadas = asignacionRepository.sumHorasAsignadasByTrabajadorDni(pTrabajador.getDni());
        // Si el trabajador ya tiene horas asignadas en secciones, su nuevo contrato no puede ser menor a esas horas
        if( pTrabajador.getHorasContrato() < horasYaAsignadas ) 
        {
            throw new IllegalArgumentException( "No se puede reducir el contrato a " + pTrabajador.getHorasContrato() + " horas porque el trabajador ya tiene " + horasYaAsignadas + " horas asignadas en secciones.");
        }
        
        // Si hemos llegado hasta aqui, Guardamos al Trabajador
        return trabajadorRepository.save(pTrabajador);
    }


    /**
     * Dado un trabajador y una seccion asignamos al trabajador a la seccion con el numero de horas establecido
     * @param dni = Identificador del trabajador
     * @param nombreSeccion = Identificador de la seccion
     * @param horasAsignadas = Numero de horas que se asignan o desasignan a la eccion
     * @return nueva asignacion, asignacion ya existente actualizada o null si se ha borrado
     */
    public Asignacion asignarTrabajadorToSeccion( String pDni , String pNombreSeccion , Integer pHorasAsignadas ) 
    {
    	// Inicializamos una asignacion nula
        Asignacion asignacion = null;
    	// Buscamos al trabajador, Si no la encuentra lanza una excepcion
        Trabajador trabajador = trabajadorRepository.findById(pDni).orElseThrow(() -> new RuntimeException("Trabajador no encontrado"));
        // Buscamos la seccion, Si no la encuentra lanza una excepcion
        Seccion seccion = seccionRepository.findById(pNombreSeccion).orElseThrow(() -> new RuntimeException("Seccion no encontrada"));
        
        // Comprobamos si un trabajador esta cualificado para asignarse a esta seccion
        boolean tieneAlgunaAptitud = isTrabajadorCualificado( seccion , trabajador );
        if( !tieneAlgunaAptitud )
        {
            throw new IllegalArgumentException ("Operación denegada: El trabajador " + trabajador.getNombre() + " no posee ninguna aptitud para trabajar en la sección de " + seccion.getNombre() );
        }
        	
        // Buscamos si ya existe esta asignación específica
        Optional<Asignacion> asignacionExistente = asignacionRepository.findByTrabajadorDniAndSeccionNombre( pDni , pNombreSeccion );
        // Inicialmente asumimos que no hay horas asignadas para esta seccion
        int horasAsignadasEstaSeccion = 0;
        // Identificamos el numero de horas asignadas a esta seccion
        if( asignacionExistente.isPresent() ){ horasAsignadasEstaSeccion = asignacionExistente.get().getHorasAsignadas(); }
        // Calculamos el nuevo numero de horas asignadas a esta seccion
        int NuevasHorasAsignadasEstaSecccion = horasAsignadasEstaSeccion + pHorasAsignadas;
        // Si las nuevas horas asignadas van a ser iguales o menores que cero, borramos la asignacion
        if( NuevasHorasAsignadasEstaSecccion <= 0 ){ asignacionExistente.ifPresent(asignacionRepository::delete); }
        // Si las nuevas horas asignadas quedan en positivo 
        else 
        {
            // Calculamos las horas actualmente asignadas a todas las secciones (Incluida esta)
            int horasTotalesActuales = asignacionRepository.sumHorasAsignadasByTrabajadorDni(pDni);
            // Calculamos el nuevo numero de horas asignadas en todas las secciones (Incluida esta)
            int horasTotalesFuturas = ( horasTotalesActuales - horasAsignadasEstaSeccion ) + NuevasHorasAsignadasEstaSecccion;
            
            // Validar que la nueva asignación no exceda las horas del contrato, Si se superan lanzamos una excepcion
            if( horasTotalesFuturas > trabajador.getHorasContrato()) { throw new IllegalArgumentException("El trabajador no tiene suficientes horas disponibles"); }
            
            // Si hemos llegado hasta aqui y la asignacion ya existia guardamos la asignacion
            if( asignacionExistente.isPresent() ) 
            {
                asignacion = asignacionExistente.get();
                asignacion.setHorasAsignadas(NuevasHorasAsignadasEstaSecccion);
                asignacionRepository.save(asignacion);
            } 
            // Si la asignacion no existia, Creamos una nueva
            else 
            {
            	asignacion = new Asignacion( trabajador , seccion , NuevasHorasAsignadasEstaSecccion );
                asignacionRepository.save(asignacion);
            }
        }
        // Devolvemos la asignacion
        return asignacion;
    }
    
    /**
     * Comprueba si un trabajador esta capacitado para asignarse a una seccion
     * @param pSeccion = Seccion a la que se pretende asignar el trabajador
     * @param pTrabajador = Trabajador que se pretende asignar a la seccion
     * @return True si el trabajador tiene al menos una aptitud de la seccion o false si no tiene ninguna aptitud de la seccion
     */
    private boolean isTrabajadorCualificado( Seccion pSeccion , Trabajador pTrabajador )
    {
        // Inicialmente asumimos que el trabajador no tiene ninguna aptitud de la seccion
        boolean tieneAlgunaAptitud = false;
        // Recorremos las aptitudes que exige la sección
        for( Aptitud aptitudRequerida : pSeccion.getAptitudesRequeridas() ) 
        {
            // Inicialmente asumimos que el trabajador no tiene esta aptitud
            boolean tieneEstaAptitud = false;
            // Recorremos las aptitudes del rabajador
            for( Aptitud aptitudTrabajador : pTrabajador.getAptitudesAdquiridas() ) 
            {
            	// Buscamos si el trabajador tiene esta aptitud en concreto y si la encontramos detenemos la busqueda
            	if( aptitudTrabajador.getNombre().equals( aptitudRequerida.getNombre() ) ){ tieneEstaAptitud = true; break; }
            }
            // Si hemos revisado todo el trabajador y si tenia esta aptitud,adimitimos que el trabajador tiene al menos una aptitud y puede trabajar en esta seccion
            if( tieneEstaAptitud ){ tieneAlgunaAptitud = true; break; }
        }
        // Devolvemos la comprobacion de aptitudes
        return tieneAlgunaAptitud;
    }
    
    // -- ------------- --
    // -- TODO ELIMINAR --
    // -- ------------- --
    
    /**
     * Intenta eliminar un trabajador y todas sus asignaciones si las tubiera </br>
     * Si algo falla a mitad de la operacion la anotacion de Transactional impedira que se borre nada
     * @param dni
     */
    @Transactional
    public void eliminarTrabajador(String dni) 
    {
        // Primero borramos sus relaciones en la tabla intermedia
        asignacionRepository.deleteByTrabajadorDni(dni);
        // Luego ya podemos borrar al trabajador sin que la BD se queje
        trabajadorRepository.deleteById(dni);
    }

}