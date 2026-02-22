package mercadona_prueba.repository;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;

import mercadona_prueba.model.Asignacion;
import mercadona_prueba.model.Seccion;
import mercadona_prueba.model.Tienda;
import mercadona_prueba.model.Trabajador;

@DataJpaTest // Levanta una BD H2 en memoria solo para estos tests
public class SeccionRepositoryTest 
{
    // -- ----------------- --
    // -- TODO DEPENDENCIAS --
    // -- ----------------- --
    
    @Autowired private SeccionRepository seccionRepository;
    @Autowired private TiendaRepository tiendaRepository;
    @Autowired private TrabajadorRepository trabajadorRepository;
    @Autowired private AsignacionRepository asignacionRepository;

    // -- ---------------------- --
    // -- TODO CALCULO DE FALTAS --
    // -- ---------------------- --
    
    @Test
    void findFaltasByTienda_CalculaCorrectamenteLaRestaEnBD() 
    {
        // Preparamos datos reales en la BD de prueba
        Tienda tienda = new Tienda();
        tienda.setCodigo(99);
        tienda.setNombre("Tienda Test BD");
        tiendaRepository.save(tienda);

        // Creamos una sección que necesita 16 horas
        Seccion seccion = new Seccion();
        seccion.setNombre("CajasTest");
        seccion.setHorasNecesarias(16);
        seccionRepository.save(seccion);

        // Creamos un trabajador de esa tienda con 8 horas de contrato
        Trabajador trabajador = new Trabajador("99999999X", "TestBD", "ApeBD", 8, tienda);
        trabajadorRepository.save(trabajador);

        // Le asignamos 5 horas a la sección (Deberían faltar 16 - 5 = 11 horas)
        Asignacion asignacion = new Asignacion(trabajador, seccion, 5);
        asignacionRepository.save(asignacion);

        // Ejecutamos nuestra Query JPQL
        List<Object[]> resultados = seccionRepository.findFaltasByTienda(99);

        // Verificamos el resultado devuelto por la BD
        assertFalse(resultados.isEmpty(), "La base de datos debería devolver un resultado");
        // Buscamos la fila correspondiente a "CajasTest" 
        Object[] filaCajas = null;
        for (Object[] fila : resultados) 
        {
        	// Si lo encontramos, paramos de buscar
            if( fila[0].equals("CajasTest")) { filaCajas = fila; break; }
        }
        // Verificamos que el nombre es "CajasTest" 
        assertEquals("CajasTest", filaCajas[0]);
        // Verificamos que las horas faltantes son 11
        assertEquals(11, ((Number) filaCajas[1]).intValue(), "La BD no ha calculado bien 16 - 5 = 11");
    }
}