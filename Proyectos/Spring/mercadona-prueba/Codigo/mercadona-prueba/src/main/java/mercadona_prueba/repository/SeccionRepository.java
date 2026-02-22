package mercadona_prueba.repository;

import mercadona_prueba.model.Seccion;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface SeccionRepository extends JpaRepository<Seccion, String> 
{
	
	/**
	 * Agrupa todas las secciones, 
	 * suma las horas de los trabajadores para una tienda en concreto, 
	 * Calcula las horas faltantes para la secion,
	 * Devuelve solo las secciones a las que les falten horas
	 * @param codigoTienda
	 * @return Listado con dos datos, el nombre de la seccion y el calculo de horas restantes de la seccion. </br>
	 * - Se excluyen del listado las secciones que den menos de cero horas
	 */
    @Query("SELECT seccion.nombre , ( seccion.horasNecesarias - COALESCE( " + 
	       "SUM( CASE WHEN tienda.tienda.codigo = :codigoTienda THEN asignacion.horasAsignadas ELSE 0 END) , 0) ) " + 
    	   "FROM Seccion seccion " +
           "LEFT JOIN Asignacion asignacion ON asignacion.seccion = seccion " +
           "LEFT JOIN asignacion.trabajador tienda " +
           "GROUP BY seccion.nombre , seccion.horasNecesarias " +
           "HAVING seccion.horasNecesarias > COALESCE(SUM(CASE WHEN tienda.tienda.codigo = :codigoTienda THEN asignacion.horasAsignadas ELSE 0 END), 0)")
    List<Object[]> findFaltasByTienda(@Param("codigoTienda") Integer codigoTienda);
    
}