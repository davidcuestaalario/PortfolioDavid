package mercadona_prueba.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Column;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.JoinColumn;

//NOTAS:
//* Cuando un trabajador puede estar en muchas secciones y una sección puede tener muchos trabajadores, se genera una relación "Muchos a Muchos". 
//  El problema es que en Spring Boot, si usamos la anotación simple @ManyToMany, no podemos guardar información extra
//  Por eso, la solución profesional y más escalable es crear una nueva Entidad que represente esa asignación específica.
//* En una base de datos estricta, la clave primaria de esta tabla intermedia suele ser la combinación del dni y el nombre_seccion (una clave compuesta). 
//  Sin embargo, en Spring Boot (JPA), programar claves compuestas requiere crear clases adicionales y complica bastante el código inicial.
//  Como mi objetivo es mantener esto simple voy a optar por inventar una clave primaria única 
//  Esta clave primaria será un número correlativo autogenerado para cada asignación. 
//  Esto hace que el código sea mucho más limpio y fácil de entender, pero en casos reales habría que tirar por crear una clase adicional para la clave compuesta. 
//  Esto sería crear como @Id de esta clase una clase AsignacionPK que tuviera como atributos el dni del trabajador y el nombre de la sección. 
//  Así se mantendrá la restricción de tener un único @Id pero en realidad serian dos

@Entity
public class Asignacion 
{
    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    
    // @GeneratedValue hace que H2 asigne automáticamente un ID autoincremental (1, 2, 3...)
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; 
    
    /** Referencia al trabajador que puede trabajar en muchas secciones */
    @ManyToOne @JoinColumn(name = "dni_trabajador", nullable = false)
    private Trabajador trabajador;
    
    /** Referencia a la seccion en la que pueden trabajar muchos trabajadores */
    @ManyToOne @JoinColumn(name = "nombre_seccion", nullable = false)
    private Seccion seccion;
    
    /** Numero de horas asignadas para este trabajador en esta seccion */
    @Column(nullable = false)
    private Integer horasAsignadas;

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
    
    public Asignacion() { }

    public Asignacion(Trabajador trabajador, Seccion seccion, Integer horasAsignadas) 
    {
        this.trabajador = trabajador;
        this.seccion = seccion;
        this.horasAsignadas = horasAsignadas;
    }

    // -- ---------------------- --
    // -- TODO GETTERS Y SETTERS --
    // -- ---------------------- --
    
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public Trabajador getTrabajador() { return trabajador; }
    public void setTrabajador(Trabajador trabajador) { this.trabajador = trabajador; }

    public Seccion getSeccion() { return seccion; }
    public void setSeccion(Seccion seccion) { this.seccion = seccion; }

    public Integer getHorasAsignadas() { return horasAsignadas; }
    public void setHorasAsignadas(Integer horasAsignadas) { this.horasAsignadas = horasAsignadas; }
}