using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Rotar : MonoBehaviour
{
        
    // ######################################## //
    // ############## VARIABLES ############### //
    // ######################################## //

    // Velocidad
    [SerializeField] private float velocidad;

    // ######################################## //
    // ############## CONSTRUCTOR ############# //
    // ######################################## //
    void Start(){ }

    
    // ######################################## //
    // ################ FLUJO ################# //
    // ######################################## //
    void Update()
    {
        rotacion();
    }

    // ######################################## //
    // ############## MOVIMIENTO ############## //
    // ######################################## //

    private void rotacion()
    {
        // Leemos la rotacion actual
        Vector3 rotacion = transform.rotation.eulerAngles;
        // Incrementamos la rotacion en funcion de la velocidad
        rotacion.z += Time.deltaTime * this.velocidad;
        // Limitamos la rotacion
        if( rotacion.z >= 360 ){ rotacion.z = 0; }
        // Ejecuta la rotacion
        transform.rotation = Quaternion.Euler( rotacion );
    }
}
