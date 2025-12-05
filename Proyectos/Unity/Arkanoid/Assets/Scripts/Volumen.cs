using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Audio;

public class Volumen : MonoBehaviour
{
    // ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //

    // ---------------- Mixer ----------------- //
    private AudioMixer mixer;
    [SerializeField] private string fuente;

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //
    void Start()
    {
       mixer = MusicManager.Instancia.getAudioMixer(); 
    }

    // ######################################## //
    // ################ VOLUMEN ############### //
    // ######################################## //

    public void controlarVolumen( float slider )
    {
        // Calculamos el volumen el escala logaritmica
        float volumen = Mathf.Log10( slider ) * 20;
        // Seteamos el valor al AudioMixer
        mixer.SetFloat( fuente , volumen );
    }

}
