using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Pelota : MonoBehaviour
{
	// ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //
	
    // -------------- Constantes -------------- //
	
    // --------------- Variables -------------- //
	
    [SerializeField] private float aceleracion = 300f;

	// ----------------- Flags ---------------- //
	
	// ---------------- Modelo ---------------- //

    // Pelota
    private Rigidbody pelota;

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //
    
	void Awake(){}
    void Start()
    {
        // Pelota
        this.pelota = GetComponent<Rigidbody>();
    }
	
    // ######################################## //
    // ########## GETTERS Y SETTERS ########### //
    // ######################################## //
	
    // ######################################## //
    // ############### EVENTOS ################ //
    // ######################################## //

    // ######################################## //
    // ############## COLISIONES ############## //
    // ######################################## //

    // ######################################## //
    // ############## CORRUTINAS ############## //
    // ######################################## //
    
    // ######################################## //
    // ################ FLUJO ################# //
    // ######################################## //

    void FixedUpdate(){ movimiento(); }
    void Update(){}

    // ######################################## //
    // ############## ESPECIALES ############## //
    // ######################################## //

    // -------------- Movimiento -------------- //

    private void movimiento()
    {
        // Capturamos los imputs de movimiento
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        // Calculamos la direccion del movimiento
        Vector3 movimiento = new Vector3( horizontal , 0 , vertical );
        // Aplicamos una fuerza en la direccion del movimiento
        pelota.AddForce( movimiento * this.aceleracion * Time.deltaTime );
    }

    // ######################################## //
    // ################ DEBUG ################# //
    // ######################################## //
}
