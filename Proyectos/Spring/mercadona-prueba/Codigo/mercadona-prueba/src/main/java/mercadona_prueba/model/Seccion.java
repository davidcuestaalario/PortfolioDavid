package mercadona_prueba.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;
import jakarta.persistence.JoinColumn;
import java.util.List;

import jakarta.persistence.Column;

@Entity
public class Seccion 
{
    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    
	/** El nombre será nuestra Clave Primaria (Horno, Cajas...) */
    @Id private String nombre; 
    /** Numero de horas necesarias en cada seccion */
    @Column(nullable = false) 
    private Integer horasNecesarias;

    // Una seccion puede requerir muchas aptitudes y una aptitud puede ser requerida por mas de una seccion
    /** Listado de aptitudes requeridas para trabajar en la seccion */
    @ManyToMany
    @JoinTable
    (
        name = "seccion_aptitud", // Nombre de la tabla intermedia que Spring creará automaticamente
        joinColumns = @JoinColumn(name = "nombre_seccion"),
        inverseJoinColumns = @JoinColumn(name = "nombre_aptitud")
    )
    private List<Aptitud> aptitudesRequeridas;

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
    
    public Seccion() { }

    public Seccion(String nombre, Integer horasNecesarias) 
    {
        this.nombre = nombre;
        this.horasNecesarias = horasNecesarias;
    }

    // -- ---------------------- --
    // -- TODO GETTERS Y SETTERS --
    // -- ---------------------- --
    
    // Nombre de la seccion
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    // Horas requeridas en la seccion
    public Integer getHorasNecesarias() { return horasNecesarias; }
    public void setHorasNecesarias(Integer horasNecesarias) { this.horasNecesarias = horasNecesarias; }
    
    // Aptitudes necesarias para la seccion
    public List<Aptitud> getAptitudesRequeridas() { return aptitudesRequeridas; }
    public void setAptitudesRequeridas(List<Aptitud> aptitudesRequeridas) { this.aptitudesRequeridas = aptitudesRequeridas; }
    
}