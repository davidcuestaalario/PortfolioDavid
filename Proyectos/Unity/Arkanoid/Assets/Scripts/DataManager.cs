using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class DataManager : MonoBehaviour
{
    // ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //

    // ---------------- Nivel ----------------- //
    private int nivelActual;

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //

    public static DataManager Instancia { get ; private set; }
    void Awake()
    {
        // -------------- Singelton -------------- //
        if( Instancia != null && Instancia != this ){ Destroy( this ); }
        else{ Instancia = this; }
        DontDestroyOnLoad( this.gameObject );
        // ---------------- Nivel ----------------- //
        // Seleccionamos el primer nivel
        this.nivelActual = 1;
    }

    // ######################################## //
    // ########### GETERS Y SETERS ############ //
    // ######################################## //

    public int getNivelActual( ){ return this.nivelActual; }
    
    public void setNivelActual( int pNivelActual ){ this.nivelActual = pNivelActual; }

}
