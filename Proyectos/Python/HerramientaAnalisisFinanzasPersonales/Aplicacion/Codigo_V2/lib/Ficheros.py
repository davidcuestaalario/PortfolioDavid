# -*- coding: utf-8 -*-
import csv
import pathlib
import os
import datetime

from app import Sesion as sesion
from app import Seccion as secciones

from lib import Utils as utils 

####################################################################    
#--------------------------- READ CSV -----------------------------#
####################################################################

# RUTA = "C:/Users/David/Dropbox (Personal)/Finanzas/Scraper/Aplicacion/Codigo_V2/tmp"
RUTA = "C:/Users/David/OneDrive/zzz - tmp/ZZZ - Resumen Inversion/Scraper/Aplicacion/Codigo_V2/tmp"

#MENSAJE = "Seleccione un fichero csv con el mismo formato y estructura que las plantillas. <br />"
#MENSAJE += "Si no tiene las plantillas, descárguelas desde el apartado importaciones -> Descargas  <br /> "

EXITO = "La importación fue un éxito"
ERROR_INSERCION = "Algunas filas no han podido ser insertadas. A continuación se detallan las posibles causas: <br /> <br />"
NOTIFICACION_DESCARGA = "(Se descargara un fichero con las filas erróneas para facilitar su corrección) <br /> <br />"

IMPORTACION_FALLIDA = "La importación ha fallado porque: <br />  *  añadió columnas nuevas, elimino las que ya existían o cambio su orden <br />  *  Elimino o modifico la fila de la cabecera <br /> <br />"
            
# ---------------------------------------- #
# --------------- Gestion ---------------- #
# ---------------------------------------- #

def guardarFichero( pNombre , pFichero ):    
    pFichero.save( os.path.join( RUTA , pNombre ) )

def eliminarFichero( pRuta ): 
    if os.path.exists( pRuta ): os.remove( pRuta )
    
def crearFichero( pNombre , pLinea ):
    file = open( RUTA + "/" + pNombre + ".csv" , "w" , newline="" )
    with file:
        writer = csv.writer( file )
        writer.writerows( pLinea )

# ---------------------------------------- #
# -------------- Importacion ------------- #
# ---------------------------------------- #

def importarDatosCSV( pFichero , pNombre , pSustituir ):    
    if comprobarFichero( pNombre ):
        sal = utils.generarSal( )
        nombre = sal + "_" + pNombre
        ruta = RUTA + "/" + nombre
        guardarFichero( nombre , pFichero )
        if pNombre == "Aportaciones.csv": importarAportacionesCSV( ruta )
        if pNombre == "Comisiones.csv": importarComisionesCSV( ruta )              
        if pNombre == "Gastos.csv": importarTransaccionesCSV( ruta )
        if pNombre == "Transpasos.csv": importarTraspasosCSV( ruta ) 
        eliminarFichero( ruta )


def importarAportacionesCSV( pRuta ):
    ningunError = True
    conexion = csv.reader( open( pRuta ) ) 
    next(conexion)
    secciones.Secciones().reportarError( ERROR_INSERCION )
    for linea in conexion:
        linea = utils.concatenarStringVector( linea )
        if linea.count(";") == 9:
            dia , mes , ano , cuenta , isin , tipo , precio , titulos , cambio , descripcion = linea.split( ";" )
            descripcion = utils.depurarSimbolos( descripcion )
            cuenta = utils.depurarTodo( cuenta )
            isin = utils.depurarTodo( isin )
            tipo = utils.depurarTodo( tipo )
            if tipo == "compra": tipo = "Compra"
            if tipo == "venta": tipo = "Venta"
            if precio == "": precio = 0 
            if titulos == "": titulos = 0 
            if cambio == "": cambio = 1             
            if ( comprobarAportacion( dia , mes , ano , cuenta , isin , tipo , precio , titulos , cambio ) ):
                fecha = datetime.date( int(ano) , int(mes) , int(dia) )
                precio = float(precio)
                titulos = float(titulos)
                cambio = float(cambio)
                sesion.Sesion().anadirAportacion( fecha , cuenta , isin , tipo , precio , titulos , cambio , 'No' , descripcion )
            else: ningunError = False
        else: secciones.Secciones().reportarError( IMPORTACION_FALLIDA )            
    if ningunError: secciones.Secciones().reportarError( EXITO )
        

def importarComisionesCSV( pRuta ):
    ningunError = True
    conexion = csv.reader( open( pRuta ) )
    next(conexion)
    secciones.Secciones().reportarError( ERROR_INSERCION )
    for linea in conexion:
        linea = utils.concatenarStringVector( linea )
        if linea.count(";") == 8:
            dia , mes , ano , cuenta , tipo , isin , gasto , ingreso , descripcion = linea.split( ";" )               
            descripcion = utils.depurarSimbolos( descripcion )
            cuenta = utils.depurarTodo( cuenta )
            isin = utils.depurarTodo( isin )
            if isin == '': isin = "*"
            tipo = utils.depurarTodo( tipo )
            if tipo == "interes": tipo = "Interes"
            if tipo == "comision" or tipo == "comisón" or tipo == "Comision": tipo = "Comisión"
            if tipo == "compensacion" or tipo == "compensación" or tipo == "Compensacion": tipo = "Compensación"
            if tipo == "impuesto": tipo = "Impuesto"
            if tipo == "dividendo": tipo = "Dividendo"
            if gasto == "": gasto = 0
            if ingreso == "": ingreso = 0              
            if ( comprobarComision( dia , mes , ano , cuenta , tipo , isin , gasto , ingreso ) ):
                fecha = datetime.date( int(ano) , int(mes) , int(dia) )
                gasto = float(gasto)
                ingreso = float(ingreso) 
                sesion.Sesion().anadirComision( fecha , cuenta , tipo , isin , gasto , ingreso , 'No' , descripcion )
            else: ningunError = False
        else: secciones.Secciones().reportarError( IMPORTACION_FALLIDA )            
    if ningunError: secciones.Secciones().reportarError( EXITO )
        
        
def importarTransaccionesCSV( pRuta ):
    ningunError = True
    conexion = csv.reader( open( pRuta ) )
    next(conexion)    
    secciones.Secciones().reportarError( ERROR_INSERCION )
    for linea in conexion:
        linea = utils.concatenarStringVector( linea )
        if linea.count(";") == 8:
            dia , mes , ano , cuenta , clasificacion , subClasificacion , gasto , ingreso , descripcion = linea.split( ";" )               
            descripcion = utils.depurarSimbolos( descripcion )
            cuenta = utils.depurarTodo( cuenta )
            clasificacion = utils.depurarTodo( clasificacion )
            subClasificacion = utils.depurarTodo( subClasificacion )
            if gasto == "": gasto = 0
            if ingreso == "": ingreso = 0               
            if ( comprobarTransaccion( dia , mes , ano , cuenta , clasificacion , subClasificacion , gasto , ingreso ) ):
                fecha = datetime.date( int(ano) , int(mes) , int(dia) )
                gasto = float(gasto)
                ingreso = float(ingreso)
                sesion.Sesion().anadirTransaccion( fecha , cuenta , clasificacion , subClasificacion , gasto , ingreso , 'No' , descripcion )
            else: ningunError = False
        else: secciones.Secciones().reportarError( IMPORTACION_FALLIDA )            
    if ningunError: secciones.Secciones().reportarError( EXITO )
        
        
def importarTraspasosCSV( pRuta ):
    ningunError = True
    conexion = csv.reader( open( pRuta ) ) 
    next(conexion)
    secciones.Secciones().reportarError( ERROR_INSERCION )
    for linea in conexion:
        linea = utils.concatenarStringVector( linea )
        if linea.count(";") == 6:
            dia , mes , ano , origen , destino , precio , descripcion = linea.split( ";" )
            descripcion = utils.depurarSimbolos( descripcion )
            origen = utils.depurarTodo( origen )
            destino = utils.depurarTodo( destino )
            if precio == "": precio = 0;
            if ( comprobarTraspaso( dia , mes , ano , origen , destino , precio ) ):
                fecha = datetime.date( int(ano) , int(mes) , int(dia) )
                precio = float(precio)
                sesion.Sesion().anadirTraspaso( fecha , origen , destino , precio , 'No' , descripcion )
            else: ningunError = False
        else: secciones.Secciones().reportarError( IMPORTACION_FALLIDA )            
    if ningunError: secciones.Secciones().reportarError( EXITO )
          
# ---------------------------------------- #
# -------------- Comprobar --------------- #
# ---------------------------------------- #
        
def comprobarFichero( pNombre ):
    correcto = False
    error = "La importacion ha fallado porque "
    if pNombre != "":
        if pNombre.count(".") == 1:
            nombre , extension = pNombre.split( "." )        
            if nombre == "Aportaciones": correcto = True
            elif nombre == "Comisiones": correcto = True
            elif nombre == "Gastos": correcto = True
            elif nombre == "Transpasos": correcto = True
            else: correcto = False      
            if extension != 'csv': correcto = False
        if not correcto: error += "ha modificado el nombre del fichero o su extensión <br /> <br />"
        else: error = ""    
    else: error += "no ha insertado ningún fichero. <br /> <br />"
    secciones.Secciones().reportarError( error )
    return correcto


def comprobarAportacion( dia , mes , ano , cuenta , isin , tipo , precio , titulos , cambio ):
    correcto = True
    error = ""
    if not utils.comprobarFechaCorrecta( dia , mes , ano ): 
        correcto = False
        error += "    * La fecha " + ano + "/" + mes + "/" + dia + " no existe <br />"       
    else: 
        fecha = datetime.date( int(ano) , int(mes) , int(dia) )
        if not sesion.Sesion().existeCuenta( cuenta ):
            correcto = False
            error += "    * No tienes registrada la cuenta " + cuenta + " <br />"
        if not sesion.Sesion().existeActivo( isin ):
            correcto = False
            error += "    * No tienes registrado el activo " + isin + " <br />"
        if sesion.Sesion().existeAportacion( fecha , cuenta , isin , tipo ):
            correcto = False
            error += "    * Ya existe una operación para " + isin + " del " + str(fecha) + " en la cuenta " + cuenta + "<br />"          
        if tipo != "Compra" and tipo != "Venta":
            correcto = False
            error += "    * El tipo de operación debe ser 'Compra' o 'Venta' <br />"
        if not utils.isFloat( precio ): 
            correcto = False
            error += "    * El precio debe ser un número Real. Comprueba que no has añadido ningún símbolo diferente al punto o la coma para separar la parte decimal <br />"
        if not utils.isFloat( titulos ): 
            correcto = False
            error += "    * El numero de titulos debe ser un número Real. Comprueba que no has añadido ningún símbolo diferente al punto o la coma para separar la parte decimal <br />"
        if not utils.isFloat( cambio ): 
            correcto = False
            error += "    * El tipo de cambio debe ser un número Real. Comprueba que no has añadido ningún símbolo diferente al punto o la coma para separar la parte decimal <br />"    
    if not correcto:secciones.Secciones().agregarError( error )
    return correcto


def comprobarComision( dia , mes , ano , cuenta , tipo , isin , gasto , ingreso ):
    correcto = True
    error = ""
    if not utils.comprobarFechaCorrecta( dia , mes , ano ): 
        correcto = False
        error += "    * La fecha " + ano + "/" + mes + "/" + dia + " no existe <br />"       
    else: 
        fecha = datetime.date( int(ano) , int(mes) , int(dia) )
        if not sesion.Sesion().existeCuenta( cuenta ):
            correcto = False
            error += "    * No tienes registrada la cuenta " + cuenta + " <br />"
        if not sesion.Sesion().existeActivo( isin ) and isin != "*":
            correcto = False
            error += "    * No tienes registrado el activo " + isin + " <br />"
        if sesion.Sesion().existeComision( fecha , cuenta , isin , tipo ):
            correcto = False
            error += "    * Ya existe una operacion para " + isin + " del " + str(fecha) + " en la cuenta " + cuenta + "<br />"          
        if tipo != "Interes" and tipo != "Comisión" and tipo != "Impuesto" and tipo != "Dividendo" and tipo != "Compensación":
            correcto = False
            error += "    * El tipo de operacion debe ser 'Interes', 'Comisión', 'Impuesto' o 'Dividendo'  <br />"
        if not utils.isFloat( gasto ) or not utils.isFloat( ingreso ): 
            correcto = False
            error += "    * El Gasto y el Ingreso deben ser un numeros Reales. Comprueba que no has añadido ningun simbolo diferente al punto o la coma para separar la parte decimal <br />"
    if not correcto: secciones.Secciones().agregarError( error )
    return correcto
  
  
def comprobarTransaccion( dia , mes , ano , cuenta , clasificacion , subClasificacion , gasto , ingreso ):
    correcto = True
    error = ""
    fecha = ""
    if not utils.comprobarFechaCorrecta( dia , mes , ano ): 
        correcto = False
        error += "    * La fecha " + ano + "/" + mes + "/" + dia + " no existe <br />"       
    else: 
        fecha = datetime.date( int(ano) , int(mes) , int(dia) )
        if not sesion.Sesion().existeCuenta( cuenta ):
            correcto = False
            error += "    * No tienes registrada la cuenta " + cuenta + " <br />"
        if not sesion.Sesion().existeClasificacion( clasificacion , subClasificacion ):
            correcto = False
            error += "    * No tienes registrada la clasificacion " + clasificacion + " - " + subClasificacion + ", añadela antes de insertar esta transaccion <br />"
        if sesion.Sesion().existeTransaccion( fecha , cuenta , subClasificacion ):
            correcto = False
            error += "    * Ya existe una operacion para " + clasificacion + " - " + subClasificacion + " del " + str(fecha) + " en la cuenta " + cuenta + "<br />"          
        if not utils.isFloat( gasto ) or not utils.isFloat( ingreso ): 
            correcto = False
            error += "    * El Gasto y el Ingreso deben ser un numeros Reales. Comprueba que no has añadido ningun simbolo diferente al punto o la coma para separar la parte decimal <br />"
    if not correcto: secciones.Secciones().agregarError( error )
    return correcto
 
   
def comprobarTraspaso( dia , mes , ano , origen , destino , precio ):
    correcto = True
    error = ""
    print( ano + "/" + mes + "/" + dia )
    if not utils.comprobarFechaCorrecta( dia , mes , ano ):   
        correcto = False
        error += "    * La fecha " + ano + "/" + mes + "/" + dia + " no existe <br />"       
    else: 
        fecha = datetime.date( int(ano) , int(mes) , int(dia) )
        if not sesion.Sesion().existeCuenta( origen ):
            correcto = False
            error += "    * No tienes registrada la cuenta " + origen + " <br />"
        if not sesion.Sesion().existeCuenta( destino ):
            correcto = False
            error += "    * No tienes registrada la cuenta " + destino + " <br />"    
        if sesion.Sesion().existeTraspaso( fecha , origen , destino ):
            correcto = False
            error += "    * Ya existe un traspaso desde la cuenta " + origen + " hasta la cuenta " + destino + " del " + str(fecha) + "<br />"          
        if not utils.isFloat( precio ):
            correcto = False
            error += "    * El monto del traspaso debe ser un numero Real. Comprueba que no has añadido ningun simbolo diferente al punto o la coma para separar la parte decimal <br />"
    if not correcto: secciones.Secciones().agregarError( error )
    return correcto