using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MenuManager : MonoBehaviour
{
    // ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //


    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //
    void Start()
    {
        GameManager.Instancia.iniciarPartida();
    }

    // ######################################## //
    // ############### BOTONES ################ //
    // ######################################## //
    
    public void botonStart( )
    {
        SceneManager.LoadScene( DataManager.Instancia.getNivelActual() );
    }

    public void botonSalir( )
    {
        Application.Quit();
    }


}
