package mercadona_prueba.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import mercadona_prueba.model.Tienda;

public interface TiendaRepository extends JpaRepository<Tienda,Integer> 
{
	
}