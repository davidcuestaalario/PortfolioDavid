package mercadona_prueba.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class Aptitud 
{
    // -- -------------- --
    // -- TODO ATRIBUTOS --
    // -- -------------- --
    
    @Id private String nombre;

    // -- ---------------- --
    // -- TODO CONSTRUCTOR --
    // -- ---------------- --
    
    public Aptitud() {}

    public Aptitud(String nombre) { this.nombre = nombre; }

    // -- ---------------------- --
    // -- TODO GETTERS Y SETTERS --
    // -- ---------------------- --
    
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
}