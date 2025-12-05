# -*- coding: utf-8 -*-

import Z_Utils as utilidades;
import Z_SQLReader as sql;

####################################################################    
#----------------------------- TITULOS ----------------------------#
####################################################################

def titulo( pTitulo ):
    #pId = pTitulo.replace( " " , "_" );
    informacion = "<section>"
    informacion += "     <article >"
    informacion += "           <hgroup id='equipo'> <h1> " + pTitulo + " </h1> </hgroup>"		
    informacion += "     </article>"
    informacion += "</section>"
    return informacion;

def subTitulo( pTitulo ):
    #pId = pTitulo.replace( " " , "_" );
    informacion = "<section >"
    informacion += "     <article id='equipo'>"
    informacion += "           <hgroup id='equipo'> <h2> " + pTitulo + " </h2> </hgroup>"		
    informacion += "     </article>"
    informacion += "</section>"
    return informacion;

def subTitulo_2( pTitulo ):
    #pId = pTitulo.replace( " " , "_" );
    informacion = "<section >"
    informacion += "     <article>"
    informacion += "           <hgroup id='equipo'> <h3> " + pTitulo + " </h3> </hgroup>"		
    informacion += "     </article>"
    informacion += "</section>"
    return informacion;

def mensaje( pMensaje ):
    informacion = ""
    if pMensaje != "":
       informacion += "<section id='contenido'>"
       informacion += "<br /> <span class='mensajes'> " + pMensaje + " </span> <br /> <br />"
       informacion += "</section>"
    return informacion;


####################################################################    
#-------------------------- FORMULARIOS ---------------------------#
####################################################################

def formularioRegistro( pAction , pNombre , pApellido1 , pApellido2 , pUsuario , pDNI , pTelefono , pEmail , pPassword , pPasswordRP ):
    informacion = ""
    informacion += "	<form id='registro' name='registro_frm' action='" + pAction + "' method='post'>"
    informacion += "		<fieldset>"
    informacion += "		<label for='nombre_txt'> Nombre: </label>"
    informacion += "		<input id='nombre_txt' type='text' name='nombre_txt' pattern='[A-Za-z0-9]*' placeholder='Introduzca su nombre' required value='" + pNombre + "' />"
    informacion += "		<br /> <br />"
    informacion += "		<label for='apellido1_txt'> Primer apellido: </label>"
    informacion += "		<input id='apellido1_txt' type='text' name='apellido1_txt' pattern='[A-Za-z0-9]*' placeholder='Introduzca su primer apellido' required value='" + pApellido1 + "' />"
    informacion += "		<br /> <br />"
    informacion += "		<label for='apellido2_txt'> Segundo apellido: </label>"
    informacion += "		<input id='apellido2_txt' type='text' name='apellido2_txt' pattern='[A-Za-z0-9]*' placeholder='Introduzca su segundo apellido' required value='" + pApellido2 + "' />"
    informacion += "		<br /> <br />"
    informacion += "		<label for='usuario_txt'> Usuario: </label>"
    informacion += "		<input id='usuario_txt' type='text' name='usuario_txt' pattern='[A-Za-z0-9]*' placeholder='Introduzca un nombre de usuario' title='El nombre de usuario debe ser unico' required value='" + pUsuario + "' />"
    informacion += "		<br /> <br /> <br /> <br />"
			
    informacion += "		<label for='dni_txt'> DNI: </label>"
    informacion += "		<input id='dni_txt' type='text' name='dni_txt' pattern='[0-9]{8}-[A-Za-z]{1}' placeholder='Introduzca su DNI' required value='" + pDNI + "' />"
    informacion += "		<br /> <br />"
    informacion += "		<label for='telefono_tel'> Tel&eacute;fono: </label>"
    informacion += "		<input id='telefono_tel' type='tel' name='telefono_tel' placeholder='Introduzca su numero de télefono' required value='" + pTelefono + "' />"
    informacion += "		<br /> <br />"
    informacion += "		<label for='fecha_date'> Fecha nacimiento: </label>"
    informacion += "		<input id='fecha_date' type='date' name='fecha_date' placeholder='Introduzca su fecha de nacimiento' />"
    informacion += "		<br /> <br />"
    informacion += "		<label for='email_email'> email: </label>"
    informacion += "		<input id='email_email' type='email' name='email_email' placeholder='Introduzca su e-mail' required value='" + pEmail + "' />"
    informacion += "		<br /> <br /> <br /> <br />"
			
    informacion += "		<label for='password_txt'> Contrase&ntilde;a: </label>"
    informacion += "		<input id='password_txt' type='password' name='password_txt' title='Las contraseñas deben coincidir' required value='" + pPassword + "' />"
    informacion += "		<br /> <br />"
    informacion += "		<label for='passwordRP_txt'> repite la Contrase&ntilde;a: </label>"
    informacion += "		<input id='passwordRP_txt' type='password' name='passwordRP_txt' title='Las contraseñas deben coincidir' required value='" + pPasswordRP + "' />"
    informacion += "		<br /> <br />  <br />"
			 
    informacion += "		<input type='submit' name='enviar_btn' value='Registrarse' id='procesar_POST' />"
    informacion += "		</fieldset>"
    informacion += "	</form>"
    return informacion; 

def gestionarCategoriaDistribucion( usuario , categoria_distribucion  ):
    informacion = ""
    informacion += "<table id='equipos'>"
    informacion += "<tr>"
    informacion += "    <th> CATEGORIA </th>"
    informacion += "	<th> COLOR </th>"
    informacion += "	<th>  </th>"
    informacion += "</tr>"
    
    informacion += "    <tr>"
    informacion += "        <form name='ordenar_frm' action='anadir_clasificacion_distribucion' method='post' enctype='application/x-www-form-urlencoded'> "
    informacion += "                <input type='hidden' name='categoria_distribucion' value='" + categoria_distribucion + "' />"
    informacion += "            <td>"
    informacion += "                 <input id='clase_txt' type='text' name='clase_txt' pattern='[A-Za-z0-9]*' placeholder='Asunto' required />"		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                 <input id='color_color' type='color' name='color_color' required />"		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                    <input type='submit' id='aceptar' class='editar' name='anadir_btn' value='Añadir'/>	 "			     		        		
    informacion += "            </td>"
    informacion += "        </form> " 
    informacion += "    <tr>"
    
    resultado = sql.getCategoriaDistribucion( usuario , categoria_distribucion )
    for clase , color in resultado:
        informacion += "    <tr>"
        informacion += "        <td> <h3> " + clase + " </h3> </td>"
        informacion += "        <td>"
        informacion += "            <form name='ordenar_frm' action='modificar_clasificacion_distribucion' method='post' enctype='application/x-www-form-urlencoded'> "
        informacion += "                 <input type='hidden' name='clase_hdn' value='" + clase + "' />"
        informacion += "                 <input type='hidden' name='categoria_distribucion' value='" + categoria_distribucion + "' />"
        informacion += "                 <input id='color_color' type='color' name='color_color' onchange='this.form.submit()' value='" + utilidades.colorRGBToHexadecimal(color) + "' required />"
        informacion += "            </form> "
        informacion += "        </td>"
        informacion += "        <td>"
        informacion += "            <form name='ordenar_frm' action='eliminar_clasificacion_distribucion' method='post' enctype='application/x-www-form-urlencoded'> "	   
        informacion += "                 <input type='hidden' name='categoria_distribucion' value='" + categoria_distribucion + "' />"
        informacion += "                 <input type='hidden' name='clase_hdn' value='" + clase + "' />"
        informacion += "                 <input type='submit' id='eliminar' class='editar' name='eliminar_btn' value='Eliminar'/>	 "			     		        		
        informacion += "            </form> "
        informacion += "        </td>"
        informacion += "    <tr>"
    
    informacion += "</table>"
    return informacion;
####################################################################    
#----------------------------- TABLAS -----------------------------#
####################################################################

# ---------------------------------------- #
# --------------- FINANZAS --------------- #
# ---------------------------------------- #

# pCabeceras Lista con las cabeceras
# pCuerpo diccionario de diccionarios:
# - cada diccionario de pCuerpo es una fila de la tabla
# - cada sub diccionario es la columna cuya key corresponde con la cabecera (si no estan son cero)
def tablaResumenFinanzas( pId , pResumen , pCabeceras , pCuerpo ):
    
    informacion = "<table id='" + pId + "'>"
    informacion += "<tr>"
    informacion += "    <th>              </th>"
    for cabecera in pCabeceras:
        informacion += "	<th> " + cabecera + " </th>"
    informacion += "</tr>"
     
    for gasto in pCuerpo:        
        estilo = ""
        informacion += "<tr>"
        informacion += "	<td> <h3 " + estilo + " > </br>" + gasto + " </br> </h3> </td>"
        for cabecera in pCabeceras: 
            elemento = "0";
            if cabecera in pCuerpo[gasto]:
                elemento = str( "{:.2f}".format( pCuerpo[gasto][cabecera] ) );
            informacion += "	<td> <h3 " + estilo + " > </br>" + elemento + " </br> </h3> </td>"
        informacion += "</tr>"
        
    informacion += "</table>"
    informacion += "<br />"
    
    return informacion;

# ---------------------------------------- #
# ------------- INVERSIONES -------------- #
# ---------------------------------------- #

def tablaResumenInversiones( pResumen , pListaResumen ):
    
    informacion = "<table id='equipos'>"
    informacion += "<tr>"
    informacion += "    <th>              </th>"
    informacion += "	<th> APORTACIONES </th>"
    informacion += "    <th> VALOR ACTUAL </th>"
    informacion += "	<th> COMISION / DIVIDENDOS </th>"
    informacion += "	<th> BENEFICIO BRUTO </th>"
    informacion += "	<th> BENEFICIO NETO </th>"
    informacion += "	<th> RENTABILIDAD </th>"
    informacion += "</tr>"
    
    for resumen in pListaResumen.listaResumen:
        
        aportaciones = str( "{:.2f}".format( pListaResumen.listaResumen[resumen].aportaciones) );
        valorActual = str( "{:.2f}".format(pListaResumen.listaResumen[resumen].valorActual) );
        comisiones = str( "{:.2f}".format(pListaResumen.listaResumen[resumen].dividendos - pListaResumen.listaResumen[resumen].comisiones) );
        beneficioBruto = str( "{:.2f}".format(pListaResumen.listaResumen[resumen].beneficioBruto) );
        beneficioNeto = str( "{:.2f}".format(pListaResumen.listaResumen[resumen].beneficioNeto) );
        rentabilidad = str( "{:.2f}".format(pListaResumen.listaResumen[resumen].rentabilidad) );
        
        estilo = ""
        informacion += "<tr>"
        informacion += "	<td> <h3 " + estilo + " > </br>" + pListaResumen.listaResumen[resumen].descripcion + " </br> </h3> </td>"
        informacion += "	<td> <h3 " + estilo + " >" + aportaciones + "</h3> </td>"
        informacion += "	<td> <h3 " + estilo + " >" + valorActual + "</h3> </td>"
        informacion += "    <td> <h3 " + estilo + " >" + comisiones + "</h3> </td>"
        informacion += "    <td> <h3 " + estilo + " >" + beneficioBruto + "</h3> </td>"
        informacion += "    <td> <h3 " + estilo + " >" + beneficioNeto + "</h3> </td>"
        informacion += "    <td> <h3 " + estilo + " >" + rentabilidad + "</h3> </td>"
        informacion += "</tr>"
    
    aportaciones = str( "{:.2f}".format(pResumen.aportaciones) );
    valorActual = str( "{:.2f}".format(pResumen.valorActual) );
    comisiones = str( "{:.2f}".format(pResumen.dividendos - pResumen.comisiones) );
    beneficioBruto = str( "{:.2f}".format(pResumen.beneficioBruto) );
    beneficioNeto = str( "{:.2f}".format(pResumen.beneficioNeto) );
    rentabilidad = str( "{:.2f}".format(pResumen.rentabilidad) );
        
    estilo = ""
    informacion += "<tr>"
    informacion += "	<td> <h3 " + estilo + " > </br>" + "RESUMEN GLOBAL" + " </br> </h3> </td>"
    informacion += "	<td> <h3 " + estilo + " >" + aportaciones + "</h3> </td>"
    informacion += "	<td> <h3 " + estilo + " >" + valorActual + "</h3> </td>"
    informacion += "    <td> <h3 " + estilo + " >" + comisiones + "</h3> </td>"
    informacion += "    <td> <h3 " + estilo + " >" + beneficioBruto + "</h3> </td>"
    informacion += "    <td> <h3 " + estilo + " >" + beneficioNeto + "</h3> </td>"
    informacion += "    <td> <h3 " + estilo + " >" + rentabilidad + "</h3> </td>"
    informacion += "</tr>"
    
    informacion += "</table>"
    informacion += "<br />"
    
    return informacion;

# ---------------------------------------- #
# --------------- USUARIOS --------------- #
# ---------------------------------------- #

def tablaUsuariosActivos( ):
    usuarios = sql.getUsuarios()
    informacion = ""
    informacion += "<table id='equipos'>"
    informacion += "	<tr>"
    informacion += "		<th> NOMBRE </th>"
    informacion += "		<th> DNI </th>"
    informacion += "		<th> TELÉFONO </th>"
    informacion += "		<th> E-MAIL </th>"
    informacion += "		<th> CATEGORIA ACTUAL </th>"
    informacion += "		<th> CAMBIAR CATEGORIA </th>"
    informacion += "		<th> ELIMINAR USUARIO </th>"
    informacion += "	</tr>"
    for nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , contra , categoria in usuarios:
        informacion += "    <tr>"
        informacion += "        <td> <h3>" + nombre + " " + apellido1 + " " + apellido2 + " </h3> </td>"
        informacion += "        <td> " + DNI + " </td>"
        informacion += "        <td> " + telefono + " </td>"
        informacion += "        <td> " + email + " </td>"
        informacion += "        <td> " + categoria + " </td>"
        informacion += "        <td> "
        informacion += "                <form name='admitir_frm' action='cambiar_permisos_usuario' method='post' enctype='application/x-www-form-urlencoded'> "	
        informacion += "                    <input type='hidden' name='usuario_hdn' value='" + usuario + "' />"
        informacion += "        			<select id='admision' class='cambio' name='tipo_select' onchange='this.form.submit()'> "
        informacion += "                        <option selected disabled > Selecciona Categoria </option> "
        informacion += "                        <option value='admin'> Admin </option> "
        informacion += "                        <option value='notario'> notario </option> "
        informacion += "                        <option value='usuario'> Usuario </option> "
        informacion += "        			</select>   				 "
        informacion += "               </form> "
        informacion += "        </td> "
        informacion += "        <td> "
        informacion += "               <form name='admitir_frm' action='eliminar_usuario' method='post' enctype='application/x-www-form-urlencoded'> "	
        informacion += "                    <input type='hidden' name='usuario_hdn' value='" + usuario + "' />"
        informacion += "                    <input type='submit' id='eliminar' class='editar' name='eliminar_btn' value='Eliminar '/>	 "			
        informacion += "               </form> "
        informacion += "        </td> "
        informacion += "        </tr> "
    
    informacion += "</table>"
    informacion += "<br />"
    return informacion;
    
def tablasolicitudesPendientes( ):
    usuarios = sql.getAdmisiones()
    informacion = ""
    informacion += "<table id='equipos'>"
    informacion += "	<tr>"
    informacion += "		<th> NOMBRE </th>"
    informacion += "		<th> DNI </th>"
    informacion += "		<th> TELÉFONO </th>"
    informacion += "		<th> E-MAIL </th>"
    informacion += "		<th> ACEPTAR USUARIO </th>"
    informacion += "		<th> RECHAZAR USUARIO </th>"
    informacion += "	</tr>"
    for nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , contra in usuarios:
        informacion += "    <tr>"
        informacion += "        <td> <h3> " + nombre + " " + apellido1 + " " + apellido2 + " </h3> </td>"
        informacion += "        <td> " + DNI + " </td>"
        informacion += "        <td> " + telefono + " </td>"
        informacion += "        <td> " + email + " </td>"
        informacion += "        <td> "
        informacion += "                <form name='admitir_frm' action='anadir_usuario' method='post' enctype='application/x-www-form-urlencoded'> "	
        informacion += "                    <input type='hidden' name='usuario_hdn' value='" + usuario + "' />"
        informacion += "        			<select id='admision' class='cambio' name='tipo_select'> "
        informacion += "                        <option value='admin'> Admin </option> "
        informacion += "                        <option value='notario'> Notario </option> "
        informacion += "                        <option value='usuario'> Usuario </option> "
        informacion += "        			</select>   				 "
        informacion += "                    &nbsp &nbsp &nbsp &nbsp    			 "	
        informacion += "                    <input type='submit' id='aceptar' class='editar' name='editar_btn' value='Confirmar '/>	"
        informacion += "               </form> "
        informacion += "        </td> "
        informacion += "        <td> "
        informacion += "               <form name='admitir_frm' action='eliminar_registro' method='post' enctype='application/x-www-form-urlencoded'> "	
        informacion += "                    <input type='hidden' name='usuario_hdn' value='" + usuario + "' />"
        informacion += "                    <input type='submit' id='eliminar' class='editar' name='editar_btn' value='Rechazar '/>	 "			
        informacion += "               </form> "
        informacion += "        </td> "
        informacion += "    </tr> "
            
    informacion += "</table>"
    informacion += "<br />"
    return informacion;

####################################################################    
#---------------------------- GRAFICAS ----------------------------#
####################################################################

# ---------------------------------------- #
# --------------- GENERICO --------------- #
# ---------------------------------------- #
        
def graficoTarta( pTitulo , pCabeceras , pDatos , cBackground , cBorder ):
    
    informacion = ""
    
    informacion += "<canvas id='" + pTitulo  + "' width='400' height='400'></canvas>"
    informacion += "<script>"
    informacion += "var ctx = document.getElementById('" + pTitulo  + "').getContext('2d');"
 
    informacion += "var mychart = new Chart( ctx ,                                            "
    informacion += "{                                                                         "
    informacion += "type: 'pie',                                                    "
    informacion += "data:                                                                     "
    informacion += "{                                                                         "
    informacion += "   labels: " + pCabeceras + ",                                            "
    informacion += "   datasets:                                                              "
    informacion += "   [{                                                                     "
    informacion += "        label: '# of Votes',                                              "
    informacion += "        data: " + pDatos + ",                                             "
    informacion += "        backgroundColor: " + cBackground + ",                             "                                                               
    informacion += "        borderColor:  " + cBorder + ",                                    "
    informacion += "        borderWidth: 1                                                    "
    informacion += "   }]                                                                     "
    informacion += "},                                                                        "
    informacion += "options: { scales: {  yAxes: [{  ticks: {  beginAtZero: true }  }]   }   }"
    informacion += "});"
    informacion += "</script>"
    return informacion;


def graficoBarras( pTitulo , pCabeceras , pDatos , cBackground ):
    informacion = ""
    
    informacion += "<canvas id='" + pTitulo  + "' width='400' height='400'></canvas>"
    informacion += "<script>"
    informacion += "var ctx = document.getElementById('" + pTitulo  + "').getContext('2d');"
 
    informacion += "var mychart = new Chart( ctx ,                                            "
    informacion += "{                                                                         "
    informacion += "type: 'bar',                                                    "
    informacion += "data:                                                                     "
    informacion += "{                                                                         "
    informacion += "   labels: " + pCabeceras + ",                                            "
    informacion += "   datasets:                                                              "
    informacion += "   [{                                                                     "
    informacion += "        label: '" + pTitulo + "',                                              "
    informacion += "        data: " + pDatos + ",                                             "
    informacion += "        backgroundColor: " + cBackground + ",                             "                                                               
    informacion += "        borderColor:  " + cBackground + ",                                    "
    informacion += "        borderWidth: 1                                                    "
    informacion += "   }]                                                                     "
    informacion += "},                                                                        "
    informacion += "options: { scales: {  yAxes: [{  ticks: {  beginAtZero: true }  }]   }   }"
    informacion += "});"
    informacion += "</script>"    
    return informacion;
    
                                                                   
def graficoBarrasAgrupado( pTitulo , pCabeceras , pCuerpo ):
    informacion = ""
    
    informacion += "<canvas id='" + pTitulo  + "' width='400' height='400'></canvas>"
    informacion += "<script>"
    informacion += "var ctx = document.getElementById('" + pTitulo  + "').getContext('2d');"
 
    informacion += "var mychart = new Chart( ctx ,                                            "
    informacion += "{                                                                         "
    informacion += "type: 'horizontalBar',                                                    "
    informacion += "data:                                                                     "
    informacion += "{                                                                         "
    informacion += "   labels: " + pCabeceras + ",                                            "
    informacion += "   datasets:                                                              "
    informacion += "   [                                                                      "
    
    for cuerpo in pCuerpo:
        label = cuerpo[0];          cBackground = cuerpo[1];              data = cuerpo[2];
        cBackground = "'" + cBackground + "'"
        informacion += "   {                                                                      "
        informacion += "        label: '" + label + "',                                           "
        informacion += "        backgroundColor: " + cBackground + ",                             "
        informacion += "        data: " + data + ",                                               "                                                                     
        informacion += "   },"
    
    temp = len(informacion);
    informacion = informacion[:temp - 1]
    
    informacion += "   ]                                                                      "
    informacion += "},                                                                        "
    #informacion += "options: { scales: {  yAxes: [{  ticks: {  beginAtZero: true }  }]   }   }"
    informacion += "});"
    informacion += "</script>"
    return informacion;

# ---------------------------------------- #
# --------------- FINANZAS --------------- #
# ---------------------------------------- # 

def graficoSectoresFinanzas( pTitulo , pListaFinanzas ):
    
    informacion = ""    
    etiqueta = "gasto" # gasto ingreso
    
    informacion += subTitulo_2( "Reparto de " + etiqueta + "s" )
    cabeceras = str( pListaFinanzas.getCabeceras() )
    datos = str( pListaFinanzas.getAtributo( etiqueta ) )
    color = str( pListaFinanzas.getAtributo( "color" ) )    
    informacion += graficoTarta( pTitulo + "_reparto" , cabeceras , datos , color , color )
    
    informacion += "<br />"
    informacion += subTitulo_2( "Representacion del Ahorro " )
    cabeceras = str ( [ "Gastado" , "Ahorrado" , "Invertido" ] )
    datos = str ( [ pListaFinanzas.totalGastos , pListaFinanzas.ahorrado , pListaFinanzas.invertido ] )
    color = str ( [ "rgba( 22 , 22 , 23 , 1 )" , "rgba( 3 , 173 , 9 , 1 )" , "rgba( 0 , 170 , 204 , 1 )" ] )
    informacion += graficoTarta( pTitulo + "_representacion" , cabeceras , datos , color , color )
    return informacion;
    
    
def graficoBarrasAgrupadoCategoriasFinanzas( pTitulo , pClases , pResumenes , pTipo ):
    informacion = ""
    cabeceras = []
    cuerpo = []
       
    for clase in pClases:
        color = pClases[ clase ]
        data = []
        
        for resumen in pResumenes:
            clases = pResumenes[ resumen ].clases
            if clase in clases:
               if pTipo == "Ingresos":
                  data.append( clases[ clase ].ingreso )
               else:
                data.append( clases[ clase ].gasto )
            else: 
               data.append( 0 )
        
        cuerpo.append( [ clase , color , str ( data ) ] )
    
    for resumen in pResumenes:
        cabeceras.append( resumen )
    
    informacion += graficoBarrasAgrupado( pTitulo , str ( cabeceras ) , cuerpo )    
    return informacion

def graficoBarrasAgrupadoAnosFinanzas( pTitulo , pClases , pResumenes , pTipo ):
    informacion = ""
    cabeceras = []
    cuerpo = []
    r = 0;     g = 0;    b = 250;
    for resumen in pResumenes:
        data = []
        
        r , g , b = utilidades.getDegradado( r , g , b )
        color = "rgba( " + str( r ) + ", " + str( g ) + ", " + str( b ) + ", 1 )"
        
        for clase in pClases: 
            clases = pResumenes[ resumen ].clases
            if clase in clases:               
               if pTipo == "Ingresos":
                  data.append( clases[ clase ].ingreso )
               else:
                   data.append( clases[ clase ].gasto )
            else: data.append( 0 )
        cuerpo.append( [ resumen , color , str ( data ) ] ) 
  
    for clase in pClases:
        cabeceras.append( clase )
    
    informacion += graficoBarrasAgrupado( pTitulo , str ( cabeceras ) , cuerpo )
    
    return informacion

# ---------------------------------------- #
# ------------- INVERSIONES -------------- #
# ---------------------------------------- #

def graficoSectoresInversiones( pTitulo , pListaInversiones ):   
    informacion = ""    
    cabeceras = str( pListaInversiones.getCabeceras() )
    datos = str( pListaInversiones.getAtributo( "valorActual" ) )
    color = str( pListaInversiones.getAtributo( "color" ) )
    
    informacion += graficoTarta( pTitulo , cabeceras , datos , color , color )
    return informacion;


def graficoRentabilidadesInversiones( pTitulo , pListaInversiones ):      
    informacion = ""    
    cabeceras = str( pListaInversiones.getCabeceras() )
    datos = str( pListaInversiones.getAtributo( "beneficioNeto" ) ) 
    color = str( pListaInversiones.getAtributo( "color" ) )

    informacion += graficoBarras( pTitulo , cabeceras , datos , color )
    return informacion;
    
    
    
    
    
    
    
    
    