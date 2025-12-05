# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta

from app import Seccion as secciones
from lib import SQL as sql
from lib import Utils as utils
from lib import Finanzas as finanzas

####################################################################    
#------------------------------ Sesion ----------------------------#
####################################################################

class Sesion:
    
    instancia = None
    
    def __new__( cls ):
        if not Sesion.instancia:
            Sesion.instancia = Sesion.__Sesion( )
        return Sesion.instancia
        
    class __Sesion:
        
        def __init__( self ):
            self.usuario = ""
            self.permisos = 0
            self.contrasena = ""
            self.tiempo_inicio = ""
            self.tiempo_permitido = 10
            
        # ---------------------------------------- #
        # ---------------- Sesion ---------------- #
        # ---------------------------------------- #
        
        def iniciarSesion( self , pUsuario , pContraseña ):
            if( self.comprobarCredenciales( pUsuario , pContraseña ) ):
                sesionIniciada = True
                self.usuario = pUsuario
                self.contrasena = pContraseña
                self.permisos = sql.getPermisos( pUsuario , pContraseña )
                self.tiempo_inicio = datetime.now()
                # TODO Descomentar
                # finanzas.actualizarCotizaciones()
                # TODO registrar los intentos de acceso
                # print ("nuevo usuario " + self.usuario + " como " + str(self.permisos) )
                secciones.Secciones().generarRedireccion( 'Principal' )
            else:
                sesionIniciada = False
                print ("TODO - Añadir el intento de acceso")
                secciones.Secciones().generarRedireccion( 'InicioSesion' )
            return sesionIniciada
        
        
        def cerrarSesion( self ):
            secciones.Secciones().generarRedireccion( 'InicioSesion' )
            self.cerrarSesionConf( )
            
        def cerrarSesionConf( self ):
            self.usuario = ""
            self.permisos = 0
            self.contrasena = ""
            self.tiempo_inicio = ""
        
        # ---------------------------------------- #
        # ---------------- Anadir ---------------- #
        # ---------------------------------------- #
        
        # --------------- Usuario ---------------- #
        
        def anadirAdmision( self , pUsuario , pNombre , pPrimerApellido , pSegundoApellido , pDNI , pTelefono , pEmail , pContrasena , pContraseñaRPT , pCondiciones ):            
            admision = self.comprobarAdmision( pUsuario , pNombre , pPrimerApellido , pSegundoApellido , pDNI , pTelefono , pEmail , pContrasena , pContraseñaRPT , pCondiciones )             
            if admision:
                sal = utils.generarSal( )
                has = utils.getHash( pContrasena + sal )
                sql.anadirAdmision( pNombre , pPrimerApellido , pSegundoApellido , pUsuario , pDNI , pTelefono , pEmail , has , sal )
                sql.crearUsuarioBD( pUsuario , pContrasena )
                secciones.Secciones().reportarError( "El usuario " + pUsuario + " ha sido añadido correctamente a la lista de admisiones " )
                secciones.Secciones().generarRedireccion( 'InicioSesion' )
            else: secciones.Secciones().generarRedireccion( 'Registro' )              
            return admision
        
        
        def anadirUsuario( self , pUsuario , pPermisos ):
            nombre , primerApellido , segundoApellido , usuario , DNI , telefono , email , contrasena , sal = self.getAdmision( pUsuario )
            sql.crearBD( self.usuario , self.contrasena , pUsuario )
            #sql.asignarPermisosUsuarioBD( pUsuario , pPermisos )
            sql.anadirUsuario( self.usuario , self.contrasena , nombre , primerApellido , segundoApellido , usuario , DNI , telefono , email , contrasena , sal , pPermisos )
            secciones.Secciones().reportarError( "El usuario " + pUsuario + " ha sido añadido correctamente a la lista de usuarios " )
            return True

        # --------------- Activos ---------------- #
        
        def anadirActivo( self , isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , producto , estrategia ):
            sql.anadirActivo( self.usuario , self.contrasena , isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , producto , estrategia )
        
        # ------------- Estrategias -------------- #
        
        def anadirEstrategia( self , estrategia , color , descripcion ):
            sql.anadirEstrategia( self.usuario , self.contrasena , estrategia , color , descripcion )
            
        # -------------- Categorias -------------- #
        
        def anadirCategoria( self , categoria , color , descripcion ):
            sql.anadirCategoria( self.usuario , self.contrasena , categoria , color , descripcion )
        
        def anadirCategorizacion( self , isin , categoria ):
            sql.anadirCategorizacion( self.usuario , self.contrasena , isin , categoria )
            
        # -------------- Productos --------------- #
        
        def anadirProducto( self , producto , color , descripcion ):
            sql.anadirProducto( self.usuario , self.contrasena , producto , color , descripcion )
                
        # --------------- Cuentas ---------------- #
        
        def anadirCuenta( self , cuenta , color , descripcion , moneda , pais ):
            sql.anadirCuenta( self.usuario , self.contrasena , cuenta , color , descripcion , moneda , pais )
       
        # ------------ Transacciones ------------- #
   
        def anadirTransaccion( self , fecha , cuenta , clasificacion , subClasificacion , gasto , ingreso , favorita , descripcion ):
            sql.anadirTransaccion( self.usuario , self.contrasena , fecha , cuenta , clasificacion , subClasificacion , gasto , ingreso , favorita , descripcion )
              
        # -------------- Transpasos -------------- #

        def anadirTraspaso( self , fecha , origen , destino , precio , favorita , descripcion ):
            sql.anadirTraspaso( self.usuario , self.contrasena , fecha , origen , destino , precio , favorita , descripcion )
            
        # ------------- Aportaciones ------------- #

        def anadirAportacion( self , fecha , cuenta , isin , tipo , precio , titulos , cambio , favorita , descripcion ):          
            sql.anadirAportacion( self.usuario , self.contrasena , fecha , cuenta , isin , tipo , precio , titulos , cambio , favorita , descripcion )

        # -------------- Comisiones -------------- #

        def anadirComision( self , fecha , cuenta , tipo , isin , gasto , ingreso , favorita , descripcion ):
            sql.anadirComision( self.usuario , self.contrasena , fecha , cuenta , tipo , isin , gasto , ingreso , favorita , descripcion )
         
        # ------------- Clasificacion ------------ #
 
        def anadirClasificacion( self , clasificacion , color , descripcion ):
            sql.anadirClasificacion( self.usuario , self.contrasena , clasificacion , color , descripcion )
        
        def anadirSubClasificacion( self , clasificacion , subClasificacion ):
            sql.anadirSubClasificacion( self.usuario , self.contrasena , clasificacion , subClasificacion )
    
        # --------------- Allocation ------------- #
                
        def anadirAllocation( self , allocation , descripcion ):
            sql.anadirAllocation( self.usuario , self.contrasena , allocation , descripcion )
        
        def anadirSubAllocation( self , allocation , subAllocation , color ):
            sql.anadirSubAllocation( self.usuario , self.contrasena , allocation , subAllocation , color )
            isins = self.getIsinOfDistribucionFor( allocation )
            print('isins --> ',isins)
            for isin in isins:
                self.anadirDistribucion( isin , subAllocation , 0 )
            
        # --------------- Distribucion ------------- #
        
        def anadirDistribucion( self , isin , subAllocation , porcentaje ):
            sql.anadirDistribucion( self.usuario , self.contrasena , isin , subAllocation , utils.floatStr(porcentaje) )
                
        # ---------------------------------------- #
        # --------------- Eliminar --------------- #
        # ---------------------------------------- #
        
        # --------------- Usuario ---------------- #
        
        def eliminarUsuario( self , pUsuario , pPermisos ):
            if self.comprobarPermisos( ">=" , pPermisos ):
                if pUsuario == "": usuario = self.usuario
                else: usuario = pUsuario
                sql.eliminarUsuario( self.usuario , self.contrasena , usuario )
                sql.eliminarBD( self.usuario , self.contrasena , usuario )
                if pUsuario == "": self.cerrarSesion()
            else: 
                mensaje = "Solo puedes eliminar aquellos usuarios que tengan menor rango que tu"
                secciones.Secciones().reportarError( mensaje )               
             
        def eliminarAdmision( self , pUsuario ):
            sql.eliminarAdmision( self.usuario , self.contrasena , pUsuario )
        
        # --------------- Activos ---------------- #
        
        def eliminarActivo( self , isin ):
            sql.eliminarActivo( self.usuario , self.contrasena , isin )
            
        # ------------- Estrategias -------------- #
        
        def eliminarEstrategia( self , estrategia ):
            sql.eliminarEstrategia( self.usuario , self.contrasena , estrategia )
            
        # -------------- Categorias -------------- #
        
        def eliminarCategoria( self , categoria ):
            sql.eliminarCategoria( self.usuario , self.contrasena , categoria )
        
        def eliminarCategorizacion( self , isin , categoria ):
            sql.eliminarCategorizacion( self.usuario , self.contrasena , isin , categoria )
            
        # -------------- Productos --------------- #
        
        def eliminarProducto( self , producto ):
            sql.eliminarProducto( self.usuario , self.contrasena , producto )
        
        # --------------- Cuentas ---------------- #
        
        def eliminarCuenta( self , cuenta ):
            sql.eliminarCuenta( self.usuario , self.contrasena , cuenta )
        
        # ------------ Transacciones ------------- #

        def eliminarTransaccion( self , cuenta , subClasificacion , fecha ):
            sql.eliminarTransaccion( self.usuario , self.contrasena , cuenta , subClasificacion , fecha )
    
        # -------------- Transpasos -------------- #

        def eliminarTraspaso( self , origen , destino , fecha ):
            sql.eliminarTraspaso( self.usuario , self.contrasena , origen , destino , fecha )

        # ------------- Aportaciones ------------- #

        def eliminarAportacion( self , isin , cuenta , tipo_operacion , fecha ):
           sql.eliminarAportacion( self.usuario , self.contrasena , isin , cuenta , tipo_operacion , fecha )
    
        # -------------- Comisiones -------------- #

        def eliminarComision( self , isin , cuenta , tipo_operacion , fecha ):
           sql.eliminarComision( self.usuario , self.contrasena , isin , cuenta , tipo_operacion , fecha )

        # ------------- Clasificacion ------------ #
        
        def eliminarClasificacion( self , clasificacion ):
            sql.eliminarClasificacion( self.usuario , self.contrasena , clasificacion )
        
        def eliminarSubClasificacion( self , subClasificacion ):
            sql.eliminarSubClasificacion( self.usuario , self.contrasena , subClasificacion )
    
        # --------------- Allocation ------------- #
        
        def eliminarAllocation( self , allocation ):
            sql.eliminarAllocation( self.usuario , self.contrasena , allocation )
        
        def eliminarSubAllocation( self , subAllocation ):
            sql.eliminarSubAllocation( self.usuario , self.contrasena , subAllocation )
        
        # --------------- Distribucion ------------- #
        
        def eliminarDistribucion( self , isin , subAllocation ):
            sql.eliminarDistribucion( self.usuario , self.contrasena , isin , subAllocation )
              
        # ---------------------------------------- #
        # -------------- Actualizar -------------- #
        # ---------------------------------------- #
        
        # --------------- Usuario ---------------- #
         
        def actualizarCredenciales( self , pContrasenaAntigua , pConraseñaNueva , pContrasenaNuevaRPT ):
            actualizacion = True
            mensaje = "*"
            if pConraseñaNueva != pContrasenaNuevaRPT:
                actualizacion = False
                mensaje += " *  Los campos de la nueva contraseña deben coincidir <br /> "
            if not self.comprobarContrasena( self.usuario , pContrasenaAntigua ): 
                actualizacion = False
                mensaje += " *  La contraseña antigua no es correcta <br /> "          
            if actualizacion: 
                mensaje = "La contraseña ha sido correctamente modificada"
                self.actualizarContraseña( pConraseñaNueva )
            secciones.Secciones().reportarError( mensaje ) 
            return actualizacion
            
        
        def actualizarContraseña( self , pContrasena ):
            sal = utils.generarSal( )
            has = utils.getHash( pContrasena + sal )
            sql.actualizarCredenciales( self.usuario , self.contrasena , has , pContrasena , sal )
            self.contrasena = pContrasena
        
        
        def actualizarUsuario( self , nombre , primerApellido , segundoApellido , dni , telefono , email ):
            sql.actualizarUsuario( self.usuario , self.contrasena , nombre , primerApellido , segundoApellido , dni , telefono , email )
        
        
        def actualizarPermisos( self , pUsuario , pPermisos , pNuevosPermisos ):
            if self.comprobarPermisos( ">" , pPermisos ):
                sql.actualizarPermisos( self.usuario , self.contrasena , pUsuario , pNuevosPermisos )
            else: 
                mensaje = "Solo puedes modificar los permisos de aquellos usuarios que tengan menor rango que tu"
                secciones.Secciones().reportarError( mensaje ) 
        
        # --------------- Activos ---------------- #
        
        def actualizarActivo( self , isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , producto , estrategia ):
            sql.actualizarActivo( self.usuario , self.contrasena , isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , producto , estrategia )
            
        def actualizarCotizacionActivo( self , isin , cotizacion ):
            sql.actualizarCotizacionActivo( self.usuario , self.contrasena , isin , cotizacion )
            
        # ------------- Estrategias -------------- #
        
        def actualizarEstrategia( self , estrategia , color , descripcion ):
            sql.actualizarEstrategia( self.usuario , self.contrasena , estrategia , color , descripcion )
            
        # -------------- Categorias -------------- #
        
        def actualizarCategoria( self , categoria , color , descripcion ):
            sql.actualizarCategoria( self.usuario , self.contrasena , categoria , color , descripcion )
            
        # -------------- Productos --------------- #
        
        def actualizarProducto( self , producto , color , descripcion ):
            sql.actualizarProducto( self.usuario , self.contrasena , producto , color , descripcion )
                    
        # --------------- Cuentas ---------------- #
        
        def actualizarCuenta( self , cuenta , color , descripcion , moneda , pais ):
            sql.actualizarCuenta( self.usuario , self.contrasena , cuenta , color , descripcion , moneda , pais )
        
        # ------------ Transacciones ------------- #

        def actualizarTransaccion( self , cuenta , subClasificacion , fecha , gasto , ingreso , favorita , descripcion ):
            sql.actualizarTransaccion( self.usuario , self.contrasena , cuenta , subClasificacion , fecha , gasto , ingreso , favorita , descripcion )
            
        # -------------- Transpasos -------------- #

        def actualizarTraspaso( self , origen , destino , fecha , precio , favorita , descripcion ):
            sql.actualizarTraspaso( self.usuario , self.contrasena , origen , destino , fecha , precio , favorita , descripcion )
      
        # ------------- Aportaciones ------------- #

        def actualizarAportacion( self , isin , cuenta , fecha , precio , titulos , cambio , tipo_operacion , favorita , descripcion ):
            sql.actualizarAportacion( self.usuario , self.contrasena , isin , cuenta , fecha , precio , titulos , cambio , tipo_operacion , favorita , descripcion )
         
        # -------------- Comisiones -------------- #

        def actualizarComision( self , isin , cuenta , fecha , gasto , ingreso , tipo_operacion , favorita , descripcion ):
            sql.actualizarComision( self.usuario , self.contrasena , isin , cuenta , fecha , gasto , ingreso , tipo_operacion , favorita , descripcion )
   
        # ------------- Clasificacion ------------ #
 
        def actualizarClasificacion( self , clasificacion , color , descripcion ):
            sql.actualizarClasificacion( self.usuario , self.contrasena , clasificacion , color , descripcion )
        
        def actualizarSubClasificacion( self , clasificacion , subClasificacion ):
            sql.actualizarSubClasificacion( self.usuario , self.contrasena , clasificacion , subClasificacion )

        # --------------- Allocation ------------- #
        
        def actualizarAllocation( self , allocation , descripcion ):
            sql.actualizarAllocation( self.usuario , self.contrasena , allocation , descripcion )
        
        def actualizarSubAllocation( self , allocation , subAllocation , color ):
            sql.actualizarSubAllocation( self.usuario , self.contrasena , allocation , subAllocation , color )
        
        # --------------- Distribucion ------------- #
        
        def actualizarDistribucion( self , isin , subAllocation , porcentaje ):
            sql.actualizarDistribucion( self.usuario , self.contrasena , isin , subAllocation , utils.floatStr(porcentaje) )
            
        # ---------------------------------------- #
        # --------------- Comprobar -------------- #
        # ---------------------------------------- #
        
        def comprobarPermisos( self , pEstricto , pPermisos ):
            validacion = False
            if pEstricto == "=":  validacion = ( self.permisos == pPermisos )
            if pEstricto == ">":  validacion = ( self.permisos >  pPermisos )
            if pEstricto == "<":  validacion = ( self.permisos <  pPermisos )
            if pEstricto == ">=": validacion = ( self.permisos >= pPermisos )
            if pEstricto == "<=": validacion = ( self.permisos <= pPermisos )
            # print( "Permisos Usuario: " , self.permisos , pEstricto ,  "Permisos Pagina" , pPermisos , "Validacion:" , validacion)
            return validacion
            
         
        def comprobarTiempoSesion( self ):
            tiempo_maximo = self.tiempo_inicio + timedelta( minutes = self.tiempo_permitido )
            caducado = False
            if datetime.now() > tiempo_maximo: 
                caducado = True
                self.cerrarSesionConf( )
            else: self.tiempo_inicio = datetime.now()
            return caducado
        
        
        def comprobarSesionIniciada( self ):
            sesionIniciada = False
            if self.usuario != "": sesionIniciada = True
            return sesionIniciada
        
        
        def comprobarContrasena( self , pUsuario , pContrasena ):
            credenciales = False
            sal = sql.getSal( pUsuario )
            has = utils.getHash( pContrasena + sal )
            if sql.contrasenaCorrecta( pUsuario , has ): credenciales = True
            return credenciales
        
        
        def comprobarCredenciales( self , pUsuario , pContrasena ):         
            if sql.existeAdmision( pUsuario ):
                credenciales = False
                mensaje = " El usuario " + pUsuario + " está pendiente de admisión"              
            elif not sql.existeUsuario( pUsuario ):
                credenciales = False
                mensaje = " El usuario " + pUsuario + " no está registrado"             
            elif not self.comprobarContrasena( pUsuario , pContrasena ):
                credenciales = False
                mensaje = " La contraseña para " + pUsuario + " no es correcta"               
            else:
                credenciales = True
                mensaje = ""
            secciones.Secciones().reportarError( mensaje )
            return credenciales
                

        def comprobarAdmision( self , pUsuario , pNombre , pPrimerApellido , pSegundoApellido , pDNI , pTelefono , pEmail , pContrasena , pContraseñaRPT , pCondiciones ):
            admision = True
            mensaje = ''
            print( pUsuario , pNombre , pPrimerApellido , pSegundoApellido , pDNI , pTelefono , pEmail , pContrasena , pContraseñaRPT , pCondiciones )
            if pContrasena != pContraseñaRPT:
                print( "contraseñas no coinciden" )
                mensaje += " *  Las contraseñas no coinciden <br />"
                admision = False;
            if sql.existeUsuario( pUsuario ):
                print( "usuario existe" )
                mensaje += " *  Ese usuario ya existe <br />"
                admision = False;
            if sql.existeAdmision( pUsuario ):
                print( "admision existe" )
                mensaje += " *  Ese usuario está pendiente de admisión <br />"
                admision = False;
            if not pCondiciones:
                print( "no acepta condiciones" )
                mensaje += " *  Debe aceptar las condiciones de uso <br />"
                admision = False;
            if mensaje != '': secciones.Secciones().reportarError( mensaje )
            return admision

        # ---------------------------------------- #
        # ---------------- Existe ---------------- #
        # ---------------------------------------- #
        
        def existeCuenta( self , pCuenta ):
            return sql.existeCuenta( self.usuario , self.contrasena , pCuenta )
            
        def existeActivo( self , pIsin ):
            return sql.existeActivo( self.usuario , self.contrasena , pIsin )
        
        def existeAportacion( self , pFecha , pCuenta , pIsin , pTipo ):
            return sql.existeAportacion( self.usuario , self.contrasena , pFecha , pCuenta , pIsin , pTipo )
          
        def existeComision( self , pFecha , pCuenta , pIsin , pTipo ):
            return sql.existeComision( self.usuario , self.contrasena , pFecha , pCuenta , pIsin , pTipo )
 
        def existeTransaccion( self , pFecha , pCuenta , pSubClasificacion ):
            return sql.existeTransaccion( self.usuario , self.contrasena , pFecha , pCuenta , pSubClasificacion )
                       
        def existeTraspaso( self , pFecha , pOrigen , pDestino ):
            return sql.existeTraspaso( self.usuario , self.contrasena , pFecha , pOrigen , pDestino )
               
        def existeClasificacion( self , pClasificacion , pSubClasificacion ):
            return sql.existeClasificacion( self.usuario , self.contrasena , pClasificacion , pSubClasificacion )
        
        # ---------------------------------------- #
        # ------------- Desencriptar ------------- #
        # ---------------------------------------- #
        
        # --------------- Usuario ---------------- #
        
        def getUsuario( self , pUsuario ):
            if pUsuario == "": usuario = sql.getUsuario( self.usuario , self.contrasena , self.usuario )
            else: usuario = sql.getUsuario( self.usuario , self.contrasena , pUsuario )
            return usuario

        def getUsuarios( self ):
            return sql.getUsuarios( self.usuario , self.contrasena )
        
        def getUsuariosBy( self , pUsuario , pDNI , pNombre , pApellido1 , pApellido2 , pPermisos , orden ):
            return sql.getUsuariosBy( self.usuario , self.contrasena , pUsuario , pDNI , pNombre , pApellido1 , pApellido2 , pPermisos , orden )
        
        # --------------- Admision ---------------- #
        
        def getAdmision( self , pUsuario ):
            return sql.getAdmision( self.usuario , self.contrasena , pUsuario )

        def getAdmisiones( self ):
            return sql.getAdmisiones( self.usuario , self.contrasena )
        
        def getAdmisionesBy( self , pUsuario , pDNI , pNombre , pApellido1 , pApellido2 , pOrden ):
            return sql.getAdmisionesBy( self.usuario , self.contrasena , pUsuario , pDNI , pNombre , pApellido1 , pApellido2 , pOrden )
        
        # --------------- Activos ---------------- #
        
        def getActivo( self , pISIN ):
            return sql.getActivo( self.usuario , self.contrasena , pISIN )
            
        def getActivos( self ):
            return sql.getActivos( self.usuario , self.contrasena )
        
        def getActivosBy( self , isin , producto , estrategia , orden ):
            return sql.getActivosBy( self.usuario , self.contrasena , isin , producto , estrategia , orden )
        
        # --------------- Estrategias ---------------- #
        
        def getEstrategia( self , estrategia ):
            return sql.getEstrategia( self.usuario , self.contrasena , estrategia )
        
        def getEstrategias( self ):
            return sql.getEstrategias( self.usuario , self.contrasena )
        
        def getEstrategiasBy( self , pEstrategia , pOrden ):
            return sql.getEstrategiasBy( self.usuario , self.contrasena , pEstrategia , pOrden )
 
        # -------------- Categorias -------------- #
        
        def getCategoria( self , categoria ):
            return sql.getCategoria( self.usuario , self.contrasena , categoria )
        
        def getCategorias( self ):
            return sql.getCategorias( self.usuario , self.contrasena )
        
        def getCategoriasBy( self , pCategoria , pOrden ):
            return sql.getCategoriasBy( self.usuario , self.contrasena , pCategoria , pOrden )
        
        def getCategorizacionesBy( self , isin , orden ):
            return sql.getCategorizacionesBy( self.usuario , self.contrasena  , isin , orden )
        
        # --------------- Productos ---------------- #

        def getProducto( self , producto ):
            return sql.getProducto( self.usuario , self.contrasena , producto )
        
        def getProductos( self ):
            return sql.getProductos( self.usuario , self.contrasena )
        
        def getProductosBy( self , pProducto , pOrden ):
            return sql.getProductosBy( self.usuario , self.contrasena , pProducto , pOrden )
        
        # --------------- Cuentas ---------------- #
        
        def getCuenta( self , cuenta ):
            return sql.getCuenta( self.usuario , self.contrasena , cuenta )
        
        def getCuentasBy( self , cuenta , moneda , pais , orden ):
            return sql.getCuentasBy( self.usuario , self.contrasena , cuenta , moneda , pais , orden )

        # ------------ Transacciones ------------- #

        def getTransaccion( self , fecha , cuenta , subClasificacion ):
            return sql.getTransaccion( self.usuario , self.contrasena , fecha , cuenta , subClasificacion )
        
        def getTransaccionesBy( self , fechaInicio , fechaFin , cuenta , subClasificacion , orden ):
            return sql.getTransaccionesBy( self.usuario , self.contrasena , fechaInicio , fechaFin , cuenta , subClasificacion , orden )

        # -------------- Transpasos -------------- #

        def getTraspaso( self , fecha , origen , destino ):
            return sql.getTraspaso( self.usuario , self.contrasena , fecha , origen , destino )
        
        def getTraspasosBy( self , fechaInicio , fechaFin , origen , destino , orden ):
            return sql.getTraspasosBy( self.usuario , self.contrasena , fechaInicio , fechaFin , origen , destino , orden )

        # ------------- Aportaciones ------------- #

        def getAportacion( self , fecha , cuenta , isin , tipo ):
            return sql.getAportacion( self.usuario , self.contrasena , fecha , cuenta , isin , tipo )
        
        def getAportacionesBy( self , fechaInicio , fechaFin , cuenta , isin , tipo , orden ):
            return sql.getAportacionesBy( self.usuario , self.contrasena , fechaInicio , fechaFin , cuenta , isin , tipo , orden )

        # -------------- Comisiones -------------- #

        def getComision( self , fecha , cuenta , isin , tipo ):
            return sql.getComision( self.usuario , self.contrasena , fecha , cuenta , isin , tipo )
        
        def getComisionesBy( self , fechaInicio , fechaFin , cuenta , isin , tipo , orden ):
            return sql.getComisionesBy( self.usuario , self.contrasena , fechaInicio , fechaFin , cuenta , isin , tipo , orden )

        # ------------- Clasificacion ------------ #
        
        def getClasificacion( self , clasificacion ):
            return sql.getClasificacion( self.usuario , self.contrasena , clasificacion )
        
        def getClasificacionesBy( self , clasificacion , orden ):
            return sql.getClasificacionesBy( self.usuario , self.contrasena , clasificacion , orden )
        
        def getSubClasificacion( self , subClasificacion ):
            return sql.getSubClasificacion( self.usuario , self.contrasena , subClasificacion )
        
        def getSubClasificacionesBy( self , clasificacion , subClasificacion , orden ):
            return sql.getSubClasificacionesBy( self.usuario , self.contrasena , clasificacion , subClasificacion , orden )

        # --------------- Allocation ------------- #

        def getAllocation( self , allocation ):
            return sql.getAllocation( self.usuario , self.contrasena , allocation )
        
        def getAllocationsBy( self , allocation , orden ):
            return sql.getAllocationsBy( self.usuario , self.contrasena , allocation , orden )
        
        def getAllocationsOf( self , pISIN , pOrden ):
            allocationsOf = sql.getAllocationsOf( self.usuario , self.contrasena , pISIN , pOrden )
            resultado = []
            for allocation in allocationsOf: resultado.append( allocation[0] )
            return resultado
        
        def getSubAllocation( self , subAllocation ):
            return sql.getSubAllocation( self.usuario , self.contrasena , subAllocation )
        
        def getSubAllocationsBy( self , allocation , subAllocation , orden ):
            return sql.getSubAllocationsBy( self.usuario , self.contrasena , allocation , subAllocation , orden )
        
        def getSubAllocationsOf( self , pAllocation , pISIN , pOrden ):
            return sql.getSubAllocationsOf( self.usuario , self.contrasena , pAllocation , pISIN , pOrden )
        
        # --------------- Distribucion ------------- #
        
        def getIsinOfDistribucionFor( self , allocation ):
            return sql.getIsinOfDistribucionFor( self.usuario , self.contrasena , allocation )

        # ---------------------------------------- #
        # -------------- Calculos BD ------------- #
        # ---------------------------------------- #
        
        # --------------- Activos ---------------- #
        
        # ------------ Transacciones ------------- #
        
        def calcularTransacciones( self , pCuenta , pFechaInicio , pFechaFin , pClasificacion ):
            transacciones = sql.calcularTransacciones( self.usuario , self.contrasena , pCuenta , pFechaInicio , pFechaFin , pClasificacion )
            gastos = 0 ; ingresos = 0;
            for gasto , ingreso in transacciones:
                gastos += gasto;  ingresos += ingreso;
            return ( gastos , ingresos )
        
        # -------------- Transpasos -------------- #
        
        def calcularTraspasos( self , pCuenta , pFechaInicio , pFechaFin ):
            origen = 0
            traspasos = sql.calcularTraspasos( self.usuario , self.contrasena , 'Origen' , pCuenta , pFechaInicio , pFechaFin )
            for traspaso in traspasos: origen += traspaso[0]
            destino = 0
            traspasos = sql.calcularTraspasos( self.usuario , self.contrasena , 'Destino' , pCuenta , pFechaInicio , pFechaFin )
            for traspaso in traspasos: destino += traspaso[0]
            return ( origen , destino )
            
        
        # ------------- Aportaciones ------------- #
        
        # -------------- Comisiones -------------- #
        
        def calcularComisiones( self , pCuenta , pFechaInicio , pFechaFin , pTipo ):
            comisiones = sql.calcularComisiones( self.usuario , self.contrasena , pCuenta , pFechaInicio , pFechaFin , pTipo )
            gastos = 0 ; ingresos = 0;
            for gasto , ingreso in comisiones:
                gastos += gasto;  ingresos += ingreso;
            return ( gastos , ingresos )