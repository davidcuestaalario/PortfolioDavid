using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Objetivo : MonoBehaviour
{
	// ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //
	
    // -------------- Constantes -------------- //
	
    [SerializeField] private float retrasoDelReinicio;

    // --------------- Variables -------------- //
	
    [SerializeField] private Transform suelo;
    [SerializeField] private Transform isla;
 
	// ----------------- Flags ---------------- //
	
	// ---------------- Modelo ---------------- //

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //
    
	void Awake(){}
    void Start(){}
	
    // ######################################## //
    // ########## GETTERS Y SETTERS ########### //
    // ######################################## //
	
    // ######################################## //
    // ############### EVENTOS ################ //
    // ######################################## //

    private void OnTriggerEnter( Collider pColider )
    {
        if( pColider.CompareTag("Jugador") )
        { 
            pColider.transform.parent.gameObject.GetComponent<AgentePelota>().alcanzarObjetivo();
            Invoke( "reiniciarObjetivo" , this.retrasoDelReinicio ); 
        }
    }

    // ######################################## //
    // ############## COLISIONES ############## //
    // ######################################## //

    // ######################################## //
    // ############## CORRUTINAS ############## //
    // ######################################## //
    
    // ######################################## //
    // ################ FLUJO ################# //
    // ######################################## //

    void Update()
    {
        //if( Input.anyKeyDown ){ reiniciarObjetivo(); }
    }

    // ######################################## //
    // ############## ESPECIALES ############## //
    // ######################################## //

    public void reiniciarObjetivo()
    {
        // Calculamos el area de despliege
        float areaDespliege_X = this.suelo.localScale.x - 1;
        float areaDespliege_Z = this.suelo.localScale.z - 1;
        float altura = this.suelo.localScale.y + 1;
        // Calculamos la nueva posicion del objetivo
        float posicion_X = Random.Range( -areaDespliege_X/2 , (areaDespliege_X - 1)/2 );
        float posicion_Z = Random.Range( -areaDespliege_Z/2 , (areaDespliege_Z - 1)/2 );
        // Calculamos la posicion del area de despliege
        posicion_X = posicion_X + this.isla.localPosition.x;
        posicion_Z = posicion_Z + this.isla.localPosition.z;
        altura = altura + this.isla.localPosition.y;
        // Teletransportamos al objetivo
        this.transform.position = new Vector3( posicion_X , altura , posicion_Z );
    }

    // ######################################## //
    // ################ DEBUG ################# //
    // ######################################## //
}
