using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Bloque : MonoBehaviour
{
    // ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //

    // --------------- Bloque ---------------- //
    
    // Bloque
    private SpriteRenderer bloque;
    
    // Tipo de Bloque 
    [Header("Propiedades del BLoque")]
    [SerializeField] [Range(1,4)] private int nivel = 4;
    [SerializeField] private ColorBloque color = ColorBloque.Violeta;
    [SerializeField] private bool randomizar = false;

    // Tipo de Bloque 
    [Header("Propiedades de la Recompensa")]
    [SerializeField] [Range(0,100)] private int probabilidad = 5;
    [SerializeField] private GameObject recompensa;

    // Sprites
    [Header("Sprites para los niveles")]
    [SerializeField] private List<Sprite> bloquesVioletas;
    [SerializeField] private List<Sprite> bloquesRojos;
    [SerializeField] private List<Sprite> bloquesVerdes;
    [SerializeField] private List<Sprite> bloquesAzules;

    // Efectos de Particulas
    [Header("Efectos de Particulas")]
    [SerializeField] private ParticleSystem particleBloqueDestruccion;

    // Efectos de Sonido
    [Header("Efectos de Sonido")]
    [SerializeField] private AudioClip audioBloqueDestruccion;

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //

    void Start()
    {
        // ------------- Randomizar -------------- //
        if( this.randomizar )
        {
            this.nivel = Random.Range( 1 , 4 );
            //this.color = (ColorBloque) Random.Range( 0 , 3 );
        }
        // --------------- Bloque ---------------- //
        this.bloque = GetComponent<SpriteRenderer>();
        asignarBloque();
    }

    private void asignarBloque()
    {
        if( this.color == ColorBloque.Violeta ){ this.bloque.sprite = bloquesVioletas[ this.nivel - 1 ]; }
        else if( this.color == ColorBloque.Azul ){ this.bloque.sprite = bloquesAzules[ this.nivel - 1 ]; }
        else if( this.color == ColorBloque.Verde ){ this.bloque.sprite = bloquesVerdes[ this.nivel - 1 ]; }
        else{ this.bloque.sprite = bloquesRojos[ this.nivel - 1 ]; }
    }

    private void generarRecompensa()
    {
        // Generamos un numero aleatorio entre uno y cien
        int random = Random.Range( 1 , 100 );
        // Se genera una recompensa si el numero generado es menor que la probabilidad
        if( this.probabilidad > random ){ Instantiate( this.recompensa , transform.position , transform.rotation ); }
    }

    // ######################################## //
    // ################ FLUJO ################# //
    // ######################################## //

    // Update is called once per frame
    void Update()
    {
        
    }

    // ######################################## //
    // ############# DESTRUCCION ############## //
    // ######################################## //

    public void destruirBloque()
    {
        // Reproducimos un sonido de destruccion
        MusicManager.Instancia.reproducirEfecto( this.audioBloqueDestruccion );
        // Reducimos en uno el nivel del Bloque
        this.nivel -= 1;
        // Si el nivel es cero 
        if( this.nivel <= 0 )
        { 
            // Instanciamos el sistema de particulas
            Instantiate( this.particleBloqueDestruccion , transform.position , Quaternion.identity );
            // Generamos la recompensa
            this.generarRecompensa();
            // Notificamos al GameManager
            GameManager.Instancia.NotificarDestruccionBloque();
            // Destruimos el Bloque
            Destroy( this.gameObject );
        }
        // En caso contrario reducimos en uno el nivel del Bloque
        else{ asignarBloque(); }
    }

}

public enum ColorBloque { Azul , Violeta , Rojo , Verde };
