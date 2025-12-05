# -*- coding: utf-8 -*-
from lib import Utils as utils

MARGEN = 0.01
    
####################################################################    
#----------------------------- TITULOS ----------------------------#
####################################################################

def seccion( pID , pClass ):
    informacion = "<br />"
    informacion += "<section id='" + pID + "' class='" + pClass + "' >"
    return informacion

def articulo( pID , pClass ):
    informacion = "<article id='" + pID + "' class='" + pClass + "'>"
    return informacion

def titulo( pID , pClass , pNivel , pTitulo ):
    informacion = ""
    informacion += " <hgroup id='" + pID + "' class='" + pClass + "'>"
    informacion += "      <h"+ str(pNivel) +" id='" + pID + "' class='" + pClass + "'> " + pTitulo + " </h"+ str(pNivel) +" >"	
    informacion += " </hgroup>"	
    return informacion

def tituloTabla( pTitulo ):
    informacion = ""
    informacion += "<table class='titulo'>"
    informacion += "   <tr class='titulo'>"
    informacion += "       <th class='titulo'> " + pTitulo + " </th>"
    informacion += "   </tr>"
    informacion += "</table>"
    return informacion
    
####################################################################    
#---------------------------- MENSAJES ----------------------------#
####################################################################

def mensaje( pMensaje ):
    informacion = ""
    if pMensaje != "":
       informacion += seccion( 'error' , 'error' )
       informacion += "<br /> <span class='mensajes'> " + pMensaje + " </span> <br /> <br />"
       informacion += "</section>"
    return informacion


def working( ):
    informacion = ""
    informacion += "</br> </br>"
    informacion += "<p id='Working' class='Contenido'>"
    informacion += "	<img class='Contenido' alt='FinanasPersonales.com' src='static/img/Working_1.png' width='100%' height='100%' /> "
    informacion += "</p>"	
    informacion += "</br> </br>"
    return informacion	


def parrafo( pID , pClass , pMensaje ):
    informacion = ""
    if pMensaje != "":
       informacion += seccion( pID , pClass )
       informacion += "<br /> <p class='" + pClass + "'> " + pMensaje + " </p> <br /> <br />"
       informacion += "</section>" 
    return informacion

def representarNumero( pNumero , tieneColor ):
    color = "Normal"
    if utils.isFloat( str(pNumero) ): 
        if pNumero < MARGEN and pNumero > -MARGEN: numero = '--'
        else:
            numero = float( round ( pNumero , 2 ) )
            if tieneColor: numero = abs ( numero )
            numero = "{:,}".format( numero )
            numero = numero.replace(',','~')
            numero = numero.replace('.',',')
            numero = numero.replace('~','.')
        if pNumero > 0 + MARGEN and tieneColor: color = "Positivo"
        if pNumero < 0 - MARGEN and tieneColor: color = "Negativo"
        numero = "<p class = '" + color + "' > " + numero + " </p>"
    else: numero = str( pNumero )
    return numero

####################################################################    
#----------------------------- ENLACES ----------------------------#
####################################################################

def refrescar( pID , pClass , pTipo , pFuncion , pParametros , pTitulo ):
    informacion = ""
    informacion += formHeader( pID , pClass , '/' + pFuncion , False )
    informacion += formHidden( 'Parametros' , pClass , pParametros )
    informacion += formSubmit( pTipo , pClass , pTitulo )
    informacion += "</form>"
    return informacion
    
####################################################################    
#------------------------------ INDICE ----------------------------#
####################################################################

def indice( pID , pClass , pLista ):
    informacion = ""
    informacion += seccion( pID , pClass )
    informacion += "<nav id='" + pID + "' class='" + pClass + "' >"
    informacion += "     <ul>"

    for enlace , etiqueta in pLista:
        informacion += "<li>"
        informacion += formHeader( pID , pClass , 'Redirigir' , False )
        informacion += formHidden( 'Redirigir' , 'Redirigir' , enlace )
        informacion += formSubmit( etiqueta , pClass , etiqueta )
        informacion += "</form>"
        informacion += "</li>"

    informacion += "     </ul>"
    informacion += "</nav>"
    informacion += "</section>"
    return informacion

####################################################################    
#--------------------------- FORMULARIOS --------------------------#
####################################################################

def formHeader( pID , pClass , pAccion , pEncriptadoFichero ):
    informacion = ""
    encriptadoFichero = ""
    if( pEncriptadoFichero ): encriptadoFichero = "enctype='multipart/form-data'"
    informacion += "<form id='" + pID + "' class='" + pClass + "' name='" + pID + "' action='" + pAccion + "' method='post' " + encriptadoFichero + ">"
    return informacion

def formInput( pID , pClass , pLabel , pTipo , pPlaceHolder , pTitulo , pInformacion , pSubmitOnChange ):
    pattern = '' ; tipo = pTipo ;
    if pTipo == 'DNI' or pTipo == 'dni':
        tipo = 'text'
        pattern = '[0-9]{8}[A-Za-z]{1}'
    informacion = ""
    if pLabel != '': informacion += "    <label for='" + pID + "'> " + pLabel + ": </label>"
    informacion += "    <input type='" + tipo + "' " + pattern + " id='" + pID + "' class='" + pClass + "' name='" + pID + "' placeholder='" + pPlaceHolder + "' title='" + pTitulo + "' value='" + pInformacion + "' />"
    return informacion    

def formCheckBox( pID , pClass , pLabel , pValor ):
    informacion = "" 
    if pLabel != '': informacion += " <label for='" + pID + "'> " + pLabel + " </label>"
    informacion += "<input type='checkbox' id='" + pID + "' class='" + pClass + "' name='" + pID + "' value='" + pValor + "' />"
    return informacion

def formOptionList( pID , pClass , pLabel , pOptions , pSubmitOnChange ):
    informacion = "" ;  submitOnChange = "";
    if pSubmitOnChange: submitOnChange = "onchange='this.form.submit()'"
    if pLabel != '': informacion += "    <label for='" + pID + "'> " + pLabel + ": </label>" 
    informacion += "<select id='" + pID + "' name='" + pID + "' " + submitOnChange + "> "
    for opcion , titulo , seleccion in pOptions:
        if seleccion: selected = 'selected'
        else: selected = ''
        informacion += "<option " + selected + " value='" + opcion + "'> " + titulo + " </option>"
    informacion += "</select>"
    return informacion

def formFichero( pID , pClass , pTipo ):
    informacion = "" 
    informacion += "<input type='file' id='" + pID + "' class='" + pClass + "' name='" + pID + "' accept='" + pTipo + "' />"
    return informacion

def formHidden( pID , pClass , pInformacion ):
     informacion = ""
     informacion += "    <input type='hidden' id='" + pID + "' class='" + pClass + "' name='" + pID + "' value='" + pInformacion + "' />"
     return informacion

def formSubmit( pID , pClass , pTitulo ):
    informacion = ""
    informacion += "<input type='submit' id='" + pID + "' class='" + pClass + "' name='" + pID + "_btn' value='" + pTitulo + "'/>"
    return informacion
        
####################################################################    
#------------------------------ TABLAS ----------------------------#
####################################################################
       

    
####################################################################    
#----------------------------- GRAFICOS ---------------------------#
####################################################################

WIDTH = 100
HEIGHT = 100

BORDERWIDGHT = 5
MAXLENGHT = 30
MINLENGHT = 100

def opcionesGraficos( pStacked ):
    informacion = ""
    informacion += "options:                                                                  "
    informacion += "{                                                                         "
    
    informacion += "    scales:                                                               "
    informacion += "    {                                                                     "

    informacion += "        xAxes: [{                                                         "
    informacion += "                display: false,                                           "
    if pStacked: informacion += "   stacked: true,                                            "
    informacion += "                categoryPercentage: 1.0,                                  "
    informacion += "                barPercentage: 0.85                                       "
    informacion += "            }],                                                            " 
    
    informacion += "        yAxes: [{                                                         "
    informacion += "                display: true,                                            "
    if pStacked: informacion += "   stacked: true,                                            "
    informacion += "                gridLines: { display: false },                            "
    informacion += "                ticks:                                                    "
    informacion += "                {                                                         "
    informacion += "                    min: 0.1,                                             "
    informacion += "                    suggestedMin: 0,                                      "
    #informacion += "                    mirror: true,                                         "
    informacion += "                    fontColor: '#b9ffff',                                 "
    informacion += "                    fontStyle: 'normal',                                  "
    informacion += "                    fontSize: 13                                          "
    informacion += "                },                                                        "
    informacion += "                categoryPercentage: 1.0,                                  "
    informacion += "                barPercentage: 0.85                                       "
    informacion += "            }]                                                            "
    informacion += "    },                                                                    "

    informacion += "    legend:                                                               "
    informacion += "    {                                                                     "
    informacion += "        labels: {  fontColor: '#b9ffff'    }                              "
    informacion += "    }                                                                     "
    informacion += "}                                                                         "
    return informacion



# pTipo = 'pie'  'donut' 
def graficoSimple( pID , pCabeceras , pDatos , cBackground , cBorder , pTipo , pStacked ):  
    informacion = ""
    informacion += "<canvas id='" + pID  + "' max-width='" + str( WIDTH ) + "' max-height='" + str( HEIGHT ) + "'></canvas>"
    informacion += "<script>"
    informacion += "var ctx = document.getElementById('" + pID  + "').getContext('2d');"
 
    informacion += "var mychart = new Chart( ctx ,                                            "
    informacion += "{                                                                         "
    informacion += "type: '" + pTipo + "',                                                    "
    informacion += "data:                                                                     "
    informacion += "{                                                                         "
    informacion += "   labels: " + str( pCabeceras ) + ",                                     "
    informacion += "   datasets:                                                              "
    informacion += "   [{                                                                     "
    informacion += "        borderWidth: " + str( BORDERWIDGHT ) + ",                         "
    informacion += "        minBarLength: " + str( MINLENGHT ) + ",                           "
    informacion += "        maxBarLength: " + str( MAXLENGHT ) + ",                           "
    informacion += "        label: " + pID + ",                                               "
    informacion += "        data: " + str( pDatos ) + ",                                      "
    informacion += "        backgroundColor: " + str( cBackground ) + ",                      "                                                               
    informacion += "        borderColor:  " + str( cBorder ) + ",                             "
    informacion += "        borderWidth: 1                                                    "
    informacion += "   }]                                                                    "
    informacion += "},                                                                        "
    #informacion += "options: { scales: {  yAxes: [{  ticks: {  beginAtZero: true }  }]   }   }"
    informacion += opcionesGraficos( pStacked )
    informacion += "});"
    informacion += "</script>"
    return informacion

# pTipo 'bar'  'horizontalBar'                                              
def graficoBarrasAgrupado( pID , pCabeceras , pCuerpo , pHorizontal , pStacked ):
    informacion = ""
    informacion += "<canvas id='" + pID  + "' max-width='" + str( WIDTH ) + "' max-height='" + str( HEIGHT ) + "'></canvas>"
    informacion += "<script>"
    informacion += "var ctx = document.getElementById('" + pID  + "').getContext('2d');"
 
    informacion += "var mychart = new Chart( ctx ,                                            "
    informacion += "{                                                                         "
    if pHorizontal: informacion += "type: 'horizontalBar',                                    "
    else: informacion += "type: 'bar',                                                        "
    informacion += "data:                                                                     "
    informacion += "{                                                                         "
    informacion += "   labels: " + str( pCabeceras ) + ",                                     "
    informacion += "   datasets:                                                              "
    informacion += "   [                                                                      "
    
    for label , cBackground , data in pCuerpo:
        cBackground = "'" + cBackground + "'"
        informacion += "   {                                                                  "
        #informacion += "        grouped: true,                                                "     
        informacion += "        label: '" + label + "',                                       "
        informacion += "        borderWidth: " + str( BORDERWIDGHT ) + ",                     "
        informacion += "        minBarLength: " + str( MINLENGHT ) + ",                       "
        informacion += "        maxBarLength: " + str( MAXLENGHT ) + ",                       "
        informacion += "        backgroundColor: " + cBackground + ",                         "
        informacion += "        data: " + str( data ) + ",                                    "                                                                     
        informacion += "   },"
    
    informacion = informacion[:len(informacion) - 1]
    informacion += "   ]                                                                      "
    informacion += "},                                                                        "
    #informacion += "options: { scales: {  yAxes: [{  ticks: {  beginAtZero: true }  }]   }   }"
    informacion += opcionesGraficos( pStacked )
    informacion += "});"
    informacion += "</script>"
    return informacion
        
        