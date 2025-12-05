using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    // ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //

    [Header("Opciones")]
    [SerializeField] private float retardoEntreNiveles = 1f;

    // -------------- Personaje --------------- //
    private GameObject personaje;

    // --------------- Bloque ---------------- //
    private int bloques;

    // --------------- Bolas ---------------- //
    private List<GameObject> pelotas;

    // --------------- Musica --------------- //
    [Header("Efectos de Sonido")]
    [SerializeField] private AudioClip audioMusic1;
    [SerializeField] private AudioClip audioMusic2;
    [SerializeField] private AudioClip audioMusicWin;

    // --------------- Flags ---------------- //
    private bool partidaIniciada;

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //

    public static GameManager Instancia { get ; private set; }
    void Awake()
    {
        // -------------- Singelton -------------- //
        if( Instancia != null && Instancia != this ){ Destroy( this ); }
        else{ Instancia = this; }
        // --------------- Bloque ---------------- //
        // Contamos cuantos bloques hay en la escena
        this.bloques = GameObject.FindGameObjectsWithTag("Bloque").Length;
        // --------------- Bolas ---------------- //
        this.pelotas = new List<GameObject>();
        // -------------- Personaje --------------- //
        this.personaje = GameObject.FindGameObjectWithTag("Player");
        // --------------- Flags ---------------- //
        this.partidaIniciada = false;       
    }

    void Start()
    {
        // Establecemos la musica de antes de iniciar el Juego
        MusicManager.Instancia.reproducirMusica( this.audioMusic1 );
    }

    public void iniciarPartida()
    {
        // Indicamos que la partida se ha iniciado
        this.partidaIniciada = true;
        // Establecemos la musica de la partida
        MusicManager.Instancia.reproducirMusica( this.audioMusic2 );
        // Lanzamos todas las Pelotas
        foreach( GameObject pelota in this.pelotas ){ pelota.GetComponent<Pelota>().lanzarPelota(); }
    }

    // ######################################## //
    // ############ NOTIFICACIONES ############ //
    // ######################################## //

    public void NotificarDestruccionBloque()
    {
        // Reducimos en uno el numero de bloques restantes
        this.bloques--;
        // Si no quedan bloques en la escena se termina la partida
        if( this.bloques <= 0 ){ this.siguienteNivel(); }
    }

    public void NotificarDestruccionPelota( GameObject pPelota )
    {
        // Eliminamos la bola destruida
        this.pelotas.Remove( pPelota );
        // Si no quedan bolas en la escena se termina la partida
        if( this.pelotas.Count <= 0 ){ this.repetireNivel(); }
    }

    public void NotificarCreacionPelota( GameObject pPelota )
    {
        // Añadimos la nueva pelota a la lista
        this.pelotas.Add( pPelota );
        // Si la partida ya esta iniciada, Lanzamos la pelota
        if( this.partidaIniciada ){ pPelota.GetComponent<Pelota>().lanzarPelota(); }
        // Si la partida no esta iniciada y existe el jugador, Vinculamos la pelota al jugador
        else if( this.personaje != null ) { pPelota.GetComponent<Pelota>().fijarPadre( this.personaje ); }
        Debug.Log( "Partida Iniciada: " + this.partidaIniciada.ToString() );
    }

    // ######################################## //
    // ############### ESCENAS ################ //
    // ######################################## //

    private void siguienteNivel( )
    {
        // Si existe la siguiente escena
        int siguienteEscena = SceneManager.GetActiveScene().buildIndex + 1 ;
        if( Application.CanStreamedLevelBeLoaded( siguienteEscena ) )
        {
            // Reproducimos la musica de victoria
            MusicManager.Instancia.reproducirMusica( this.audioMusicWin );
            // Cargamos la siguiente escena
            Invoke ( "siguienteEscena" , this.retardoEntreNiveles );
            // Informamos del cambio de escena
            DataManager.Instancia.setNivelActual( siguienteEscena );
        }
        // Si no existe la siguiente escena
        else
        {
            // Volvemos al menu principal
            abrirMenuPrincipal( );
            // Reiniciamos el contador de escenas
            DataManager.Instancia.setNivelActual( 1 );
        }
    }

    private void siguienteEscena( )
    {
        SceneManager.LoadScene( SceneManager.GetActiveScene().buildIndex + 1 );
    }

    private void repetireNivel( )
    {
        // Cargamos de nuevo esta escena
        SceneManager.LoadScene( SceneManager.GetActiveScene().buildIndex );
    }

    private void abrirMenuPrincipal( )
    {
        // Cargamos el menu principal
        SceneManager.LoadScene( 0 );

    }

    // ######################################## //
    // ################ FLUJO ################# //
    // ######################################## //

    // Update is called once per frame
    void Update()
    {
        // Con la R Reiniciamos el Nivel
        if( Input.GetKeyDown( KeyCode.R ) ){ this.repetireNivel(); }
        // Con la tecla L Pasamos al siguiente nivel
        if( Input.GetKeyDown( KeyCode.L ) ){ this.siguienteNivel(); }
        // Con la tecla Escape volvemos al menu principal
        if( Input.GetKeyDown( KeyCode.Escape ) ){ this.abrirMenuPrincipal(); }
        // Con la Barra espaciadora Iniciamos la partida
        if( !this.partidaIniciada && Input.GetKeyDown( KeyCode.Space ) ){ iniciarPartida(); }
    }


    // ######################################## //
    // ############## FUNCIONES ############### //
    // ######################################## //

    public void premiar( TipoPremio pPremio )
    {
        // Si el premio es duplicar las bolas Duplicamos cada pelota que exista
        if( pPremio == TipoPremio.DuplicarBolas )
        {
            // Creamos un Vector Auxiliar con las pelotas existentes
            List<GameObject> bolas = new List<GameObject>();
            foreach( GameObject pelota in this.pelotas ){ bolas.Add( pelota ); }
            // Si la partida ya ha iniciado duplicamos cada Bola
            if( this.partidaIniciada ){ foreach( GameObject bola in bolas ){ bola.GetComponent<Pelota>().duplicarPelota(); } }
            // Si la partida no ha iniciado incrementamos la velocidad del jugador
            else{ this.personaje.GetComponent<Jugador>().incrementarVelocidad(); }
        }
        // Si el premio es incrementar la velocidad del jugador
        else if( pPremio == TipoPremio.IncrementarVelocidad )
        {
            this.personaje.GetComponent<Jugador>().incrementarVelocidad();
        }
    }


}
