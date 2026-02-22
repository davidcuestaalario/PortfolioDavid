package mercadona_prueba.service;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import mercadona_prueba.model.Aptitud;
import mercadona_prueba.model.Asignacion;
import mercadona_prueba.model.Seccion;
import mercadona_prueba.model.Tienda;
import mercadona_prueba.model.Trabajador;
import mercadona_prueba.repository.AsignacionRepository;
import mercadona_prueba.repository.SeccionRepository;
import mercadona_prueba.repository.TiendaRepository;
import mercadona_prueba.repository.TrabajadorRepository;

@ExtendWith(MockitoExtension.class)
public class TrabajadorServiceTest 
{
    // -- --------- --
    // -- TODO MOKS --
    // -- --------- --
    
    // No queremos tocar la base de datos real en los tests unitarios.
    // Mockito creará repositorios "falsos" que devolverán lo que nosotros le digamos.
    @Mock private TrabajadorRepository trabajadorRepository;
    @Mock private TiendaRepository tiendaRepository;
    @Mock private SeccionRepository seccionRepository;
    @Mock private AsignacionRepository asignacionRepository;

    // -- ----------------- --
    // -- TODO DEPENDENCIAS --
    // -- ----------------- --
    
    // Mockito inyectará los repositorios falsos dentro de este servicio real
    @InjectMocks private TrabajadorService trabajadorService;

    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    
    // Variables de apoyo para no repetir código
    private Trabajador trabajadorBase;
    private Tienda tiendaBase;

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
    
    // Esto se ejecuta antes de cada test para tener datos frescos
    @BeforeEach
    void setUp() 
    {
        tiendaBase = new Tienda();
        tiendaBase.setCodigo(1);
        tiendaBase.setNombre("Mercadona Test");
        trabajadorBase = new Trabajador("11111111A", "TestNombre", "TestApellido", 8, tiendaBase);
    }

    // -- ----------------------- --
    // -- TODO GUARDAR TRABAJADOR --
    // -- ----------------------- --
    
    @Test
    void guardarTrabajador_TodoCorrecto_GuardaYDevuelveTrabajador() 
    {
    	// Indicamos al Repository de Mokito que cuando valla a buscar una tienda, nos devuelva una tienda valida
        when(tiendaRepository.findById(1)).thenReturn(Optional.of(tiendaBase));
        // Indicamos al Repository de Mokito que cuando valla calculas las horas trabajadas de un trabajador, nos diga que son cero
        when(asignacionRepository.sumHorasAsignadasByTrabajadorDni("11111111A")).thenReturn(0);
        // Indicamos al Repository de Mokito que cuando valla guardar los datos de un trabajador, nos devuelva al trabajador guardado
        when(trabajadorRepository.save(any(Trabajador.class))).thenReturn(trabajadorBase);

        // Ejecutamos la funcion de guardar al trabajador
        Trabajador resultado = trabajadorService.guardarTrabajador(trabajadorBase, 1);

        // Verificamos que el trabajador obtenido no es nulo
        assertNotNull(resultado);
        // Verificamos que el trabjador obtenido es el que habiamos guardado
        assertEquals("11111111A", resultado.getDni());
        // Verificamos que se llamó al repositorio para guardar exactamente 1 vez
        verify(trabajadorRepository, times(1)).save(trabajadorBase);
    }
    
    @Test
    void guardarTrabajador_SinCodigoTiendaPeroExisteEnBD_MantieneTiendaYGuarda() 
    {
    	// Indicamos al Repository de Mokito que cuando valla a buscar un trabajador, lo encuentre
        when(trabajadorRepository.findById("11111111A")).thenReturn(Optional.of(trabajadorBase));
        // Indicamos al Repository de Mokito que cuando valla calculas las horas trabajadas de un trabajador, nos diga que son cero
        when(asignacionRepository.sumHorasAsignadasByTrabajadorDni("11111111A")).thenReturn(0);
        // Indicamos al Repository de Mokito que cuando valla guardar los datos de un trabajador, nos devuelva al trabajador guardado
        when(trabajadorRepository.save(any(Trabajador.class))).thenReturn(trabajadorBase);

        // Ejecutamos la funcion de guardar al trabajador
        Trabajador resultado = trabajadorService.guardarTrabajador(trabajadorBase, null);

        // Verificamos que el trabajador obtenido no es nulo
        assertNotNull(resultado);
        // Verificamos que la tienda del trabajador era la tienda asignada
        assertEquals(tiendaBase, resultado.getTienda());
        // Verificamos que se llamó al repositorio para guardar exactamente 1 vez
        verify(trabajadorRepository, times(1)).save(trabajadorBase);
    }

    @Test
    void guardarTrabajador_ReduceContratoPorDebajoDeAsignado_LanzaExcepcion() 
    {
        // Creamos un trabajador con un contrado de 4 horas (Intentamos reducirlo a 4h) 
        trabajadorBase.setHorasContrato(4); 
        // Indicamos al Repository de Mokito que cuando valla a buscar una tienda, la encuentre
        when(tiendaRepository.findById(1)).thenReturn(Optional.of(tiendaBase));
        // Indicamos al Repository de Mokito que el trabajador tiene 6 horas ya asignadas en secciones
        when(asignacionRepository.sumHorasAsignadasByTrabajadorDni("11111111A")).thenReturn(6);

        // Ejecutamos la funcion de guardar trabajador y obtenemos la excepcion programada 
        IllegalArgumentException excepcion = assertThrows(IllegalArgumentException.class, () ->
        {
        	// Falla porque no puedes tener 4h de contrato si ya trabajas 6h
            trabajadorService.guardarTrabajador(trabajadorBase, 1);
        });
        // Validamos que el mensaje es exactamente programado
        assertTrue(excepcion.getMessage().contains("No se puede reducir el contrato a 4 horas porque el trabajador ya tiene 6 horas asignadas"));
        // Verificamos que nunca se llegó a llamar al método save de la base de datos
        verify(trabajadorRepository, never()).save(any(Trabajador.class));
    }
    
    @Test
    void guardarTrabajador_HorasContratoSuperanElMaximo_LanzaExcepcion() 
    {
        // Dado un trabajador con 10 horas de contrato
        trabajadorBase.setHorasContrato(10);
        // Indicamos al Repository de Mokito que la tienda 1 existe
        when(tiendaRepository.findById(1)).thenReturn(Optional.of(tiendaBase));
        // Ejecutamos la funcion de guardar trabajador y obtenemos la excepcion programada
        IllegalArgumentException excepcion = assertThrows( IllegalArgumentException.class , () -> 
        {
            trabajadorService.guardarTrabajador(trabajadorBase, 1);
        });
        // Validamos que el mensaje es exactamente programado
        assertEquals("Las horas de contrato no pueden superar las 8h", excepcion.getMessage());
        // Verificamos que nunca se llegó a llamar al método save de la base de datos
        verify(trabajadorRepository, never()).save(any(Trabajador.class));
    }

    @Test
    void guardarTrabajador_SinCodigoTiendaYNoExisteEnBD_LanzaExcepcion() 
    {
        // Indicamos al Repository de Mokito que cuando valla a buscar un trabajador, no lo encuentre
        when(trabajadorRepository.findById("11111111A")).thenReturn(Optional.empty());
        // Ejecutamos la funcion de guardar trabajador y obtenemos la excepcion programada
        IllegalArgumentException excepcion = assertThrows( IllegalArgumentException.class , () -> 
        {
            trabajadorService.guardarTrabajador(trabajadorBase, null);
        });
        // Validamos que el mensaje es exactamente programado
        assertEquals("El trabajador no existe y no se puede crear uno nuevo sin el codigo de la tienda", excepcion.getMessage());
        // Verificamos que nunca se llegó a llamar al método save de la base de datos
        verify(trabajadorRepository, never()).save(any(Trabajador.class));
    }

    // -- -------------------- --
    // -- TODO ASIGNAR SECCION --
    // -- -------------------- --

    @Test
    void asignarTrabajador_AsignacionNueva_GuardaCorrectamente() 
    {
        // Configuramos una nueva seccion que si exista
        Seccion seccion = new Seccion();
        seccion.setNombre("Horno");
        // Configuramos las aptitudes requeridas para esta seccion
        Aptitud aptitudRequerida = new Aptitud("Hornear Pan");
        seccion.setAptitudesRequeridas(List.of(aptitudRequerida));
        // Configuramos un trabajador que tiene la aptitud requerida
        trabajadorBase.setAptitudesAdquiridas(List.of(aptitudRequerida));

        // Indicamos al Repository de Mokito que encuentre al trabajador
        when(trabajadorRepository.findById("11111111A")).thenReturn(Optional.of(trabajadorBase));
        // Indicamos al Repository de Mokito que encuentre la seccion
        when(seccionRepository.findById("Horno")).thenReturn(Optional.of(seccion));
        // Indicamos al Repository de Mokito que no existía asignación previa a esta seccion
        when(asignacionRepository.findByTrabajadorDniAndSeccionNombre("11111111A", "Horno")).thenReturn(Optional.empty());
        // Indicamos al Repository de Mokito que el trabajador ya tiene 2h gastadas en la tienda (le quedan 6h de sus 8h)
        when(asignacionRepository.sumHorasAsignadasByTrabajadorDni("11111111A")).thenReturn(2); 

        // Ejecutamos el proceso de asignar trabajador
        Asignacion resultado = trabajadorService.asignarTrabajadorToSeccion("11111111A", "Horno", 4);

        // Verificamos que se ha creado una asignacion nueva
        assertNotNull(resultado);
        // Verificamos que la nueva asignacion tiene 4 horas
        assertEquals(4, resultado.getHorasAsignadas());
        // Verificamos que se llamó a guardar una instancia de asignacion exactamente una vez
        verify(asignacionRepository, times(1)).save(any(Asignacion.class));
    }

    @Test
    void asignarTrabajador_AsignacionExistente_ActualizaCorrectamente() 
    {
        // Configuramos una nueva seccion que si exista
        Seccion seccion = new Seccion();
        seccion.setNombre("Horno");
        // Configuramos las aptitudes requeridas para esta seccion
        Aptitud aptitudRequerida = new Aptitud("Hornear Pan");
        seccion.setAptitudesRequeridas(List.of(aptitudRequerida));
        // Configuramos un trabajador que tiene la aptitud requerida
        trabajadorBase.setAptitudesAdquiridas(List.of(aptitudRequerida));

        // Configuramos una asignación previa de 2 horas en el Horno
        Asignacion asignacionPrevia = new Asignacion(trabajadorBase, seccion, 2);
        
        // Indicamos al Repository de Mokito que encuentre al trabajador
        when(trabajadorRepository.findById("11111111A")).thenReturn(Optional.of(trabajadorBase));
        // Indicamos al Repository de Mokito que encuentre la seccion
        when(seccionRepository.findById("Horno")).thenReturn(Optional.of(seccion));
        // Indicamos al Repository de Mokito que encuentre la asignacion previa del horno
        when(asignacionRepository.findByTrabajadorDniAndSeccionNombre("11111111A", "Horno")).thenReturn(Optional.of(asignacionPrevia));
        // Indicamos al Repository de Mokito que en todas las secciones tiene 4h (2h aquí + 2h en otro lado)
        when(asignacionRepository.sumHorasAsignadasByTrabajadorDni("11111111A")).thenReturn(4); 
        
        // Ejecutamos el proceso de asignar trabajador le sumamos 3 horas a la sección del horno (2 previas + 3 nuevas = 5 horas)
        // Horas totales = (4 - 2) + 5 = 7 horas totales de contrato (es válido porque <= 8)
        Asignacion resultado = trabajadorService.asignarTrabajadorToSeccion("11111111A", "Horno", 3);

        // Verificamos que se ha creado una asignacion nueva
        assertNotNull(resultado);
        // Verificamos que la nueva asignacion tiene 5 horas
        assertEquals(5, resultado.getHorasAsignadas());
        // Verificamos que se guardó la misma instancia que ya existía, sin crear una nueva
        verify(asignacionRepository, times(1)).save(asignacionPrevia);
    }
    
    @Test
    void asignarTrabajador_TrabajadorNoExiste_LanzaExcepcion() 
    {
    	// Indicamos al Repository de Mokito que no encuentre al trabajador
        when(trabajadorRepository.findById("99999999Z")).thenReturn(Optional.empty());
        // Ejecutamos el proceso de asignar trabajador y obtenemos la excepcion programada
        RuntimeException excepcion = assertThrows(RuntimeException.class, () -> 
        {
            trabajadorService.asignarTrabajadorToSeccion("99999999Z", "Horno", 4);
        });
        // Validamos que el mensaje es exactamente el programado
        assertEquals("Trabajador no encontrado", excepcion.getMessage());
        // Verificamos que nunca se llegó a llamar al método save de la base de datos
        verify(asignacionRepository, never()).save(any(Asignacion.class));
    }

    @Test
    void asignarTrabajador_SeccionNoExiste_LanzaExcepcion() 
    {
    	// Indicamos al Repository de Mokito que el trabajador existe
        when(trabajadorRepository.findById("11111111A")).thenReturn(Optional.of(trabajadorBase));
        // Indicamos al Repository de Mokito que la seccion no existe
        when(seccionRepository.findById("SeccionInventada")).thenReturn(Optional.empty());
        // Ejecutamos el proceso de asignar trabajador y obtenemos la excepcion programada
        RuntimeException excepcion = assertThrows(RuntimeException.class, () -> 
        {
            trabajadorService.asignarTrabajadorToSeccion("11111111A", "SeccionInventada", 4);
        });
        // Validamos que el mensaje es exactamente el programado
        assertEquals("Seccion no encontrada", excepcion.getMessage());
        // Verificamos que nunca se llegó a llamar al método save de la base de datos
        verify(asignacionRepository, never()).save(any(Asignacion.class));
    }

    @Test
    void asignarTrabajador_SinAptitudes_LanzaExcepcion() 
    {
        // Configuramos una nueva seccion que si exista
        Seccion seccionHorno = new Seccion();
        seccionHorno.setNombre("Horno");
        // Configuramos las aptitudes requeridas para esta seccion
        Aptitud aptitudRequerida = new Aptitud("Hornear Pan");
        seccionHorno.setAptitudesRequeridas(List.of(aptitudRequerida));
        // Configuramos un trabajador que no tiene ninguna aptitud
        trabajadorBase.setAptitudesAdquiridas(new ArrayList<>());
        // Indicamos al Repository de Mokito que el trabajador existe
        when(trabajadorRepository.findById("11111111A")).thenReturn(Optional.of(trabajadorBase));
        // Indicamos al Repository de Mokito que la seccion existe
        when(seccionRepository.findById("Horno")).thenReturn(Optional.of(seccionHorno));
        // Ejecutamos el proceso de asignar trabajador y obtenemos la excepcion programada
        IllegalArgumentException excepcion = assertThrows(IllegalArgumentException.class, () -> 
        {
            trabajadorService.asignarTrabajadorToSeccion("11111111A", "Horno", 4);
        });
        // Validamos que el mensaje es exactamente el programado
        assertTrue(excepcion.getMessage().contains("no posee ninguna aptitud para trabajar en la sección"));
        // Verificamos que nunca se llegó a llamar al método save de la base de datos
        verify(asignacionRepository, never()).save(any(Asignacion.class));
    }

    @Test
    void asignarTrabajador_SuperaHorasContrato_LanzaExcepcion() 
    {
        // Configuramos una nueva seccion que si exista
        Seccion seccionHorno = new Seccion();
        seccionHorno.setNombre("Horno");
        // Configuramos las aptitudes requeridas para esta seccion
        Aptitud aptitudRequerida = new Aptitud("Hornear Pan");
        seccionHorno.setAptitudesRequeridas(List.of(aptitudRequerida));
        // Configuramos un trabajador que tiene la aptitud requerida
        trabajadorBase.setAptitudesAdquiridas(List.of(aptitudRequerida));
        // Indicamos al Repository de Mokito que el trabajador existe
        when(trabajadorRepository.findById("11111111A")).thenReturn(Optional.of(trabajadorBase));
        // Indicamos al Repository de Mokito que la seccion existe
        when(seccionRepository.findById("Horno")).thenReturn(Optional.of(seccionHorno));
        // Indicamos al Repository de Mokito que el trabajador no tiene asignaciones previas en esta sección
        when(asignacionRepository.findByTrabajadorDniAndSeccionNombre("11111111A", "Horno")).thenReturn(Optional.empty());
        // Indicamos al Repository de Mokito que el total de horas del trabajador es de 5 horas gastadas en otras secciones
        when(asignacionRepository.sumHorasAsignadasByTrabajadorDni("11111111A")).thenReturn(5);
        // Ejecutamos el proceso de asignar trabajador y obtenemos la excepcion programada 
        IllegalArgumentException excepcion = assertThrows(IllegalArgumentException.class, () -> 
        {
        	// Intentamos asignarle 4 horas más. 5 + 4 = 9 (Supera las 8 de contrato)
            trabajadorService.asignarTrabajadorToSeccion("11111111A", "Horno", 4);
        });
        // Validamos que el mensaje es exactamente el programado
        assertEquals("El trabajador no tiene suficientes horas disponibles", excepcion.getMessage());
        // Verificamos que nunca se llegó a llamar al método save de la base de datos
        verify(asignacionRepository, never()).save(any(Asignacion.class));
    }
    
    // -- ------------------------ --
    // -- TODO ELIMINAR TRABAJADOR --
    // -- ------------------------ --

    @Test
    void eliminarTrabajador_DniValido_EjecutaBorradosEnOrden() 
    {
        // Configuramos al trabajador que queremos borrar
        String dni = "11111111A";
        // Ejecutamos el proceso de eliminar trabajador
        trabajadorService.eliminarTrabajador(dni);
        // Verificamos que se llamó a los dos métodos de borrado de los repositorios
        verify(asignacionRepository, times(1)).deleteByTrabajadorDni(dni);
        verify(trabajadorRepository, times(1)).deleteById(dni);
    }

    @Test
    void eliminarTrabajador_FalloAlBorrarTrabajador_PropagaExcepcion() 
    {
    	// Configuramos al trabajador que queremos borrar 
        String dni = "99999999Z";
        // Indicamos al Repository de Mokito que cuando el repositorio intente borrar el trabajador, la base de datos lance un error
        doThrow(new RuntimeException("Error fatal en la BD al borrar")).when(trabajadorRepository).deleteById(dni);
        // Ejecutamos el proceso de asignar trabajador y obtenemos la excepcion programada 
        RuntimeException excepcion = assertThrows(RuntimeException.class, () -> 
        {
            trabajadorService.eliminarTrabajador(dni);
        });
        // Verificamos que se llamó a los dos métodos de borrado de los repositorios
        assertEquals("Error fatal en la BD al borrar", excepcion.getMessage());
        // verificamos que antes del error, sí se intentaron borrar las asignaciones
        verify(asignacionRepository, times(1)).deleteByTrabajadorDni(dni);
    }
    
}