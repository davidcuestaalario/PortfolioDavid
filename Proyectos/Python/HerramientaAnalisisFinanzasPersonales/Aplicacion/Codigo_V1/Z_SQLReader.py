# -*- coding: utf-8 -*-
import pymysql;
import csv;
import datetime
import Z_Utils as utilidades

####################################################################    
#----------------------------BASE DATOS----------------------------#
####################################################################

# ------- Crear ------- #

def copiarTabla( cursor , pUsuario , pTabla ):
    tablaNueva = "finanzas_" + pUsuario + "." + pTabla 
    tablaAnterior = "finanzas_" + "." + pTabla

    cursor.execute("CREATE TABLE " + tablaNueva + " LIKE " + tablaAnterior + ";" )
    cursor.execute("INSERT INTO " + tablaNueva + " SELECT * FROM " + tablaAnterior + ";")
    
def crearBaseDatosFinanzas( pUsuario ):
    conexion = pymysql.connect( host="localhost", user="root", passwd="" ) 
    cursor = conexion.cursor()    
    cursor.execute("DROP DATABASE IF EXISTS FINANZAS_" + pUsuario + ";" )
    cursor.execute("CREATE DATABASE FINANZAS_" + pUsuario + ";" )
    
    copiarTabla( cursor , pUsuario , "descripcion" )
    copiarTabla( cursor , pUsuario , "categoria" )
    copiarTabla( cursor , pUsuario , "estrategia" )
    copiarTabla( cursor , pUsuario , "broker" )
    
    copiarTabla( cursor , pUsuario , "indices" )
    copiarTabla( cursor , pUsuario , "aportaciones" )
    copiarTabla( cursor , pUsuario , "comisiones" )
    
    copiarTabla( cursor , pUsuario , "allocation" )
    copiarTabla( cursor , pUsuario , "allocations" )
    copiarTabla( cursor , pUsuario , "region" )
    copiarTabla( cursor , pUsuario , "regiones" )
    copiarTabla( cursor , pUsuario , "sector" )
    copiarTabla( cursor , pUsuario , "sectores" )
    copiarTabla( cursor , pUsuario , "capitalizacion" )
    copiarTabla( cursor , pUsuario , "capitalizaciones" )
    copiarTabla( cursor , pUsuario , "vencimiento" )
    copiarTabla( cursor , pUsuario , "vencimientos" )
    copiarTabla( cursor , pUsuario , "calidad" )
    copiarTabla( cursor , pUsuario , "calidades" )
    copiarTabla( cursor , pUsuario , "entidad" )
    copiarTabla( cursor , pUsuario , "entidades" )

    copiarTabla( cursor , pUsuario , "clasificacion" )
    copiarTabla( cursor , pUsuario , "finanzas_personales" )          
     
def eliminarBaseDatosFinanzas( pUsuario ):
    conexion = pymysql.connect( host="localhost", user="root", passwd="" ) 
    cursor = conexion.cursor()
    cursor.execute("DROP DATABASE IF EXISTS FINANZAS_" + pUsuario + ";" )
    
# ------- Administrar ------- #

def conectarBD( pUsuario ):      
    if pUsuario == None: baseDatos = "usuarios"
    else: baseDatos = 'finanzas_' + pUsuario;
    host = "localhost";
    user = 'root';
    password = '';
    conexion = pymysql.connect( host , user , password , baseDatos );
    return conexion;

def consultarBD( conexion , consulta ):    
    try:
        cursor = conexion.cursor()
        cursor.execute( consulta );
        resultado = cursor.fetchall();
        cursor.close()
        conexion.close()
        return resultado;        
    except Exception as e: raise

def updateBD( conexion , consulta ):    
    try:
        cursor = conexion.cursor()
        cursor.execute( consulta );
        conexion.commit()
        cursor.close()
        conexion.close();      
    except Exception as e: raise

# ---------------------------------------- #
# --------------- COLORES ---------------- #
# ---------------------------------------- #

# -------- Geters -------- #

def getColorFinanzas( pID , pUsuario ):
    consulta = "SELECT color FROM CLASIFICACION WHERE CLASIFICACION = '" + pID + "';";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );
    resultado = resultado[0][0]
    return resultado
    
def getColorInversion( pID , pTipo , pUsuario ):
    if pTipo == "Activo": pTipo = "DESCRIPCION";
    consulta = "SELECT color FROM " + pTipo + " WHERE " + pTipo + " = '" + pID + "';";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );
    resultado = resultado[0][0]
    return resultado

# -------- Editar -------- #
    
def cambiarColor( pUsuario , categoria_distribucion , clasificacion , color ):
    consulta = "UPDATE " + categoria_distribucion + " SET color = '" + color + "' WHERE ";
    consulta += categoria_distribucion + " = '" + clasificacion + "' ;"
    conexion = conectarBD( pUsuario );
    updateBD( conexion , consulta );
    
# ---------------------------------------- #
# ------------- INVERSIONES -------------- #
# ---------------------------------------- #

# -------- Geters -------- #

def getActivos( pUsuario ):   
    consulta = "SELECT * FROM indices";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );        
    return resultado;

def getActivosBy( pUsuario , pCategoria , pEstrategia , pProducto ):       
    categoria = "categoria = '" + pCategoria + "' "
    estrategia = "estrategia = '" + pEstrategia + "' "
    producto = "producto = '" + pProducto + "' "
    if pCategoria == "": categoria = "1"
    if pEstrategia == "": estrategia = "1"
    if pProducto == "": producto = "1"        
    consulta = "SELECT * FROM indices WHERE " + categoria + " and " + estrategia + " and " + producto;      
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

def getPosiciones( pUsuario ):    
    consulta = "SELECT * FROM aportaciones";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );
    return resultado;

def getAportacionesBy( pUsuario , pFecha , pIsin , pBroker ):
    fecha = " year(fecha) = '" + pFecha + "' "
    isin = " isin = '" + pIsin + "' "
    broker = " broker = '" + pBroker + "' "
    if pFecha == "": fecha = " 1 "
    if pIsin == "": isin = " 1 "
    if pBroker == "": broker = " 1 "
    consulta = "SELECT * FROM aportaciones WHERE " + fecha + " and " + isin + " and " + broker + " ORDER BY fecha ASC";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

def getComisiones( pUsuario ):    
    consulta = "SELECT * FROM comisiones";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

def getComisionesBy( pUsuario , pFecha , pIsin , pBroker ):
    fecha = " year(fecha) = '" + pFecha + "' "
    isin = " isin = '" + pIsin + "' "
    broker = " broker = '" + pBroker + "' "
    if pFecha == "": fecha = " 1 "
    if pIsin == "": isin = " 1 "
    if pBroker == "": broker = " 1 "
    consulta = "SELECT * FROM comisiones WHERE " + fecha + " and " + isin + " and " + broker + " ORDER BY fecha ASC";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

# -------- Anadir -------- #

def anadirActivo( pUsuario , isin , tipo , categoria , estrategia , producto , link ):
    existe = existeActivo( pUsuario , isin )
    if existe:
        cambiarActivo( pUsuario , isin , tipo , categoria , estrategia , producto , link )
    else:
        consulta = "INSERT INTO indices ( isin , producto , categoria , estrategia , descripcion , link ) "
        consulta += "VALUES ( '" + isin + "' , '" + tipo + "' , '" + categoria + "' , '" + estrategia + "' , '" + producto + "' , '" + link + "' );"
        conexion = conectarBD( pUsuario );
        updateBD( conexion , consulta );
        
def anadirAportacion( pUsuario , fecha , isin , titulos , precio , broker , operacion ):
    existe = existeAportacion( pUsuario , isin , fecha )
    if existe:
        cambiarAportacion( pUsuario , fecha , isin , titulos , precio , broker , operacion )
    else:
        consulta = "INSERT INTO aportaciones ( fecha , isin , titulos , precio , broker , operacion ) "
        consulta += "VALUES ( '" + fecha + "' , '" + isin + "' , '" + str(titulos) + "' , '" + str(precio) + "' , '" + broker + "' , '" + operacion + "' );"
        conexion = conectarBD( pUsuario );
        updateBD( conexion , consulta );
        
def anadirComision( pUsuario , fecha , isin , broker , comision , precio ):
    existe = existeComision( pUsuario , isin , fecha )
    if existe:
        cambiarComision( pUsuario , fecha , isin , broker , comision , precio )
    else:
        consulta = "INSERT INTO comisiones ( fecha , isin , broker , comision , precio ) "
        consulta += "VALUES ( '" + fecha + "' , '" + isin + "' , '" + broker + "' , '" + comision + "' , '" + str(precio) + "' );"
        conexion = conectarBD( pUsuario );
        updateBD( conexion , consulta );
    
# ------- Eliminar ------- #

def eliminarActivo( pUsuario , isin ):
    consulta = "DELETE FROM indices WHERE "
    consulta += "isin = '" + isin + "';"
    conexion = conectarBD( pUsuario );
    updateBD( conexion , consulta );
    
def eliminarAportacion( pUsuario , isin , fecha ):
    consulta = "DELETE FROM aportaciones WHERE "
    consulta += "isin = '" + isin + "' and fecha = '" + fecha + "' ;"
    conexion = conectarBD( pUsuario );
    updateBD( conexion , consulta );
    
def eliminarComision( pUsuario , isin , fecha ):
    consulta = "DELETE FROM comisiones WHERE "
    consulta += "isin = '" + isin + "' and fecha = '" + fecha + "' ;"
    conexion = conectarBD( pUsuario );
    updateBD( conexion , consulta );
    
# -------- Editar -------- #

def cambiarActivo( pUsuario , isin , tipo , categoria , estrategia , producto , link ):
    consulta = "UPDATE indices SET producto = '" + tipo + "' , categoria = '" + categoria + "' , estrategia = '" + estrategia + "' , descripcion = '" + producto + "' , link = '" + link + "' " 
    consulta += " WHERE isin = '" + isin + "';"
    conexion = conectarBD( pUsuario );
    updateBD( conexion , consulta )
    
def cambiarAportacion( pUsuario , fecha , isin , titulos , precio , broker , operacion ): 
    consulta = "UPDATE aportaciones SET titulos = '" + str(titulos) + "' , precio = '" + str(precio) + "' , broker = '" + broker + "' , operacion = '" + operacion + "' " 
    consulta += " WHERE isin = '" + isin + "' and fecha = '" + fecha + "' ;"
    conexion = conectarBD( pUsuario );
    updateBD( conexion , consulta )
    
def cambiarComision( pUsuario , fecha , isin , broker , comision , precio ):
    consulta = "UPDATE comisiones SET broker = '" + broker + "' , comision = '" + comision + "' , precio = '" + str(precio) + "' " 
    consulta += " WHERE isin = '" + isin + "' and fecha = '" + fecha + "' ;"
    conexion = conectarBD( pUsuario );
    updateBD( conexion , consulta )
    
# ------- Comprobaciones ------- #

def existeActivo( pUsuario , isin ):
    existe = True;
    consulta = "SELECT isin FROM indices WHERE "
    consulta += "isin = '" + isin + "' ;"
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );
    if resultado == (): existe = False;
    return existe;

def existeAportacion( pUsuario , isin , fecha ):   
    existe = True;
    consulta = "SELECT isin FROM aportaciones WHERE "
    consulta += "isin = '" + isin + "' and fecha = '" + fecha + "' ;"
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );
    if resultado == (): existe = False;
    return existe;

def existeComision( pUsuario , isin , fecha ):
    existe = True;
    consulta = "SELECT isin FROM comisiones WHERE "
    consulta += "isin = '" + isin + "' and fecha = '" + fecha + "' ;"
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );
    if resultado == (): existe = False;
    return existe;

# ---------------------------------------- #
# -------- CATEGORIA DISTRIBUCION -------- #
# ---------------------------------------- #

# -------- Geters -------- #

def getCategoriaDistribucion( pUsuario , pCategoria ):
    consulta = "SELECT * FROM " + pCategoria;
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

# -------- Anadir -------- #

def anadirCategoriaDistribucion( pUsuario , categoria_distribucion , clasificacion , color ):
    existe = existeCategoriaDistribucion( pUsuario , categoria_distribucion , clasificacion )
    if existe:
        cambiarColor( pUsuario , categoria_distribucion , clasificacion , color )
    else:
        consulta = "INSERT INTO " + categoria_distribucion + " ( " + categoria_distribucion + " , color ) "
        consulta += "VALUES ( '" + clasificacion + "' , '" + color + "' );"
        conexion = conectarBD( pUsuario );
        updateBD( conexion , consulta );

# ------- Eliminar ------- #

def eliminarCategoriaDistribucion( pUsuario , categoria_distribucion , clasificacion ):
    consulta = "DELETE FROM " + categoria_distribucion + " WHERE "
    consulta += categoria_distribucion + " = '" + clasificacion + "' ;"
    conexion = conectarBD( pUsuario );
    updateBD( conexion , consulta );

# -------- Editar -------- #
# ------- Comprobaciones ------- # 

def existeCategoriaDistribucion( pUsuario , categoria_distribucion , clasificacion ):
    existe = True;
    consulta = "SELECT " + categoria_distribucion + " FROM " + categoria_distribucion + " WHERE "
    consulta += categoria_distribucion + " = '" + clasificacion + "' ;"
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );
    if resultado == (): existe = False;
    return existe;

# ---------------------------------------- #
# ------------ COMPOSICIONES ------------- #
# ---------------------------------------- #

# ------- Geters ------- #

def getAllocations( pUsuario ):
    consulta = "SELECT * FROM allocations";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

def getRegiones( pUsuario ):
    consulta = "SELECT * FROM regiones";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );    
    return resultado;

def getSectores( pUsuario ):
    consulta = "SELECT * FROM sectores";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );  
    return resultado;

def getCapitalizaciones( pUsuario ):   
    consulta = "SELECT * FROM capitalizaciones";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );
    return resultado;

def getVencimientos( pUsuario ):
    consulta = "SELECT * FROM vencimientos";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );  
    return resultado;

def getCalidadesCrediticias( pUsuario ):
    consulta = "SELECT * FROM calidades";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta ); 
    return resultado;

def getEntidadesEmisoras( pUsuario ):
    consulta = "SELECT * FROM entidades";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );    
    return resultado;

# ---------------------------------------- #
# --------------- FINANZAS --------------- #
# ---------------------------------------- #

# ------- Geters ------- #

def getFinanzas( pUsuario ):       
    consulta = "SELECT * FROM finanzas_personales ORDER BY fecha ASC";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

def getFinanzasBy( pUsuario , pFecha , pClasificacion ):       
    fecha = " year(fecha) = '" + pFecha + "' "
    clasificacion = " clasificacion = '" + pClasificacion + "' "
    if pFecha == "": fecha = " 1 "
    if pClasificacion == "": clasificacion = " 1 "
    consulta = "SELECT * FROM finanzas_personales WHERE " + fecha + " and " + clasificacion + " ORDER BY fecha ASC";
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

def getClases( pUsuario ):
    consulta = "SELECT * FROM clasificacion";
    conexion = conectarBD( pUsuario );
    resultados = consultarBD( conexion , consulta );
    clases = []
    for resultado in resultados:
        clases.append( resultado[0] )
    return clases;

# ------- Anadir ------- #

def anadirFinanzas( pUsuario , fecha , clasificacion , asunto , descripcion , gasto , ingreso ):
    existe = existeFinanza( pUsuario , fecha , clasificacion , asunto , descripcion )
    if existe:
        cambiarFinanza( pUsuario , fecha , clasificacion , asunto , descripcion , gasto , ingreso )
    else:
        consulta = "INSERT INTO finanzas_personales ( fecha , clasificacion , asunto , descripcion , gasto , ingreso )"
        consulta += "VALUES ( '" + fecha + "' , '" + clasificacion + "' , '" + asunto + "' , '" + descripcion + "' , '" + str(gasto) + "' , '" + str(ingreso) + "' );"
        conexion = conectarBD( pUsuario );
        updateBD( conexion , consulta );

# ------- Eliminar ------- #

def eliminarFinanzas( pUsuario , fecha , clasificacion , asunto , descripcion ):
    consulta = "DELETE FROM finanzas_personales WHERE "
    consulta += "fecha = '" + fecha + "' and clasificacion = '" + clasificacion + "' and asunto = '" + asunto + "' and descripcion ='" + descripcion + "';"
    conexion = conectarBD( pUsuario );
    updateBD( conexion , consulta );

# ------- Editar ------- #  

def cambiarFinanza( pUsuario , fecha , clasificacion , asunto , descripcion , gasto , ingreso ):
    consulta = "UPDATE finanzas_personales SET gasto = gasto + '" + str(gasto) + "' WHERE ";
    consulta += "fecha = '" + fecha + "' and clasificacion = '" + clasificacion + "' and asunto = '" + asunto + "' and descripcion ='" + descripcion + "';"
    conexion = conectarBD( pUsuario );
    updateBD( conexion , consulta )
    
    consulta = "UPDATE finanzas_personales SET ingreso = ingreso + '" + str(ingreso) + "' WHERE ";
    consulta += "fecha = '" + fecha + "' and clasificacion = '" + clasificacion + "' and asunto = '" + asunto + "' and descripcion ='" + descripcion + "';"
    conexion = conectarBD( pUsuario );
    updateBD( conexion , consulta )   
    
# ------- Comprobaciones ------- # 

def existeFinanza( pUsuario , fecha , clasificacion , asunto , descripcion ):
    existe = True;
    consulta = "SELECT clasificacion FROM finanzas_personales WHERE "
    consulta += "fecha = '" + fecha + "' and clasificacion = '" + clasificacion + "' and asunto = '" + asunto + "' and descripcion ='" + descripcion + "';"
    conexion = conectarBD( pUsuario );
    resultado = consultarBD( conexion , consulta );
    if resultado == (): existe = False;
    return existe;

# ---------------------------------------- #
# --------------- USUARIOS --------------- #
# ---------------------------------------- #

# ------- Geters ------- #

def getUsuarios( ):
    consulta = "SELECT * FROM usuario;";
    conexion = conectarBD( None );
    resultado = consultarBD( conexion , consulta );
    return resultado

def getAdmisiones( ):
    consulta = "SELECT * FROM admision;";
    conexion = conectarBD( None );
    resultado = consultarBD( conexion , consulta );
    return resultado

def getAdmision( pUsuario ):
    consulta = "SELECT * FROM admision WHERE usuario = '" + pUsuario + "';";
    conexion = conectarBD( None );
    resultado = consultarBD( conexion , consulta );
    return resultado[0]

def getPermiso( pUsuario ):
    consulta = "SELECT tipo FROM usuario WHERE usuario = '" + pUsuario + "';";
    conexion = conectarBD( None );
    resultado = consultarBD( conexion , consulta );
    return resultado[0][0]

# ------- Anadir ------- #
    
def anadirUsuario( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , tipo ):
    consulta = "INSERT INTO usuario ( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , tipo )"
    consulta += "VALUES ( '" + nombre + "' , '" + apellido1 + "' , '" + apellido2 + "' , '" + usuario + "' , '" + DNI + "' , '" + telefono + "' , '" + email + "' , '" + password + "' , '" + tipo + "' );"
    conexion = conectarBD( None );
    updateBD( conexion , consulta );

def anadirAdmision( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password ):
    consulta = "INSERT INTO admision ( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password )"
    consulta += "VALUES ( '" + nombre + "' , '" + apellido1 + "' , '" + apellido2 + "' , '" + usuario + "' , '" + DNI + "' , '" + telefono + "' , '" + email + "' , '" + password + "' );"
    conexion = conectarBD( None );
    updateBD( conexion , consulta );

# ------- Eliminar ------- #

def eliminarUsuario( pUsuario ):
    consulta = "DELETE FROM usuario WHERE usuario = '" + pUsuario + "';";
    conexion = conectarBD( None );
    updateBD( conexion , consulta );   
    
def eliminarAdmision( pUsuario ):
    consulta = "DELETE FROM admision WHERE usuario = '" + pUsuario + "';";
    conexion = conectarBD( None );
    updateBD( conexion , consulta );
    
# ------- Editar ------- #  

def cambiarPermisosUsuario( pUsuario , pTipo ):
    consulta = "UPDATE usuario SET tipo = '" + pTipo + "' WHERE usuario = '" + pUsuario + "';";
    conexion = conectarBD( None );
    updateBD( conexion , consulta )
    
# ------- Comprobaciones ------- # 

def existeUsuario( pUsuario ):
    existe = False;
    consulta = "SELECT usuario FROM usuario WHERE usuario = '" + pUsuario + "';";
    conexion = conectarBD( None );
    resultado = consultarBD( conexion , consulta );
    if resultado == (): existe = True;
    return existe;

def existeAdmision( pUsuario ):   
    existe = False;
    consulta = "SELECT usuario FROM admision WHERE usuario = '" + pUsuario + "';";
    conexion = conectarBD( None );
    resultado = consultarBD( conexion , consulta );
    if resultado != (): existe = True;
    return existe;

def contrasenaCorrecta( pUsuario , pContrasena ):
    existe = False;
    consulta = "SELECT usuario FROM usuario WHERE usuario = '" + pUsuario + "' AND password = '" + pContrasena + "' ;";
    conexion = conectarBD( None );
    resultado = consultarBD( conexion , consulta );
    if resultado != (): existe = True;
    return existe;
    
####################################################################    
#-------------------------------CSV--------------------------------#
####################################################################
    
def getActivosCSV( ruta , activos_csv ):   
    resultado = [ ];
    fichero = ruta + activos_csv;
    conexion = csv.reader( open( fichero ) );   
    for linea in conexion:
        isin , producto , categoria , estrategia , descripcion , link = linea[0].split( ";" );
        isin = isin.replace( " " , "" );
        producto = producto.replace( " " , "" );
        categoria = categoria.replace( " " , "" );
        estrategia = estrategia.replace( " " , "" );
        # descripcion = descripcion.replace( " " , "" );
        consulta = [ ];
        if isin != "ISIN":
            consulta.append( isin );
            consulta.append( producto );
            consulta.append( categoria );
            consulta.append( estrategia );
            consulta.append( descripcion );
            link = link.replace( " " , "" );
            consulta.append( link );
            resultado.append( tuple(consulta) );     
    return tuple(resultado);
       
        
def getPosicionesCSV( ruta , comisiones_csv ):   
    resultado = [ ];
    fichero = ruta + comisiones_csv;
    conexion = csv.reader( open( fichero ) );    
    for linea in conexion:
        dia , mes , ano , isin , titulos , precio , broker , operacion = linea[0].split( ";" );
        isin = isin.replace( " " , "" );
        consulta = [ ];
        if isin != "ISIN":
            date = datetime.date( int(ano) , int(mes) , int(dia) );
            consulta.append( date );
            consulta.append( isin );
            consulta.append( float(titulos) );
            precio = precio.replace( "€" , "" );
            consulta.append( float(precio) );
            consulta.append( broker );
            consulta.append( operacion );
            resultado.append( tuple(consulta) );    
    return tuple(resultado);

    
def getComisionesCSV( ruta , posiciones_csv ):   
    resultado = [ ];
    fichero = ruta + posiciones_csv;
    conexion = csv.reader( open( fichero ) );    
    for linea in conexion:
        dia , mes , ano , isin , broker , comision , precio = linea[0].split( ";" );
        isin = isin.replace( " " , "" );
        consulta = [ ];
        if isin != "ISIN":
            date = datetime.date( int(ano) , int(mes) , int(dia) );
            consulta.append( date );
            consulta.append( isin );
            consulta.append( broker );       
            consulta.append( comision );
            consulta.append( float(precio) );
            resultado.append( tuple(consulta) );    
    return tuple(resultado); 


def getComposicionesCSV( ruta , composiciones_csv ):
    resultado = [ ];
    fichero = ruta + composiciones_csv;
    conexion = csv.reader( open( fichero ) );
  
    for linea in conexion:
        linea = linea[0]
        linea = linea.replace( " " , "" );
        isin , region , sector , capitalizacion , vencimiento , calidad , entidad = linea.split( ";" );
        
        consulta = [ ];
        if isin != "ISIN":
           region = region.split("&")
           sector = sector.split("&")
           capitalizacion = capitalizacion.split("&")
           vencimiento = vencimiento.split("&")
           calidad = calidad.split("&")
           entidad = entidad.split("&")
           consulta.append( isin )
           consulta.append( region )
           consulta.append( sector )
           consulta.append( capitalizacion )
           consulta.append( vencimiento )
           consulta.append( calidad )
           consulta.append( entidad )
           resultado.append( tuple(consulta) );  
    return tuple(resultado); 

def getFinanzasCSV( ruta , finanzas_csv ):
    resultado = [ ];
    fichero = ruta + finanzas_csv;
    conexion = csv.reader( open( fichero ) );    
    for linea in conexion:
        dia , mes , ano , clase , asunto , descripcion , gasto , ingreso = linea[0].split( ";" );
        dia = dia.replace( " " , "" );
        mes = mes.replace( " " , "" );
        ano = ano.replace( " " , "" );
        gasto = gasto.replace( " " , "" );
        ingreso = ingreso.replace( " " , "" );
        consulta = [ ];
        if dia != "Dia":
            mes = utilidades.parseMesToInt( mes );
            date = datetime.date( int(ano) , int(mes) , int(dia) );
            consulta.append( date );
            consulta.append( clase );
            consulta.append( asunto );       
            consulta.append( descripcion );
            consulta.append( float(gasto) );
            consulta.append( float(ingreso) );
            resultado.append( tuple(consulta) );    
    return tuple(resultado);

####################################################################    
#--------------------------- CSV TO SAQL --------------------------#
####################################################################

def finanzasCSVtoSQL( ruta , finanzas_csv , finanzas_sql ):   
    resultado = getFinanzasCSV( ruta , finanzas_csv );
    fichero = open( ruta + finanzas_sql , 'w');
    for date , clase , asunto , descripcion , gasto , ingreso in resultado:
        linea = ""               
        linea += "INSERT INTO FINANZAS_PERSONALES( FECHA , CLASIFICACION , ASUNTO , DESCRIPCION , GASTO , INGRESO )" 
        linea += "VALUES('" + str(date.year) + "-" + str(date.month) + "-" + str(date.day) + "' , "
        linea += "'"+ clase + "' , '" + asunto + "' , '" + descripcion + "' , " + str(gasto) + " , " + str(ingreso) + "   );"
        fichero.write( linea );
        fichero.write( "\n" ); 
    fichero.close;

####################################################################    
#------------------------------- MAIN -----------------------------#
####################################################################

def main_1():               
    fuente = 'csv'; # 'bd'
    #ruta = 'C:/Users/david/Dropbox (Personal)/Finanzas/Scraper/BaseDatos';
    ruta = 'C:/Users/Devilvil/Desktop/Scraper/BaseDatos';
    activos_csv = '/Inversiones_Activos.csv';
    posiciones_csv = '/Inversiones_Posiciones.csv';
    comisiones_csv = '/Inversiones_Comisiones.csv';
    composiciones_csv = '/Inversiones_Composicion.csv';
    finanzas_csv = '/FinanzasPersonales.csv';
    
    resultado = getFinanzasCSV( ruta , finanzas_csv );
    print( resultado )

    
def main_2():
    
    fuente = 'bd'; # 'csv'
    #ruta = 'C:/Users/david/Dropbox (Personal)/Finanzas/Scraper/BaseDatos';
    ruta = 'C:/Users/Devilvil/Desktop/Scraper/BaseDatos';
    fichero_sql = '/BaseDatos.sql'
    usuario = 'davidcuesta';
        
    resultado = getFinanzas( ruta , usuario );
    print( resultado )


def main_3():
    #ruta = 'C:/Users/david/Dropbox (Personal)/Finanzas/Scraper/BaseDatos';
    ruta = 'C:/Users/Devilvil/Desktop/Scraper/BaseDatos';
    finanzas_csv = '/FinanzasPersonales.csv';
    finanzas_sql = '/FinanzasPersonales_sql.sql';
    
    finanzasCSVtoSQL( ruta , finanzas_csv , finanzas_sql )

#main_2()

#print ( getColorFinanzas( "Salario" , 'davidcuesta' ) )
#print ( getColorInversion( "Inditex" ,"Activo" , 'davidcuesta' ) )
#print ( getAdmisiones( ) )
#print ( getUsuarios( ) )

#crearBaseDatosFinanzas( "juan" )
#eliminarBaseDatosFinanzas( "juan" )
#print ( existeUsuario( "pepito" ) )

#cambiarPermisosUsuario( "devilvil" , "p" )
#eliminarUsuario( "devilvil" )
#anadirUsuario( "nombre" , "apellido1" , "apellido2" , "usuario" , "DNI" , "telefono" , "email" , "password" , "tipo" )
#print ( getAdmision( "venganito" ))
#anadirAdmision( "nombre" , "apellido1" , "apellido2" , "usuaaaario" , "DNI" , "telefono" , "email" , "password" )
#print ( contrasenaCorrecta( "davidcuesta" , "1234" ) )
#print ( getPermiso( "jose" ) )

#print (getFinanzasBy( "davidcuesta" , "" , "Transporte"  ))
#print (getFinanzasBy( "davidcuesta" , "2018" , ""  ))
#print( getFinanzasBy( "davidcuesta" , "2020" , "Transporte" ) )

#existeFinanza( "davidcuesta" , "2020-10-08" , "apuestas" , "aaaaaaaa" , "aaaaaaaa" )

#print ( existeFinanza( "davidcuesta" , "2020-10-08" , "apuestas" , "aaaaaaaa" , "aaaaaaaa" ) )
#anadirFinanzas( "davidcuesta" , "2020-10-08" , "apuestas" , "aaaaaaaa" , "aaaaaaaa" , 5 , 5 )
#print( getFinanzasBy( "davidcuesta" , "" , "apuestas" ) )

#cambiarColor( "davidcuesta" , "sector" , 'Salud' , 'rgba( 0 , 0 , 0 , 1 )' )
#eliminarCategoriaDistribucion( "davidcuesta" , "clasificacion" , 'Transporte' )
#print(existeCategoriaDistribucion( "davidcuesta" , "clasificacion" , 'Banco' ))
#anadirCategoriaDistribucion( "davidcuesta" , "clasificacion" , 'Viajes' , 'rgba( 0 , 0 , 0 , 1 )' )

#print( existeActivo( "davidcuesta" , 'IE00B03HD191' ) )
#print( existeActivo( "davidcuesta" , 'IE00B03HD192' ) )
#print( existeAportacion( "davidcuesta" , 'IE00B03HD191' , '2019-09-25' ) )
#print( existeAportacion( "davidcuesta" , 'IE00B03HD191' , '2019-09-26' ) )
#print( existeComision( "davidcuesta" , 'IE00B03HD191' , '2019-09-25' ) )
#print( existeComision( "davidcuesta" , 'IE00B03HD191' , '2019-09-26' ) )

#print( editarActivo( "davidcuesta" , 'IE00B03HD191' , "tipo" , "Bono" , "CarteraPermanente" , "Inditex" , "link" ) )  
#print( editarAportacion( "davidcuesta" , '2019-09-25' , 'IE00B03HD191' , 50 , 1000 , "DeGiro" , "compra" ) )   
#print( editarComision( "davidcuesta" , '2019-09-25' , 'IE00B03HD191' , "DeGiro" , "comision" , 1000 ) )

#eliminarActivo( "davidcuesta" , 'IE00B03HD191' )
#eliminarAportacion( "davidcuesta" , 'IE00B03HD191' , '2019-09-25' )
#eliminarComision( "davidcuesta" , 'IE00B03HD191' , '2019-09-25' )

print(getActivosBy( "davidcuesta" , "" , "" , "Inditex" ))