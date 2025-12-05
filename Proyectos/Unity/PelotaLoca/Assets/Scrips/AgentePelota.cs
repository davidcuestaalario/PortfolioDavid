using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.MLAgents;
using Unity.MLAgents.Sensors;
using Unity.MLAgents.Actuators;

public class AgentePelota : Agent
{
	// ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //
	
    // -------------- Constantes -------------- //
	
    // --------------- Variables -------------- //
	
    // Recompensas
    [Header("Recompensas")]
    [SerializeField] private float recompensaPorAlcanzarObjetivo = 1f;
    [SerializeField] private float recompensaPorChocarPared = -0.1f;
    [SerializeField] private float multiplicadorRecompensa = 0.5f;
    [SerializeField] private float multiplicadorPenalizacion = 0.1f;
    
    // Personaje
    [Header("Personaje")]
    [SerializeField] private float aceleracion = 300f;
    [SerializeField] private Rigidbody pelota;
    private float distanciaAnterior = 0f;

    // Objetivo
    [Header("Objetivo")]
    [SerializeField] private GameObject objetivo;

	// ----------------- Flags ---------------- //
	
    [SerializeField] private bool isTraining;

	// ---------------- Modelo ---------------- //

    public string mensaje = "";

    

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //

    // Inicializacion de la clase
    override public void Initialize()
    {
        // Pelota
        //this.pelota = GetComponent<Rigidbody>();
        // Si no estamos entrenando
        if( !isTraining ){ MaxStep = 0; }
    }

    // Inicializacion de cada fase del entrenamiento
    override public void OnEpisodeBegin()
    {
        // Detenemos al agente
        this.pelota.velocity = Vector3.zero;
        this.pelota.angularVelocity = Vector3.zero;

        // Seteamos laultima distancia conocida del agente
        float distancia = Vector3.Distance( transform.position , this.objetivo.transform.position );

        // Reiniciamos el objetivo
        this.objetivo.GetComponent<Objetivo>().reiniciarObjetivo();
    }

    // ######################################## //
    // ############### ACCIONES ############### //
    // ######################################## //

    /*  
     *  [0] Movimiento Horizontal
     *  [1] Movimiento Vertical
     */

    // Ejecuta el modelo
    // Lee los imputs generados y ejecuta las acciones correspondientes
    override public void OnActionReceived( ActionBuffers pAcciones )
    {
        // Capturamos las acciones del agente
        float[] acciones = pAcciones.ContinuousActions.Array;
        int[] eventos = pAcciones.DiscreteActions.Array; 
        // Capturamos los imputs de movimiento
        float horizontal = acciones[0];
        float vertical = acciones[1];
        // Ejecutamos el movimiento
        movimiento( horizontal , vertical );
    }

    // Genera el modelo
    // Genera los imputs necesarios para ejecutar las acciones  
    override public void Heuristic( in ActionBuffers pAcciones )
    {
        // Capturamos los imputs de movimiento
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        // Calculamos la direccion del movimiento
        Vector3 movimiento = new Vector3( horizontal , 0 , vertical );
        // Capturamos las acciones del agente
        float[] acciones = pAcciones.ContinuousActions.Array;
        int[] eventos = pAcciones.DiscreteActions.Array;
        // Generamos los imputs 
        acciones[0] = movimiento.x;
        acciones[1] = movimiento.z;
        // Devolvemos las acciones 
    }

    // ######################################## //
    // ############ OBSERVACIONES ############# //
    // ######################################## //

    override public void CollectObservations( VectorSensor pSensor )
    {
        // Anadimos como observacion la distancia hasta el objetivo
        float distancia = Vector3.Distance( transform.position , this.objetivo.transform.position );
        pSensor.AddObservation( distancia );
    }

    // ######################################## //
    // ############# RECOMPENSAS ############## //
    // ######################################## //
    
    public void alcanzarObjetivo( )
    { 
        if( isTraining ){ AddReward( this.recompensaPorAlcanzarObjetivo ); }
    }

    public void chocarPared( )
    { 
        if( isTraining ){ AddReward( this.recompensaPorChocarPared ); }
    }

    private void heuristicos()
    {
        if( isTraining )
        {
            // Calculamos la distancia hasta el objetivo
            float distancia = Vector3.Distance( transform.position , this.objetivo.transform.position );
            // Calculamos la variacion de distancia entre este instante y el anterior
            float variacion = (this.distanciaAnterior - distancia) * Time.deltaTime;
            // Recompensamos al agente con la variacion de la distancia
            if( variacion > 0 ){ AddReward( variacion * this.multiplicadorRecompensa ); }
            else{ AddReward( variacion * this.multiplicadorPenalizacion ); }
            // Actualizamos la distancia del instante
            this.distanciaAnterior = distancia;
        }
    }


    // ######################################## //
    // ############## ESPECIALES ############## //
    // ######################################## //

    private void movimiento( float horizontal , float vertical )
    {
        // Calculamos la direccion del movimiento
        Vector3 movimiento = new Vector3( horizontal , 0 , vertical );
        // Aplicamos una fuerza en la direccion del movimiento
        this.pelota.AddForce( movimiento * this.aceleracion * Time.deltaTime );
    }

    // ######################################## //
    // ################ DEBUG ################# //
    // ######################################## //
}
