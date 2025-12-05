# -*- coding: utf-8 -*-

import json
import datetime
import calendar
import random
import seaborn
import binascii
import hashlib

####################################################################    
#----------------------------- COLORES ----------------------------#
####################################################################

def randomColor():
    levels = range(32,256,32);
    return tuple(random.choice(levels) for _ in range(3))

def randomColorString( pOpacidad ):
    r = str(random.randint(0,255));   g = str(random.randint(0,255));   b = str(random.randint(0,255))
    color = "rgba( " + r + ", " + g + ", " + b + ", " + str(pOpacidad) + " )"
    return color
    
def getDegradado( r , g , b , pVelocidad ):  
    if r == 0 and g == 0 and b == 0: r = 0;  g = 250;   b = 0;
    if pVelocidad >= 250: pVelocidad = 250
    if pVelocidad <= 0: pVelocidad = 50

    #          (  R  ,   G   ,   B   )       (  R  ,   G   ,   B   )
    # Fase 1:  ( 250 ,  5    ,  5    )  To   ( 250 ,  250  ,  5    )  g --> 250
    # Fase 2:  ( 250 ,  250  ,  5    )  To   ( 5   ,  250  ,  5    )  r --> 5
    # Fase 3:  ( 5   ,  250  ,  5    )  To   ( 5   ,  250  ,  250  )  b --> 250
    # Fase 4:  ( 5   ,  250  ,  250  )  To   ( 5   ,  5    ,  250  )  g --> 5
    # Fase 5:  ( 5   ,  5    ,  250  )  To   ( 250 ,  5    ,  250  )  r --> 250
    # Fase 6:  ( 250 ,  5    ,  250  )  To   ( 255 ,  5    ,  5    )  b --> 5  
    
    if   r == 250 and g < 250  and b == 0  : g += pVelocidad
    elif r > 0    and g == 250 and b == 0  : r -= pVelocidad
    elif r == 0   and g == 250 and b < 250 : b += pVelocidad
    elif r == 0   and g > 0    and b == 250: g -= pVelocidad
    elif r < 250  and g == 0   and b == 250: r += pVelocidad
    elif r == 250 and g == 0   and b > 0   : b -= pVelocidad
    
    if r > 250: r = 250
    if g > 250: g = 250
    if b > 250: b = 250
    
    if r < 0: r = 0
    if g < 0: g = 0
    if b < 0: b = 0
 
    return r , g , b
    
def colorHexadecimalToRGB( pColor ):
    color = pColor.lstrip('#')
    color = tuple( int( color[i:i+2] , 16 ) for i in ( 0 , 2 , 4 ) )
    color = "rgba( " + str(color[0]) + " , " + str(color[1]) + " , " + str(color[2]) + " , 1 )"
    return color

def colorRGBToHexadecimal( pColor ):
    color = pColor.lstrip( 'rgba(' ).replace( " " , "" );
    r , g , b , o = color.split(',')
    r = intToHex(r);
    g = intToHex(g);
    b = intToHex(b);
    color = "#" + r + g + b;
    return color

####################################################################    
#------------------------------ Fechas ----------------------------#
####################################################################

def comprobarFechaCorrecta( pDia , pMes , pAno ):
    dia = int(pDia);    mes = int(pMes);      ano = int(pAno);
    correcto = True    
    dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    #si el dia mes y año no son numeros enteros no vale la pena comprobar nada
    if str.isdigit( pDia ) and str.isdigit( pMes ) and str.isdigit( pAno ):   
        #si el año es bisiesto
        if((ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0): dias_mes[1] = 29    
        #Comprobar que el ano sea válido
        if( ano > 9999): correcto = False    
        #Comprobar que el mes sea válido
        elif( mes < 1 or mes > 12 ): correcto = False    
        #Comprobar que el dia sea válido
        elif(dia < 0 or dia > dias_mes[mes-1]): correcto = False
    else: correcto = False
    return correcto


def parseMesToInt( pMes ):
    if pMes == "Enero" or pMes == "enero": mes = 1
    elif pMes == "Febrero" or pMes == "febrero": mes = 2
    elif pMes == "Marzo" or pMes == "marzo": mes = 3
    elif pMes == "Abril" or pMes == "abril": mes = 4
    elif pMes == "Mayo" or pMes == "mayo": mes = 5
    elif pMes == "Junio" or pMes == "junio": mes = 6
    elif pMes == "Julio" or pMes == "julio": mes = 7
    elif pMes == "Agosto" or pMes == "agosto": mes = 8
    elif pMes == "Septiembre" or pMes == "septiembre": mes = 9
    elif pMes == "Octubre" or pMes == "octubre": mes = 10
    elif pMes == "Noviembre" or pMes == "noviembre": mes = 11
    elif pMes == "Diciembre" or pMes == "diciembre": mes = 12
    else: mes = 0; print( "ERROR se ha introducido un mes que no existe: " , pMes )
    return mes;

def getYear( date ):
    ano = ""
    if date != "":
        ano , mes , dia = date.split("-")
    return ano

def nextMonth( pFecha ):
    month = pFecha.month - 1 + 1
    year = pFecha.year + month // 12
    month = month % 12 + 1
    day = min( pFecha.day , calendar.monthrange( year , month )[1])
    return datetime.date( year , month , day )

def daysBetween( pFechaInicio , pFechaFin ):
    if pFechaInicio == '': pFechaInicio = datetime.datetime(2019,9,25).date()
    if pFechaFin == '': pFechaFin = datetime.datetime.now().date()
    delta = pFechaFin - pFechaInicio
    return delta.days

def ajustarSoloFecha( pFecha ):
    try: fecha = pFecha.date()
    except: fecha = pFecha
    if isinstance( pFecha , str):
        if pFecha == '' or pFecha == ' ': fecha = datetime.datetime.now().date()
        else: 
            ano , mes , dia = fecha.split('-')
            fecha = datetime.date( int(ano) , int(mes) , int(dia) )
    return fecha

####################################################################    
#-------------------------- CAMBIO DE BASE ------------------------#
####################################################################

def intToHex( pInt ):
    resultado = int(pInt)
    if resultado == 0:
       resultado = "00"
    else: 
        if resultado > 255 or resultado < 0: resultado = 255
        resultado = hex( resultado ).lstrip('0x')
        if len(resultado) != 2: resultado = "0" + resultado
    return resultado


####################################################################    
#------------------------------ PARSER ----------------------------#
####################################################################

def depurarTodo( pString ):
    string = pString
    string = depurarEspacios( string )
    string = depurarSimbolos( string )
    return string 
    
def depurarEspacios( pString ):
    string = pString
    string = string.replace( " " , "" )
    return string    

def depurarSimbolos( pString ):
    string = pString
    string = string.replace( "/" , "" )
    string = string.replace( "*" , "" )
    string = string.replace( "+" , "" )
    string = string.replace( "-" , "" )
    string = string.replace( "=" , "" )
    string = string.replace( "^" , "" )
    string = string.replace( "_" , "" )
    string = string.replace( "|" , "" )
    string = string.replace( "?" , "" )
    string = string.replace( "¿" , "" )
    string = string.replace( "!" , "" )
    string = string.replace( "¡" , "" )
    string = string.replace( ";" , "" )
    string = string.replace( "," , "" )
    string = string.replace( "(" , "" )
    string = string.replace( ")" , "" )
    string = string.replace( "[" , "" )
    string = string.replace( "]" , "" )
    string = string.replace( "€" , "" )
    string = string.replace( "$" , "" )
    string = string.replace( "%" , "" )
    string = string.replace( "&" , "" )
    string = string.replace( "#" , "" )
    return string


def concatenarStringVector( pVector ):
    string = ""
    for element in pVector:
        string += element.replace( "." , "" ) + "."
    return string[:-1]


def isFloat( pString ):
    try:
        float( pString )
        return True
    except ValueError:
        return False


def isLista( pString ):
    try:
        pString.append( ( 'Fondo' , 'Fondo' , False ) )
        return True
    except AttributeError:
        return False
    

def floatStr( pString ):
    string = str( pString )
    return string.replace( "," , "." )
   

def permisosToString( pPerimisos ):
    if pPerimisos == 0: permisos = "No Identificado"
    if pPerimisos == 1: permisos = "Usuario"
    if pPerimisos == 2: permisos = "Administrador"
    if pPerimisos == 3: permisos = "Creador"
    return permisos
    
def sqlCondicion( pAtributo , pEstricto , pValor ):
    sql = pAtributo + " " + pEstricto + " '" + pValor + "'"
    if pValor == '' or pValor == ' ': sql = '1'
    return sql
    
def sqlOrderBy( pOrden ):
    orden = " ORDER BY " + pOrden
    if pOrden == '' or pOrden == ' ': orden = ''
    return orden

def ajustarSerieCotizaciones_YahooFinance( pSerie , pColumna ):
    serie = json.loads( pSerie )
    resultado = []
    for dato in serie:
        fecha , hora = dato['Date'].split('T')
        ano , mes , dia = fecha.split('-')
        fecha = datetime.date( int(ano) , int(mes) , int(dia) )
        precio = dato[pColumna]
        resultado.append( ( fecha , precio ) )
    return resultado

####################################################################    
#------------------------------ HASH ------------------------------#
####################################################################

def getHash( pCadena ):
    return hashlib.sha256( pCadena.encode("utf-8") ).hexdigest()
    
def generarSal( ):
    fecha = datetime.datetime.now().date() 
    hora = datetime.datetime.now().time()
    return getHash( str(fecha) + str(hora) )

####################################################################    
#------------------------------ LISTAS ----------------------------#
####################################################################

def diferenciaListas( pCompleta , pEliminar ):
    lista = []
    for elemento in pCompleta:
        if elemento not in pEliminar:
            lista.append( elemento )
    return lista



