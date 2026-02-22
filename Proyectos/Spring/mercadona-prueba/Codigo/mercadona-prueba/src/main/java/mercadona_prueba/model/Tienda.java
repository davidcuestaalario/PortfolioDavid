package mercadona_prueba.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Column;

@Entity
public class Tienda 
{
    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    
	/** Clave primaria de la Tienda */
    @Id private Integer codigo;
    /** Nombre de la tienda */
    @Column(nullable = false) 
    private String nombre;

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
    
    public Tienda(){ }

    public Tienda(Integer codigo, String nombre) 
    {
        this.codigo = codigo;
        this.nombre = nombre;
    }
    
    // -- ---------------------- --
    // -- TODO GETTERS Y SETTERS --
    // -- ---------------------- --
    
    // Codigo
    public Integer getCodigo() { return codigo; }
    public void setCodigo(Integer codigo) { this.codigo = codigo; }

    // Nombre
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    
}

