using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pelota : MonoBehaviour
{
    
    // ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //

    // ---------------- Pelota ---------------- //

    // Rigid Body
    private Rigidbody2D pelota;

    // Velocidad
    [Header("Control de Velocidad")]
    [SerializeField] [Range(0,100)] private float velocidadIncrementada = 5f;
    [SerializeField] private Vector2 velocidadInicial;

    // Posicion de lanzamiento
    [Header("Creacion de Pelotas")]
    [SerializeField] private GameObject posicionLanzamiento;
    [SerializeField] private GameObject prefabPelota;

    // Efectos de Sonido
    [Header("Efectos de Sonido")]
    [SerializeField] private AudioClip audioPelotaDestruccion;
    [SerializeField] private AudioClip audioPelotaRebote;

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //

    void Awake()
    {
        // ---------------- Pelota ---------------- //
        // Rigid Body: 
        this.pelota = GetComponent<Rigidbody2D>();
    }

    void Start()
    {
        // ---------------- Pelota ---------------- //
        // establecemos la velocidad inicial de la pelota
        this.pelota.velocity = new Vector2( 0 , 0 );
        // Seteamos la escala de la pelota
        //this.transform.localScale = new Vector3( 0.5f , 0.5f , 0.5f );
        // Añadimos la nueva pelota al GameManager
        GameManager.Instancia.NotificarCreacionPelota( this.gameObject );
    }

    public void lanzarPelota()
    {
        // Si tiene padre se desincula
        if ( transform.parent != null ){ transform.parent = null; }
        // Desvinculamos la pelota del Personaje
        transform.parent = null;
        // Le asignamos la velocidad inicial
        this.pelota.velocity = this.velocidadInicial;
    }

    public void duplicarPelota( )
    {
        Instantiate( prefabPelota , this.posicionLanzamiento.transform.position , this.posicionLanzamiento.transform.rotation );
    }

    public void fijarPadre( GameObject pPersonaje ){ this.transform.SetParent( pPersonaje.transform ); }

    // ######################################## //
    // ################ FLUJO ################# //
    // ######################################## //

    // Update is called once per frame
    void Update(){}

    // ######################################## //
    // ############## MOVIMIENTO ############## //
    // ######################################## //

    private void incrementarDificultad( float pDificultad )
    {
        // Incrementamos la dificultad
        this.pelota.velocity *= 1 + pDificultad/100;
        // Reproducimos un sonido de rebote
        MusicManager.Instancia.reproducirEfecto( this.audioPelotaRebote );
    }

    private void destruirPelota( )
    {
        // Notificamos al GameManager
        GameManager.Instancia.NotificarDestruccionPelota( this.gameObject );
        // Reproducimos un sonido de destruccion
        MusicManager.Instancia.reproducirEfecto( this.audioPelotaDestruccion );
        // Destruimos la pelota
        Destroy( this.gameObject );
    }

    // ######################################## //
    // ############## COLISIONES ############## //
    // ######################################## //

    private void OnCollisionEnter2D( Collision2D pColision )
    {
        // Si la colsion fue contra un Bloque, lo destruimos
        if( pColision.gameObject.CompareTag("Bloque") ){ pColision.gameObject.GetComponent<Bloque>().destruirBloque(); }
        // Si la colsion fue contra el Personaje, incrementamos la dificultad
        if( pColision.gameObject.CompareTag("Player") ){ incrementarDificultad( this.velocidadIncrementada ); }
        // Si la colision fue contra el fin del escenario, Destruimos la pelota
        if( pColision.gameObject.CompareTag("Suelo") ){ this.destruirPelota(); }
        // Si la colision fue contra la pared reproducimos un sonido derebote
        if( pColision.gameObject.CompareTag("Pared") ){ MusicManager.Instancia.reproducirEfecto( this.audioPelotaRebote ); }
    }
}
