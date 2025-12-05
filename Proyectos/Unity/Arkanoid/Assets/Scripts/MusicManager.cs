using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Audio;

public class MusicManager : MonoBehaviour
{
    // ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //

    // ---------------- Mixer ----------------- //
    [SerializeField] private AudioMixer mixer;

    // --------------- fuentes ---------------- //
    private AudioSource[] fuentes;
    private AudioSource fuenteMusica;
    private AudioSource fuenteEfectos;

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //

    public static MusicManager Instancia { get ; private set; }
    void Awake()
    {
        // -------------- Singelton -------------- //
        if( Instancia != null && Instancia != this ){ Destroy( this ); }
        else{ Instancia = this; }
        DontDestroyOnLoad( this.gameObject );
        // --------------- fuentes ---------------- //
        // Seleccionamos los componentes audioSource
        fuentes = GetComponents<AudioSource>();
        // Asignamos los componentes audioSource 
        fuenteMusica = fuentes[0];
        fuenteEfectos = fuentes[1];
    }

    // ######################################## //
    // ########### GETERS Y SETERS ############ //
    // ######################################## //

    public AudioMixer getAudioMixer(){ return this.mixer; }


    // ######################################## //
    // ############## REPRODUCIR ############## //
    // ######################################## //

    public void reproducirMusica( AudioClip pMusica )
    {
        this.fuenteMusica.clip = pMusica;
        this.fuenteMusica.Play();
    }

    public void reproducirEfecto( AudioClip pEfecto )
    {
        this.fuenteEfectos.PlayOneShot( pEfecto );
    }

}
