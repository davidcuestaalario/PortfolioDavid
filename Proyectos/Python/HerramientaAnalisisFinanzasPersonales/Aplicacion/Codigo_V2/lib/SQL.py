# -*- coding: utf-8 -*-
import pymysql

from lib import Utils as utils

# from datetime import datetime
# from datetime import timedelta


 
 
 ##    sql.actualizarCredenciales( pUsuario , pContrasena )

####################################################################    
#--------------------------- BASE DATOS ---------------------------#
####################################################################

IP = 'localhost'
ADMIN_USUARIO = 'root'
ADMIN_CONTRASENA = ''
BD_USUARIO = 'usuarios'

# ------- Conectar ------- #

def conectarBD( pUsuario , pPassword , pBaseDatos ):      
    if pBaseDatos == None: conexion = pymysql.connect( IP , pUsuario , pPassword )
    else: conexion = pymysql.connect( IP , pUsuario , pPassword , pBaseDatos )
    return conexion

# ------- Consultar ------- #

def consultarBD( conexion , consulta ):    
    #print("CONSULTA: " , consulta)
    try:
        cursor = conexion.cursor()
        cursor.execute( consulta )
        resultado = cursor.fetchall()
        cursor.close()
        conexion.close()
        return resultado       
    except Exception as e: raise

# ------- Actualizar ------- #

def updateBD( conexion , consulta ):    
    try:
        cursor = conexion.cursor()
        cursor.execute( consulta )
        conexion.commit()
        cursor.close()
        conexion.close()  
    except Exception as e: raise

# --------- Existe --------- #

def existeBD( conexion , consulta ):   
    existe = False;
    resultado = consultarBD( conexion , consulta )
    if resultado != (): existe = True
    return existe
    
# ------- Crear BD ------- #

def copiarTabla( cursor , pUsuario , pTabla ):
    tablaNueva = "BD_" + pUsuario + "." + pTabla 
    tablaAnterior = "BD_" + "." + pTabla
    
    cursor.execute("CREATE TABLE " + tablaNueva + " LIKE " + tablaAnterior + ";" )
    cursor.execute("INSERT INTO " + tablaNueva + " SELECT * FROM " + tablaAnterior + ";")
    
    
def crearBD( pUsuario , pContrasena , usuario ):
    conexion = conectarBD( pUsuario , pContrasena , None ) 
    cursor = conexion.cursor()    
    cursor.execute("DROP DATABASE IF EXISTS BD_" + usuario + ";" )
    cursor.execute("CREATE DATABASE BD_" + usuario + ";" )
    
    copiarTabla( cursor , usuario , "PRODUCTO" )
    copiarTabla( cursor , usuario , "ESTRATEGIA" )
    copiarTabla( cursor , usuario , "ACTIVO" )
    
    copiarTabla( cursor , usuario , "CATEGORIA" )
    copiarTabla( cursor , usuario , "CATEGORIZACION" )
    
    copiarTabla( cursor , usuario , "CLASIFICACION" )
    copiarTabla( cursor , usuario , "SUBCLASIFICACION" )
    
    copiarTabla( cursor , usuario , "ALLOCATION" )
    copiarTabla( cursor , usuario , "SUBALLOCATION" )
    
    copiarTabla( cursor , usuario , "CUENTA" )
    copiarTabla( cursor , usuario , "APORTACION" )
    copiarTabla( cursor , usuario , "COMISION" )
    copiarTabla( cursor , usuario , "TRASPASO" )
    copiarTabla( cursor , usuario , "TRANSACCION" )

# ------- Usuarios y Permisos ------- #

def crearUsuarioBD( usuario , contrasena ):
    conexion = conectarBD( ADMIN_USUARIO , ADMIN_CONTRASENA , None ) 
    cursor = conexion.cursor()
    cursor.execute("DROP USER IF EXISTS '"+ usuario +"'@'"+ IP +"';")
    cursor.execute("CREATE USER '"+ usuario +"'@'"+ IP +"' IDENTIFIED BY '"+ contrasena +"';")
    cursor.execute("GRANT ALL PRIVILEGES ON usuarios.usuario TO '"+ usuario +"'@'"+ IP +"';")
       
            
def asignarPermisosUsuarioBD( pUsuario , pContrasena , usuario , permisos ):
    conexion = conectarBD( pUsuario , pContrasena , None ) 
    cursor = conexion.cursor()    
    cursor.execute("GRANT ALL PRIVILEGES ON BD_"+ usuario +".* TO '"+ usuario +"'@'"+ IP +"';")
    if permisos >= 3: 
        cursor.execute("GRANT DELETE , INSERT , SELECT , UPDATE ON usuarios.accesos TO '"+ usuario +"'@'"+ IP +"';")
    if permisos >= 2: 
        # TODO para dar permisos de crear basededatos hay que dar permiso a todo
        cursor.execute("GRANT ALL PRIVILEGES ON *.* TO '"+ usuario +"'@'"+ IP +"';")
        cursor.execute("GRANT DELETE , INSERT , SELECT , UPDATE ON usuarios.admision TO '"+ usuario +"'@'"+ IP +"';")
    if permisos >= 1: 
        cursor.execute("GRANT DELETE , INSERT , SELECT , UPDATE ON usuarios.usuario TO '"+ usuario +"'@'"+ IP +"';")
        
# ------- Eliminar ------- #

def eliminarBD( pUsuario , pContrasena , usuario ):
    conexion = conectarBD( pUsuario , pContrasena , None ) 
    cursor = conexion.cursor()
    cursor.execute("DROP DATABASE IF EXISTS BD_" + usuario + ";" )


def eliminarUsuarioBD( pUsuario , pContrasena , usuario ):
    conexion = conectarBD( pUsuario , pContrasena , None ) 
    cursor = conexion.cursor()
    cursor.execute("DROP USER IF EXISTS " + usuario + "@" + IP + ";" )
    
####################################################################    
#----------------------------- GETERS -----------------------------#
####################################################################

# ---------------------------------------- #
# --------------- Usuarios --------------- #
# ---------------------------------------- #

def getUsuariosBy( pUsuario , pContrasena , pUsuarioBuscado , pDNI , pNombre , pApellido1 , pApellido2 , pPermisos , pOrden ):
    usuario = utils.sqlCondicion( 'usuario' , 'like' , pUsuarioBuscado )
    dni = utils.sqlCondicion( 'DNI' , 'like' , pDNI )
    nombre = utils.sqlCondicion( 'nombre' , 'like' , pNombre )
    apellido1 = utils.sqlCondicion( 'apellido1' , 'like' , pApellido1 )
    apellido2 = utils.sqlCondicion( 'apellido2' , 'like' , pApellido2 )
    permisos = utils.sqlCondicion( 'permisos' , 'like' , pPermisos )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM usuario WHERE " + usuario + " AND " + dni + " AND " + nombre + " AND " + apellido1 + " AND " + apellido2 + " AND " + permisos + " " + orden    
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    resultado = consultarBD( conexion , consulta ); 
    return resultado;

def getUsuarios( pUsuario , pContrasena ):
    consulta = "SELECT * FROM usuario;"
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    resultado = consultarBD( conexion , consulta )
    return resultado

def getUsuario( pUsuario , pContrasena , usuario ):
    consulta = "SELECT * FROM usuario WHERE usuario = '" + usuario + "';"
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    resultado = consultarBD( conexion , consulta )
    return resultado[0]

def getPermisos( pUsuario , pContrasena ):
    consulta = "SELECT permisos FROM usuario WHERE usuario = '" + pUsuario + "';"
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    resultado = consultarBD( conexion , consulta )
    return resultado[0][0]

def getSal( pUsuario ):
    consulta = "SELECT sal FROM usuario WHERE usuario = '" + pUsuario + "';"
    conexion = conectarBD( ADMIN_USUARIO , ADMIN_CONTRASENA , BD_USUARIO )
    resultado = consultarBD( conexion , consulta )
    return resultado[0][0]

# ---------------------------------------- #
# -------------- Admisiones -------------- #
# ---------------------------------------- #

def getAdmisionesBy( pUsuario , pContrasena , pUsuarioBuscado , pDNI , pNombre , pApellido1 , pApellido2 , pOrden ):
    usuario = utils.sqlCondicion( 'usuario' , 'like' , pUsuarioBuscado )
    dni = utils.sqlCondicion( 'DNI' , 'like' , pDNI )
    nombre = utils.sqlCondicion( 'nombre' , 'like' , pNombre )
    apellido1 = utils.sqlCondicion( 'apellido1' , 'like' , pApellido1 )
    apellido2 = utils.sqlCondicion( 'apellido2' , 'like' , pApellido2 )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM admision WHERE " + usuario + " AND " + dni + " AND " + nombre + " AND " + apellido1 + " AND " + apellido2 + " " + orden    
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    resultado = consultarBD( conexion , consulta ); 
    return resultado;

def getAdmisiones( pUsuario , pContrasena ):
    consulta = "SELECT * FROM admision;"
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    resultado = consultarBD( conexion , consulta )
    return resultado

def getAdmision( pUsuario , pContrasena , usuario ):
    consulta = "SELECT * FROM admision WHERE usuario = '" + usuario + "';";
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    resultado = consultarBD( conexion , consulta )
    return resultado[0]

# ---------------------------------------- #
# ---------------- Activo ---------------- #
# ---------------------------------------- #

def getActivo( pUsuario , pContrasena , isin ):
    consulta = "SELECT * FROM Activo WHERE isin = '" + isin + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta )
    return resultado[0]

def getActivos( pUsuario , pContrasena ):
    consulta = "SELECT * FROM Activo;"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta )
    return resultado

def getActivosBy( pUsuario , pContrasena , pISIN , pProducto , pEstrategia , pOrden ):       
    isin = utils.sqlCondicion( 'ISIN' , '=' , pISIN )
    producto = utils.sqlCondicion( 'tipo_producto' , '=' , pProducto )
    estrategia = utils.sqlCondicion( 'estrategia' , '=' , pEstrategia )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM activo WHERE " + isin + " and " + producto + " and " + estrategia + " " + orden;      
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

# ---------------------------------------- #
# -------------- Estrategia -------------- #
# ---------------------------------------- #

def getEstrategia( pUsuario , pContrasena , estrategia ):
    consulta = "SELECT * FROM estrategia WHERE estrategia = '" + estrategia + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta )
    return resultado[0]
        
def getEstrategias( pUsuario , pContrasena ):
    consulta = "SELECT * FROM Estrategia;"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta )
    return resultado

def getEstrategiasBy( pUsuario , pContrasena , pEstrategia , pOrden ):       
    estrategia = utils.sqlCondicion( 'estrategia' , '=' , pEstrategia )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM estrategia WHERE " + estrategia + " " + orden;      
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

# ---------------------------------------- #
# -------------- Categoria --------------- #
# ---------------------------------------- #

def getCategoria( pUsuario , pContrasena , categoria ):
    consulta = "SELECT * FROM categoria WHERE categoria = '" + categoria + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta )
    return resultado[0]

def getCategorias( pUsuario , pContrasena ):
    consulta = "SELECT * FROM Categoria;"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta )
    return resultado

def getCategoriasBy( pUsuario , pContrasena , pCategoria , pOrden ):       
    categoria = utils.sqlCondicion( 'categoria' , '=' , pCategoria )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM categoria WHERE " + categoria + " " + orden;      
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

def getCategorizacionesBy( pUsuario , pContrasena , pIsin , pOrden ):
    isin = utils.sqlCondicion( 'isin' , '=' , pIsin )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM categorizacion WHERE " + isin + " " + orden;      
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

# ---------------------------------------- #
# --------------- Producto --------------- #
# ---------------------------------------- #

def getProducto( pUsuario , pContrasena , producto ):
    consulta = "SELECT * FROM producto WHERE producto = '" + producto + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta )
    return resultado[0]

def getProductos( pUsuario , pContrasena ):
    consulta = "SELECT * FROM Producto;"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta )
    return resultado

def getProductosBy( pUsuario , pContrasena , pProducto , pOrden ):       
    producto = utils.sqlCondicion( 'producto' , '=' , pProducto )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM producto WHERE " + producto + " " + orden;      
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario );
    resultado = consultarBD( conexion , consulta );   
    return resultado;

# ---------------------------------------- #
# ---------------- Cuenta ---------------- #
# ---------------------------------------- #

def getCuenta( pUsuario , pContrasena , pCuenta ):
    consulta = "SELECT * FROM cuenta WHERE cuenta = '" + pCuenta + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado[0]

def getCuentasBy( pUsuario , pContrasena , pCuenta , pMoneda , pPais , pOrden ):
    cuenta = utils.sqlCondicion( 'cuenta' , '=' , pCuenta )
    moneda = utils.sqlCondicion( 'moneda' , '=' , pMoneda )
    pais = utils.sqlCondicion( 'pais' , '=' , pPais )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM cuenta WHERE " + cuenta + " AND " + moneda + " AND " + pais + " " + orden    
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta ); 
    return resultado;

# ---------------------------------------- #
# ------------ Transacciones ------------- #
# ---------------------------------------- #

def getTransaccion( pUsuario , pContrasena , pFecha , pCuenta , pSubClasificacion ):
    consulta = "SELECT * FROM transaccion WHERE fecha = '" + pFecha + "' AND cuenta = '" + pCuenta + "' AND subClasificacion = '" + pSubClasificacion + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado[0]

def getTransaccionesBy( pUsuario , pContrasena , pFechaInicio , pFechaFin , pCuenta , pSubClasificacion , pOrden ):
    fechaInicio = utils.sqlCondicion( 'fecha' , '>' , pFechaInicio )
    fechaFin = utils.sqlCondicion( 'fecha' , '<' , pFechaFin )
    cuenta = utils.sqlCondicion( 'cuenta' , '=' , pCuenta )
    subClasificacion = utils.sqlCondicion( 'subClasificacion' , '=' , pSubClasificacion )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM transaccion WHERE " + fechaInicio + " AND " + fechaFin + " AND " + cuenta + " AND " + subClasificacion + " " + orden    
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );   
    return resultado;

# ---------------------------------------- #
# -------------- Transpasos -------------- #
# ---------------------------------------- #

def getTraspaso( pUsuario , pContrasena , pFecha , pOrigen , pDestino ):
    consulta = "SELECT * FROM traspaso WHERE fecha = '" + pFecha + "' AND origen = '" + pOrigen + "' AND destino = '" + pDestino + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado[0]

def getTraspasosBy( pUsuario , pContrasena , pFechaInicio , pFechaFin , pOrigen , pDestino , pOrden ):
    fechaInicio = utils.sqlCondicion( 'fecha' , '>' , pFechaInicio )
    fechaFin = utils.sqlCondicion( 'fecha' , '<' , pFechaFin )
    origen = utils.sqlCondicion( 'origen' , '=' , pOrigen )
    destino = utils.sqlCondicion( 'destino' , '=' , pDestino )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM traspaso WHERE " + fechaInicio + " AND " + fechaFin + " AND " + origen + " AND " + destino + " " + orden    
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );   
    return resultado;
       
# ---------------------------------------- #
# ------------- Aportaciones ------------- #
# ---------------------------------------- #

def getAportacion( pUsuario , pContrasena , pFecha , pCuenta , pIsin , pTipo ):
    consulta = "SELECT * FROM aportacion WHERE fecha = '" + pFecha + "' AND cuenta = '" + pCuenta + "' AND ISIN = '" + pIsin + "' AND TIPO_OPERACION = '" + pTipo + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado[0]

def getAportacionesBy( pUsuario ,  pContrasena , pFechaInicio , pFechaFin , pCuenta , pIsin , pTipo , pOrden ):
    fechaInicio = utils.sqlCondicion( 'fecha' , '>' , pFechaInicio )
    fechaFin = utils.sqlCondicion( 'fecha' , '<' , pFechaFin )
    cuenta = utils.sqlCondicion( 'cuenta' , '=' , pCuenta )
    isin = utils.sqlCondicion( 'ISIN' , '=' , pIsin )
    tipo = utils.sqlCondicion( 'TIPO_OPERACION' , '=' , pTipo )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM aportacion WHERE " + fechaInicio + " AND " + fechaFin + " AND " + cuenta + " AND " + isin + " AND " + tipo + " " + orden    
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );   
    return resultado;

# ---------------------------------------- #
# -------------- Comisiones -------------- #
# ---------------------------------------- #

def getComision( pUsuario , pContrasena , pFecha , pCuenta , pIsin , pTipo ):
    consulta = "SELECT * FROM comision WHERE fecha = '" + pFecha + "' AND cuenta = '" + pCuenta + "' AND ISIN = '" + pIsin + "' AND TIPO_OPERACION = '" + pTipo + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado[0]

def getComisionesBy( pUsuario ,  pContrasena , pFechaInicio , pFechaFin , pCuenta , pIsin , pTipo , pOrden ):
    fechaInicio = utils.sqlCondicion( 'fecha' , '>' , pFechaInicio )
    fechaFin = utils.sqlCondicion( 'fecha' , '<' , pFechaFin )
    cuenta = utils.sqlCondicion( 'cuenta' , '=' , pCuenta )
    isin = utils.sqlCondicion( 'ISIN' , '=' , pIsin )
    tipo = utils.sqlCondicion( 'TIPO_OPERACION' , '=' , pTipo )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM comision WHERE " + fechaInicio + " AND " + fechaFin + " AND " + cuenta + " AND " + isin + " AND " + tipo + " " + orden    
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );   
    return resultado;

# ---------------------------------------- #
# ------------- Clasificacion ------------ #
# ---------------------------------------- # 

def getClasificacion( pUsuario , pContrasena , pClasificacion ):
    consulta = "SELECT * FROM clasificacion WHERE clasificacion = '" + pClasificacion + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado[0]

def getClasificacionesBy( pUsuario , pContrasena , pClasificacion , pOrden ):
    clasificacion = utils.sqlCondicion( 'clasificacion' , '=' , pClasificacion )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM clasificacion WHERE " + clasificacion + " " + orden    
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );   
    return resultado; 

def getSubClasificacion( pUsuario , pContrasena , pSubClasificacion ):
    consulta = "SELECT * FROM subClasificacion WHERE subClasificacion = '" + pSubClasificacion + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado[0]

def getSubClasificacionesBy( pUsuario , pContrasena , pClasificacion , pSubClasificacion , pOrden ):
    clasificacion = utils.sqlCondicion( 'clasificacion' , '=' , pClasificacion )
    subClasificacion = utils.sqlCondicion( 'subClasificacion' , '=' , pSubClasificacion )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM subClasificacion WHERE " + clasificacion + " AND " + subClasificacion + " " + orden    
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );   
    return resultado;  

# ---------------------------------------- #
# --------------- Allocation ------------- #
# ---------------------------------------- #

def getAllocation( pUsuario , pContrasena , pAllocation ):
    consulta = "SELECT * FROM allocation WHERE allocation = '" + pAllocation + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado[0]
    
def getAllocationsBy( pUsuario , pContrasena , pAllocation , pOrden ):
    allocation = utils.sqlCondicion( 'allocation' , '=' , pAllocation )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM allocation WHERE " + allocation + " " + orden      
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );   
    return resultado;

def getAllocationsOf( pUsuario , pContrasena , pISIN , pOrden ):
    isin = utils.sqlCondicion( 'ISIN' , '=' , pISIN )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT DISTINCT allocation FROM ( subAllocation NATURAL JOIN distribucion ) WHERE " + isin + " " + orden 
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado;
    
def getSubAllocation( pUsuario , pContrasena , pSubAllocation ):
    consulta = "SELECT * FROM subAllocation WHERE subAllocation = '" + pSubAllocation + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado[0]
    
def getSubAllocationsBy( pUsuario , pContrasena , pAllocation , pSubAllocation , pOrden ):
    allocation = utils.sqlCondicion( 'allocation' , '=' , pAllocation )
    subAllocation = utils.sqlCondicion( 'subAllocation' , '=' , pSubAllocation )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT * FROM subAllocation WHERE " + allocation + " AND " + subAllocation + " " + orden     
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );   
    return resultado;

def getSubAllocationsOf( pUsuario , pContrasena , pAllocation , pISIN , pOrden ):
    allocation = utils.sqlCondicion( 'allocation' , '=' , pAllocation )
    isin = utils.sqlCondicion( 'ISIN' , '=' ,  pISIN )
    orden = utils.sqlOrderBy( pOrden )
    consulta = "SELECT DISTINCT isin , subAllocation , porcentaje FROM ( distribucion NATURAL JOIN subAllocation ) WHERE " + isin + " AND " + allocation + " " + orden 
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado;

# ---------------------------------------- #
# -------------- Distribucion ------------ #
# ---------------------------------------- #

def getIsinOfDistribucionFor( pUsuario , pContrasena , allocation ):
    consulta = "SELECT DISTINCT isin FROM ( distribucion NATURAL JOIN subAllocation ) WHERE allocation = '" + allocation + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );
    return resultado[0];
            
####################################################################    
#----------------------------- AÑADIR -----------------------------#
####################################################################

# ---------------------------------------- #
# --------------- Usuarios --------------- #
# ---------------------------------------- #
    
def anadirUsuario( pUsuario , pContrasena , nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , sal , permisos ):
    consulta = "INSERT INTO usuario ( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , sal , permisos )"
    consulta += "VALUES ( '" + nombre + "' , '" + apellido1 + "' , '" + apellido2 + "' , '" + usuario + "' , '" + DNI + "' , '" + telefono + "' , '" + email + "' , '" + password + "' , '" + sal + "' ,'" + permisos + "' );"
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# -------------- Admisiones -------------- #
# ---------------------------------------- #

def anadirAdmision( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , sal ):
    consulta =  "INSERT INTO admision ( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , sal )"
    consulta += "VALUES ( '" + nombre + "' , '" + apellido1 + "' , '" + apellido2 + "' , '" + usuario + "' , '" + DNI + "' , '" + telefono + "' , '" + email + "' , '" + password + "' , '" + sal + "' );"
    conexion = conectarBD( ADMIN_USUARIO , ADMIN_CONTRASENA , BD_USUARIO )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# ---------------- Activo ---------------- #
# ---------------------------------------- #

def anadirActivo( pUsuario , pContrasena , isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , producto , estrategia ):
    consulta = "INSERT INTO Activo ( ISIN , TIPO_PRODUCTO , TIPO_EMISOR , FUENTE , LINK , MONEDA , DESCRIPCION , COLOR , PRODUCTO , ESTRATEGIA ) "
    consulta += "VALUES ( '" + isin + "' , '" + tipo_producto + "' , '" + tipo_emisor + "' , '" + fuente + "' , '" + link + "' , '" + moneda + "' , '" + descripcion + "', '" + color + "' , '" + producto + "' , '" + estrategia + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# -------------- Estrategia -------------- #
# ---------------------------------------- #

def anadirEstrategia( pUsuario , pContrasena , estrategia , color , descripcion ):
    consulta = "INSERT INTO estrategia ( estrategia , color , descripcion ) "
    consulta += "VALUES ( '" + estrategia + "' , '" + color + "' , '" + descripcion + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
            
# ---------------------------------------- #
# -------------- Categorias -------------- #
# ---------------------------------------- #        

def anadirCategoria( pUsuario , pContrasena , categoria , color , descripcion ):
    consulta = "INSERT INTO categoria ( categoria , color , descripcion ) "
    consulta += "VALUES ( '" + categoria + "' , '" + color + "' , '" + descripcion + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )

def anadirCategorizacion( pUsuario , pContrasena , isin , categoria ):
    consulta = "INSERT INTO categorizacion ( isin , categoria ) "
    consulta += "VALUES ( '" + isin + "' , '" + categoria + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
         
# ---------------------------------------- #
# --------------- Producto --------------- #
# ---------------------------------------- #

def anadirProducto( pUsuario , pContrasena , producto , color , descripcion ):
    consulta = "INSERT INTO producto ( producto , color , descripcion ) "
    consulta += "VALUES ( '" + producto + "' , '" + color + "' , '" + descripcion + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )    

# ---------------------------------------- #
# ---------------- Cuenta ---------------- #
# ---------------------------------------- #

def anadirCuenta( pUsuario , pContrasena , cuenta , color , descripcion , moneda , pais ):
    consulta = "INSERT INTO cuenta ( cuenta , color , descripcion , moneda , pais ) "
    consulta += "VALUES ( '" + cuenta + "' , '" + color + "' , '" + descripcion + "' , '" + moneda + "' , '" + pais + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# ------------ Transacciones ------------- #
# ---------------------------------------- #

def anadirTransaccion( pUsuario , pContrasena , fecha , cuenta , clasificacion , subClasificacion , gasto , ingreso , favorita , descripcion ):
    consulta = "INSERT INTO transaccion ( cuenta , fecha , subclasificacion , gasto , ingreso , favorita , descripcion ) "
    consulta += "VALUES ( '" + cuenta + "' , '" + str(fecha) + "' , '" + subClasificacion + "' , '" + utils.floatStr( gasto ) + "' , '" + utils.floatStr( ingreso ) + "' , '" + favorita + "' , '" + descripcion + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# -------------- Transpasos -------------- #
# ---------------------------------------- #

def anadirTraspaso( pUsuario , pContrasena , fecha , origen , destino , precio , favorita , descripcion ):
    consulta = "INSERT INTO traspaso ( fecha , origen , destino , precio , favorita , descripcion ) "
    consulta += "VALUES ( '" + str(fecha) + "' , '" + origen + "' , '" + destino + "' , '" + utils.floatStr( precio ) + "' , '" + favorita + "' , '" + descripcion + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# ------------- Aportaciones ------------- #
# ---------------------------------------- #

def anadirAportacion( pUsuario , pContrasena , fecha , cuenta , isin , tipo , precio , titulos , cambio , favorita , descripcion ):
    consulta = "INSERT INTO aportacion ( isin , cuenta , fecha , precio , titulos , cambio , tipo_operacion , favorita , descripcion ) "
    consulta += "VALUES ( '" + isin + "' , '" + cuenta + "' , '" + str(fecha) + "' , '" + utils.floatStr( precio ) + "' , '" + utils.floatStr( titulos ) + "' , '" + utils.floatStr( cambio ) + "' , '" + tipo + "' , '" + favorita + "' , '" + descripcion + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# -------------- Comisiones -------------- #
# ---------------------------------------- #

def anadirComision( pUsuario , pContrasena , fecha , cuenta , tipo , isin , gasto , ingreso , favorita , descripcion ):
    consulta = "INSERT INTO comision ( isin , cuenta , fecha , gasto , ingreso , tipo_operacion , favorita , descripcion ) "
    consulta += "VALUES ( '" + isin + "' , '" + cuenta + "' , '" + str(fecha) + "' , '" + utils.floatStr( gasto ) + "' , '" + utils.floatStr( ingreso ) + "' , '" + tipo + "' , '" + favorita + "' , '" + descripcion + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# ------------- Clasificacion ------------ #
# ---------------------------------------- # 

def anadirClasificacion( pUsuario , pContrasena , clasificacion , color , descripcion ):
    consulta = "INSERT INTO clasificacion ( clasificacion , color , descripcion ) "
    consulta += "VALUES ( '" + clasificacion + "' , '" + color + "' , '" + descripcion + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )        

def anadirSubClasificacion( pUsuario , pContrasena , clasificacion , subClasificacion ):
    consulta = "INSERT INTO subClasificacion ( clasificacion , subClasificacion ) "
    consulta += "VALUES ( '" + clasificacion + "' , '" + subClasificacion + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# --------------- Allocation ------------- #
# ---------------------------------------- #
    
def anadirAllocation( pUsuario , pContrasena , allocation , descripcion ):
    consulta = "INSERT INTO allocation ( allocation , descripcion ) "
    consulta += "VALUES ( '" + allocation + "' , '" + descripcion + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
def anadirSubAllocation( pUsuario , pContrasena , allocation , subAllocation , color ):
    consulta = "INSERT INTO subAllocation ( allocation , subAllocation , color ) "
    consulta += "VALUES ( '" + allocation + "' , '" + subAllocation + "' , '" + color + "' );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# -------------- Distribucion ------------ #
# ---------------------------------------- # 

def anadirDistribucion( pUsuario , pContrasena , isin , subAllocation , porcentaje ):
    consulta = "INSERT INTO distribucion ( isin , subAllocation , porcentaje ) "
    consulta += "VALUES ( '" + isin + "' , '" + subAllocation + "' , " + porcentaje + " );"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
####################################################################    
#---------------------------- ELIMINAR ----------------------------#
####################################################################

# ---------------------------------------- #
# --------------- Usuarios --------------- #
# ---------------------------------------- #

def eliminarUsuario( pUsuario , pContrasena , usuario ):
    consulta = "DELETE FROM usuario WHERE usuario = '" + usuario + "';"
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# -------------- Admisiones -------------- #
# ---------------------------------------- #

def eliminarAdmision( pUsuario , pContrasena , usuario ):
    consulta = "DELETE FROM admision WHERE usuario = '" + usuario + "';"
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# ---------------- Activo ---------------- #
# ---------------------------------------- #

def eliminarActivo( pUsuario , pContrasena , isin ):
    consulta = "DELETE FROM activo WHERE isin = '" + isin + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# -------------- Estrategia -------------- #
# ---------------------------------------- #

def eliminarEstrategia( pUsuario , pContrasena , estrategia ):
    consulta = "DELETE FROM estrategia WHERE estrategia = '" + estrategia + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# -------------- Categorias -------------- #
# ---------------------------------------- #            

def eliminarCategoria( pUsuario , pContrasena , categoria ):
    consulta = "DELETE FROM categoria WHERE categoria = '" + categoria + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )        
       
def eliminarCategorizacion( pUsuario , pContrasena , isin , categoria ):
    consulta = "DELETE FROM categorizacion WHERE isin = '" + isin + "' AND categoria = '" + categoria + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta ) 
     
# ---------------------------------------- #
# --------------- Producto --------------- #
# ---------------------------------------- #

def eliminarProducto( pUsuario , pContrasena , producto ):
    consulta = "DELETE FROM producto WHERE producto = '" + producto + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )         

# ---------------------------------------- #
# ---------------- Cuenta ---------------- #
# ---------------------------------------- #

def eliminarCuenta( pUsuario , pContrasena , cuenta ):
    consulta = "DELETE FROM cuenta WHERE cuenta = '" + cuenta + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
             
# ---------------------------------------- #
# ------------ Transacciones ------------- #
# ---------------------------------------- #

def eliminarTransaccion( pUsuario , pContrasena , cuenta , subClasificacion , fecha ):
    consulta = "DELETE FROM transaccion WHERE cuenta = '" + cuenta + "' AND subClasificacion = '" + subClasificacion + "' AND fecha = '" + fecha + "' ;"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# -------------- Transpasos -------------- #
# ---------------------------------------- #

def eliminarTraspaso( pUsuario , pContrasena , origen , destino , fecha ):
    consulta = "DELETE FROM traspaso WHERE origen = '" + origen + "' AND destino = '" + destino + "' AND fecha = '" + fecha + "' ;"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# ------------- Aportaciones ------------- #
# ---------------------------------------- #

def eliminarAportacion( pUsuario , pContrasena , isin , cuenta , tipo_operacion , fecha ):
    consulta = "DELETE FROM aportacion WHERE isin = '" + isin + "' AND cuenta = '" + cuenta + "' AND tipo_operacion = '" + tipo_operacion + "' AND fecha = '" + fecha + "' ;"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# -------------- Comisiones -------------- #
# ---------------------------------------- #

def eliminarComision( pUsuario , pContrasena , isin , cuenta , tipo_operacion , fecha ):
    consulta = "DELETE FROM comision WHERE isin = '" + isin + "' AND cuenta = '" + cuenta + "' AND tipo_operacion = '" + tipo_operacion + "' AND fecha = '" + fecha + "' ;"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# ------------- Clasificacion ------------ #
# ---------------------------------------- # 
    
def eliminarClasificacion( pUsuario , pContrasena , clasificacion ):
    consulta = "DELETE FROM clasificacion WHERE clasificacion = '" + clasificacion + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )

def eliminarSubClasificacion( pUsuario , pContrasena , subClasificacion ):
    consulta = "DELETE FROM subClasificacion WHERE subClasificacion = '" + subClasificacion + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# --------------- Allocation ------------- #
# ---------------------------------------- #  

def eliminarAllocation( pUsuario , pContrasena , allocation ):
    consulta = "DELETE FROM allocation WHERE allocation = '" + allocation + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
  
def eliminarSubAllocation( pUsuario , pContrasena , subAllocation ):
    consulta = "DELETE FROM subAllocation WHERE subAllocation = '" + subAllocation + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# -------------- Distribucion ------------ #
# ---------------------------------------- # 
def eliminarDistribucion( pUsuario , pContrasena , isin , subAllocation ):
    consulta = "DELETE FROM distribucion WHERE isin = '" + isin + "' AND subAllocation = '" + subAllocation + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )

####################################################################    
#--------------------------- ACTUALIZAR ---------------------------#
####################################################################  

# ---------------------------------------- #
# --------------- Usuarios --------------- #
# ---------------------------------------- #

def actualizarUsuario( pUsuario , pContrasena , nombre , primerApellido , segundoApellido , dni , telefono , email ):
    consulta =  "UPDATE usuario SET nombre = '" + nombre + "' , apellido1 = '" + primerApellido + "' , apellido2 = '" + segundoApellido + "' , DNI = '" + dni + "' , telefono = '" + telefono + "' , email = '" + email + "'  "
    consulta += "WHERE usuario = '" + pUsuario + "';"
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    updateBD( conexion , consulta )    

def actualizarPermisos( pUsuario , pContrasena , usuario , permisos ):
    consulta = "UPDATE usuario SET permisos = '" + permisos + "' WHERE usuario = '" + usuario + "';";
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    updateBD( conexion , consulta )
    
def actualizarCredenciales( pUsuario , pContrasena , has , contrasena , sal ):
    consulta =  "UPDATE usuario SET password = '" + has + "' , sal = '" + sal + "' "
    consulta += "WHERE usuario = '" + pUsuario + "';"
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    updateBD( conexion , consulta )
    
    consulta = "ALTER USER '" + pUsuario + "'@'" + IP + "' IDENTIFIED BY '" + contrasena + "'; "
    conexion = conectarBD( pUsuario , pContrasena , BD_USUARIO )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# -------------- Admisiones -------------- #
# ---------------------------------------- #


# ---------------------------------------- #
# ---------------- Activo ---------------- #
# ---------------------------------------- #

def actualizarActivo( pUsuario , pContrasena , isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , producto , estrategia ):
    consulta =  "UPDATE activo SET tipo_producto = '" + tipo_producto + "' , tipo_emisor = '" + tipo_emisor + "' , fuente = '" + fuente + "' , link = '" + link + "' , moneda = '" + moneda + "' , descripcion = '" + descripcion + "' , color = '" + color + "' , producto = '" + producto + "' , estrategia = '" + estrategia + "'  "
    consulta += "WHERE isin = '" + isin + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta ) 

def actualizarCotizacionActivo( pUsuario , pContrasena , isin , cotizacion ):
    consulta =  "UPDATE activo SET precio = '" + utils.floatStr( cotizacion ) + "'  "
    consulta += "WHERE isin = '" + isin + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# -------------- Estrategia -------------- #
# ---------------------------------------- #

def actualizarEstrategia( pUsuario , pContrasena , estrategia , color , descripcion ):
    consulta =  "UPDATE estrategia SET descripcion = '" + descripcion + "' , color = '" + color + "' "
    consulta += "WHERE estrategia = '" + estrategia + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# -------------- Categorias -------------- #
# ---------------------------------------- #            

def actualizarCategoria( pUsuario , pContrasena , categoria , color , descripcion ):
    consulta =  "UPDATE categoria SET descripcion = '" + descripcion + "' , color = '" + color + "' "
    consulta += "WHERE categoria = '" + categoria + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
                   
# ---------------------------------------- #
# --------------- Producto --------------- #
# ---------------------------------------- #

def actualizarProducto( pUsuario , pContrasena , producto , color , descripcion ):
    consulta =  "UPDATE producto SET descripcion = '" + descripcion + "' , color = '" + color + "' "
    consulta += "WHERE producto = '" + producto + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )       

# ---------------------------------------- #
# ---------------- Cuenta ---------------- #
# ---------------------------------------- #

def actualizarCuenta( pUsuario , pContrasena , cuenta , color , descripcion , moneda , pais ):
    consulta =  "UPDATE cuenta SET descripcion = '" + descripcion + "' , color = '" + color + "' , moneda = '" + moneda + "' , pais = '" + pais + "' "
    consulta += "WHERE cuenta = '" + cuenta + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
         
# ---------------------------------------- #
# ------------ Transacciones ------------- #
# ---------------------------------------- #

def actualizarTransaccion( pUsuario , pContrasena , cuenta , subClasificacion , fecha , gasto , ingreso , favorita , descripcion ):
    consulta =  "UPDATE transaccion SET descripcion = '" + descripcion + "' , favorita = '" + favorita + "' , ingreso = '" + utils.floatStr( ingreso ) + "' , gasto = '" + utils.floatStr( gasto ) + "' "
    consulta += "WHERE cuenta = '" + cuenta + "' AND subClasificacion = '" + subClasificacion + "' AND fecha = '" + fecha + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# -------------- Transpasos -------------- #
# ---------------------------------------- #

def actualizarTraspaso( pUsuario , pContrasena , origen , destino , fecha , precio , favorita , descripcion ):
    consulta =  "UPDATE traspaso SET descripcion = '" + descripcion + "' , favorita = '" + favorita + "' , precio = '" + utils.floatStr( precio ) + "' "
    consulta += "WHERE origen = '" + origen + "' AND destino = '" + destino + "' AND fecha = '" + fecha + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# ------------- Aportaciones ------------- #
# ---------------------------------------- #

def actualizarAportacion( pUsuario , pContrasena , isin , cuenta , fecha , precio , titulos , cambio , tipo_operacion , favorita , descripcion ):
    consulta =  "UPDATE aportacion SET descripcion = '" + descripcion + "' , favorita = '" + favorita + "' , precio = '" + utils.floatStr( precio ) + "' , titulos = '" + utils.floatStr( titulos ) + "' , cambio = '" + utils.floatStr( cambio ) + "' "
    consulta += "WHERE cuenta = '" + cuenta + "' AND isin = '" + isin + "' AND fecha = '" + fecha + "' AND tipo_operacion = '" + tipo_operacion + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
 
# ---------------------------------------- #
# -------------- Comisiones -------------- #
# ---------------------------------------- #

def actualizarComision( pUsuario , pContrasena , isin , cuenta , fecha , gasto , ingreso , tipo_operacion , favorita , descripcion ):
    consulta =  "UPDATE comision SET descripcion = '" + descripcion + "' , favorita = '" + favorita + "' , gasto = '" + utils.floatStr( gasto ) + "' , ingreso = '" + utils.floatStr( ingreso ) + "' " 
    consulta += "WHERE cuenta = '" + cuenta + "' AND isin = '" + isin + "' AND fecha = '" + fecha + "' AND tipo_operacion = '" + tipo_operacion + "';"
    print(consulta)
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
 
# ---------------------------------------- #
# ------------- Clasificacion ------------ #
# ---------------------------------------- # 

def actualizarClasificacion( pUsuario , pContrasena , clasificacion , color , descripcion ):
    consulta =  "UPDATE clasificacion SET descripcion = '" + descripcion + "' , color = '" + color + "' "
    consulta += "WHERE clasificacion = '" + clasificacion + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )  

def actualizarSubClasificacion( pUsuario , pContrasena , pClasificacion , subClasificacion ):
    consulta =  "UPDATE subClasificacion SET clasificacion = '" + pClasificacion + "' "
    consulta += "WHERE subClasificacion = '" + subClasificacion + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
# ---------------------------------------- #
# --------------- Allocation ------------- #
# ---------------------------------------- #

def actualizarAllocation( pUsuario , pContrasena , allocation , descripcion ):
    consulta =  "UPDATE allocation SET descripcion = '" + descripcion + "' "
    consulta += "WHERE allocation = '" + allocation + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
def actualizarSubAllocation( pUsuario , pContrasena , pAllocation , subAllocation , color ):
    if pAllocation == '': allocation = ''
    else: allocation = " , allocation = '" + pAllocation + "' "
    consulta =  "UPDATE subAllocation SET color = '" + color + "' " + allocation
    consulta += "WHERE subAllocation = '" + subAllocation + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )

# ---------------------------------------- #
# -------------- Distribucion ------------ #
# ---------------------------------------- # 

def actualizarDistribucion( pUsuario , pContrasena , isin , subAllocation , porcentaje ):   
    consulta =  "UPDATE distribucion SET porcentaje = '" + porcentaje + "' "
    consulta += "WHERE subAllocation = '" + subAllocation + "' AND isin = '" + isin + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    updateBD( conexion , consulta )
    
####################################################################    
#---------------------------- COMPROBAR ---------------------------#
####################################################################

# ---------------------------------------- #
# --------------- Usuarios --------------- #
# ---------------------------------------- #

def existeUsuario( pUsuario ):
    consulta = "SELECT usuario FROM usuario WHERE usuario = '" + pUsuario + "';"
    conexion = conectarBD( ADMIN_USUARIO , ADMIN_CONTRASENA , BD_USUARIO );
    return existeBD( conexion , consulta )

def contrasenaCorrecta( usuario , contrasena ):
    consulta = "SELECT usuario FROM usuario WHERE usuario = '" + usuario + "' AND password = '" + contrasena + "' ;"
    conexion = conectarBD( ADMIN_USUARIO , ADMIN_CONTRASENA , BD_USUARIO )
    return existeBD( conexion , consulta )

# ---------------------------------------- #
# -------------- Admisiones -------------- #
# ---------------------------------------- #

def existeAdmision( pUsuario ):   
    consulta = "SELECT usuario FROM admision WHERE usuario = '" + pUsuario + "';"
    conexion = conectarBD( ADMIN_USUARIO , ADMIN_CONTRASENA , BD_USUARIO )
    return existeBD( conexion , consulta )

# ---------------------------------------- #
# ---------------- Activo ---------------- #
# ---------------------------------------- #

def existeActivo( pUsuario , pContrasena , isin ):   
    consulta = "SELECT isin FROM activo WHERE isin = '" + isin + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    return existeBD( conexion , consulta )

# ---------------------------------------- #
# --------------- Producto --------------- #
# ---------------------------------------- #


# ---------------------------------------- #
# -------------- Estrategia -------------- #
# ---------------------------------------- #


# ---------------------------------------- #
# ---------------- Cuenta ---------------- #
# ---------------------------------------- #

def existeCuenta( pUsuario , pContrasena , cuenta ): 
    consulta = "SELECT cuenta FROM cuenta WHERE cuenta = '" + cuenta + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    return existeBD( conexion , consulta )

# ---------------------------------------- #
# ------------ Transacciones ------------- #
# ---------------------------------------- #

def existeTransaccion( pUsuario , pContrasena , fecha , cuenta , subClasificacion ):
    consulta = "SELECT cuenta FROM transaccion WHERE cuenta = '" + cuenta + "' and fecha = '" + str(fecha) + "' and subclasificacion = '" + subClasificacion + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    return existeBD( conexion , consulta )       
        

# ---------------------------------------- #
# -------------- Transpasos -------------- #
# ---------------------------------------- #

def existeTraspaso( pUsuario , pContrasena , fecha , origen , destino ):
    consulta = "SELECT origen FROM traspaso WHERE origen = '" + origen + "' and fecha = '" + str(fecha) + "' and destino = '" + destino + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    return existeBD( conexion , consulta )
            
# ---------------------------------------- #
# ------------- Aportaciones ------------- #
# ---------------------------------------- #

def existeAportacion( pUsuario , pContrasena , fecha , cuenta , isin , tipo ):  
    consulta = "SELECT isin FROM aportacion WHERE cuenta = '" + cuenta + "' and fecha = '" + str(fecha) + "' and isin = '" + isin + "' and tipo_operacion = '" + tipo + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    return existeBD( conexion , consulta )

# ---------------------------------------- #
# -------------- Comisiones -------------- #
# ---------------------------------------- #

def existeComision( pUsuario , pContrasena , fecha , cuenta , isin , tipo ):
    consulta = "SELECT isin FROM comision WHERE cuenta = '" + cuenta + "' and fecha = '" + str(fecha) + "' and isin = '" + isin + "' and tipo_operacion = '" + tipo + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    return existeBD( conexion , consulta )

# ---------------------------------------- #
# ------------- Clasificacion ------------ #
# ---------------------------------------- #

def existeClasificacion( pUsuario , pContrasena , clasificacion , subClasificacion ):
    consulta = "SELECT subclasificacion FROM subclasificacion WHERE subclasificacion = '" + subClasificacion + "' and clasificacion = '" + clasificacion + "';"
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    return existeBD( conexion , consulta )
    
# ---------------------------------------- #
# --------------- Allocation ------------- #
# ---------------------------------------- #

####################################################################    
#----------------------------- CALCULAR ---------------------------#
####################################################################

# ---------------------------------------- #
# --------------- Activos ---------------- #
# ---------------------------------------- #

# ---------------------------------------- #
# ------------ Transacciones ------------- #
# ---------------------------------------- #

def calcularTransacciones( pUsuario , pContrasena , pCuenta , pFechaInicio , pFechaFin , pSubClasificacion ):
    fechaInicio = utils.sqlCondicion( 'fecha' , '>' , pFechaInicio )
    fechaFin = utils.sqlCondicion( 'fecha' , '<' , pFechaFin )
    cuenta = utils.sqlCondicion( 'cuenta' , '=' , pCuenta )
    subClasificacion = utils.sqlCondicion( 'subClasificacion' , '=' , pSubClasificacion )
    consulta = "SELECT gasto , ingreso FROM transaccion WHERE " + fechaInicio + " AND " + fechaFin + " AND " + cuenta + " AND " + subClasificacion  
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );   
    return resultado;

# ---------------------------------------- #
# -------------- Transpasos -------------- #
# ---------------------------------------- #

def calcularTraspasos( pUsuario , pContrasena , queCuenta , pCuenta , pFechaInicio , pFechaFin ):
    fechaInicio = utils.sqlCondicion( 'fecha' , '>' , pFechaInicio )
    fechaFin = utils.sqlCondicion( 'fecha' , '<' , pFechaFin )
    cuenta = utils.sqlCondicion( queCuenta , '=' , pCuenta )
    consulta = "SELECT precio FROM traspaso WHERE " + fechaInicio + " AND " + fechaFin + " AND " + cuenta  
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta ); 
    return resultado;

# ---------------------------------------- #
# ------------- Aportaciones ------------- #
# ---------------------------------------- #

# ---------------------------------------- #
# -------------- Comisiones -------------- #
# ---------------------------------------- #

def calcularComisiones( pUsuario , pContrasena , pCuenta , pFechaInicio , pFechaFin , pTipo ):
    fechaInicio = utils.sqlCondicion( 'fecha' , '>' , pFechaInicio )
    fechaFin = utils.sqlCondicion( 'fecha' , '<' , pFechaFin )
    cuenta = utils.sqlCondicion( 'cuenta' , '=' , pCuenta )
    tipo = utils.sqlCondicion( 'TIPO_OPERACION' , '=' , pTipo )
    consulta = "SELECT gasto , ingreso ingresos FROM comision WHERE " + fechaInicio + " AND " + fechaFin + " AND " + cuenta + " AND " + tipo    
    conexion = conectarBD( pUsuario , pContrasena , "BD_" + pUsuario )
    resultado = consultarBD( conexion , consulta );  
    return resultado;
    
    