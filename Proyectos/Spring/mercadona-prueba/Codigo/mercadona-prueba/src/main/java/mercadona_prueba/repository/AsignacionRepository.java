package mercadona_prueba.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import mercadona_prueba.model.Asignacion;

public interface AsignacionRepository extends JpaRepository<Asignacion,Long> 
{
    // -- -------------- --
    // -- TODO BUSQUEDAS --
    // -- -------------- --
    
	/** Busca si ya existe una asignación para ese DNI y esa Sección */
    Optional<Asignacion> findByTrabajadorDniAndSeccionNombre( String dni , String nombreSeccion );
    
    /** Recupera todas las asignaciones de todos los trabajadores de una tienda específica */
    List<Asignacion> findByTrabajadorTiendaCodigo( Integer codigoTienda );
    
    // -- ------------ --
    // -- TODO CONTEOS --
    // -- ------------ --
    
    /** Suma las horas de todas las asignaciones de un trabajador directamente en la BD */
    @Query("SELECT COALESCE(SUM(a.horasAsignadas), 0) FROM Asignacion a WHERE a.trabajador.dni = :dni")
    Integer sumHorasAsignadasByTrabajadorDni( @Param("dni") String dni );
    
    // -- ----------- --
    // -- TODO DELETE --
    // -- ----------- --
    
    /** Borra todas las asignaciones de un trabajador */
    void deleteByTrabajadorDni(String dni);
}