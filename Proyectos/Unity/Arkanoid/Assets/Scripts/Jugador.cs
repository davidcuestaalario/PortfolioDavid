using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Jugador : MonoBehaviour
{
    
    // ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //

    // -------------- Personaje --------------- //

    // Velocidad
    [SerializeField] private float velocidad;
    [SerializeField] [Range(0,100)] private float velocidadIncrementada = 10;
    
    // Margen
    [SerializeField] private float margen = 6.6f;

    // Posicion de lanzamiento
    [SerializeField] private GameObject posicionLanzamiento;
    
    // ######################################## //
    // ########### GETERS Y SETERS ############ //
    // ######################################## //

    public Transform getPosicionLanzamiento(){ return this.posicionLanzamiento.transform; }

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //

    void Start(){}

    // ######################################## //
    // ################ FLUJO ################# //
    // ######################################## //
    
    void Update()
    {
        // Ejecuta el movimiento del Personaje
        movimiento();
    }

    // ######################################## //
    // ############## MOVIMIENTO ############## //
    // ######################################## //

    private void movimiento()
    {
        // Leemos el Imput del eje Horizontal
        float direccion = Input.GetAxis("Horizontal");
        // Leemos la posicion actual del Personaje
        Vector2 posicion = transform.position;

        // Calculamos el movimiento del Personaje
        float movimiento = direccion * Time.deltaTime * this.velocidad;
        // Incrementamos la posicion del perosnaje en funcion de su movimiento
        posicion.x += movimiento;
        // Limitamos la posicion del Personaje a los margenes establecidos
        posicion.x = Mathf.Clamp( posicion.x , -this.margen , this.margen );

        // Ejecuta el movimiento
        transform.position = posicion;
    }

    public void incrementarVelocidad()
    {
        this.velocidad *= 1 + velocidadIncrementada/100; 
    }

    // ######################################## //
    // ############## COLISIONES ############## //
    // ######################################## //

    private void OnCollisionEnter2D( Collision2D pColision )
    {
        // Si la colsion fue contra un Bloque, lo destruimos
        if( pColision.gameObject.CompareTag("Premio") ){ pColision.gameObject.GetComponent<Premio>().premiar(); }
    }
}
