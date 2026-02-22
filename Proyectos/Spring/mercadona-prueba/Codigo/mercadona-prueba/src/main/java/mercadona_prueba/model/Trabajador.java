package mercadona_prueba.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.JoinTable;
import jakarta.persistence.ManyToMany;

@Entity
public class Trabajador 
{
    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    
	/** El DNI del trabajador sera nuestra clave primaria */
    @Id private String dni;
    /** Nombre del trabajador */
    @Column(nullable = false) 
    private String nombre;
    /** Apellidos del trabajador */
    @Column(nullable = false) 
    private String apellidos;
    /** Numero de horas establecidas en el contrato del trabajador */
    @Column(nullable = false) 
    private Integer horasContrato;

    /** Referencia a la tienda en la ue trabaja el trabajador */
    // @ManyToOne indica que muchos Trabajadores pueden pertenecer a Una Tienda
    // @JoinColumn crea la columna "codigo_tienda" como Clave Foránea (FK) en la tabla Trabajador.
    @ManyToOne
    @JoinColumn(name = "codigo_tienda", nullable = false)
    private Tienda tienda;

    // Un trabajador puede tener muchas aptitudes y cada aptitud la pueden tener muchos trabajadores
    /** Listado de aptitudes que el trabajador posee */
    @ManyToMany
    @JoinTable
    (
        name = "trabajador_aptitud", // Nombre de la tabla intermedia que Spring creará automaticamente
        joinColumns = @JoinColumn(name = "dni_trabajador"),
        inverseJoinColumns = @JoinColumn(name = "nombre_aptitud")
    )
    private List<Aptitud> aptitudesAdquiridas;

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
    
    public Trabajador() { }

    public Trabajador(String dni, String nombre, String apellidos, Integer horasContrato, Tienda tienda) 
    {
        this.dni = dni;
        this.nombre = nombre;
        this.apellidos = apellidos;
        this.horasContrato = horasContrato;
        this.tienda = tienda;
    }

    // -- ---------------------- --
    // -- TODO GETTERS Y SETTERS --
    // -- ---------------------- --
    
    // DNI del trabajador
    public String getDni() { return dni; }
    public void setDni(String dni) { this.dni = dni; }
    
    // Nombre del trabajador
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    // Apellidos del trabajador
    public String getApellidos() { return apellidos; }
    public void setApellidos(String apellidos) { this.apellidos = apellidos; }
    
    // Horas maximas que el trabajador puede trabajar
    public Integer getHorasContrato() { return horasContrato; }
    public void setHorasContrato(Integer horasContrato) { this.horasContrato = horasContrato; }
    
    // Tienda en la que trabaja el trabajador (Solo una)
    public Tienda getTienda() { return tienda; }
    public void setTienda(Tienda tienda) { this.tienda = tienda; }
    
    // Listado de aptitudes que el trabajador posee
    public List<Aptitud> getAptitudesAdquiridas() { return aptitudesAdquiridas; }
    public void setAptitudesAdquiridas(List<Aptitud> aptitudesAdquiridas) { this.aptitudesAdquiridas = aptitudesAdquiridas; }
}