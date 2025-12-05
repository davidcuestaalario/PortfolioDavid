using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Premio : MonoBehaviour
{
    
    // ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //

    // -------------- Personaje --------------- //
    
    private TipoPremio tipoPremio;

    private SpriteRenderer premio;
    

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //

    void Start()
    {
        // Inicializamos el premio
        this.premio = GetComponent<SpriteRenderer>();
        // Elegimos el tipo de premio
        this.tipoPremio = (TipoPremio) Random.Range( 0 , 2 );
        // Seteamos el color del premio
        if( this.tipoPremio == TipoPremio.DuplicarBolas ){ premio.color = Color.blue; }
        else if( this.tipoPremio == TipoPremio.IncrementarVelocidad ){ premio.color = Color.green; }
    }

    // ######################################## //
    // ################ FLUJO ################# //
    // ######################################## //
    void Update() {}

    // ######################################## //
    // ############## FUNCIONES ############### //
    // ######################################## //

    public void premiar()
    { 
        // Destruimos el Premio
        Destroy( this.gameObject );
        // Premiamos al Jugador
        GameManager.Instancia.premiar( this.tipoPremio ); 
    }

    // ######################################## //
    // ############## COLISIONES ############## //
    // ######################################## //

    private void OnCollisionEnter2D( Collision2D pColision )
    {
        // Si la colision fue contra el fin del escenario, Destruimos el premio
        if( pColision.gameObject.CompareTag("Suelo") ){ Destroy( this.gameObject ); }
    }
}

public enum TipoPremio { DuplicarBolas , IncrementarVelocidad };
