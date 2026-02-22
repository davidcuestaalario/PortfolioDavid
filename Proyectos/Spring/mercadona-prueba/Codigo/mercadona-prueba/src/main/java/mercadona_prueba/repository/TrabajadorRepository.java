package mercadona_prueba.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import mercadona_prueba.model.Trabajador;

public interface TrabajadorRepository extends JpaRepository<Trabajador,String> 
{
	
}
