# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from lib import HTML as html
from lib import Utils as utils
from lib import Ficheros as ficheros

from app import Sesion as sesion
from app import Seccion as secciones
from app import Formulario as frm
from app import Graficas as grf
from app import Filtro as filtro

####################################################################    
#---------------------------- Secciones ---------------------------#
####################################################################

class Secciones:
    
    instancia = None
    
    def __new__( cls ):
        if not Secciones.instancia:
            Secciones.instancia = Secciones.__Secciones( )
        return Secciones.instancia
    
    
    class __Secciones:
        
        def __init__( self ):
            self.seccion_actual = "Principal"
            self.subseccion_actual = "Principal"
            self.mensaje = ""
            self.parametros = {}
            self.secciones = {}
            # ************************************ PRINCIPAL ************************************ #
            # Principal
            self.secciones[ "Principal" ] = Principal( "Principal" )
            self.secciones[ "Principal_Historia" ] = Principal( "Historia" )
            self.secciones[ "Principal_Inflacion" ] = Principal( "Inflacion" )
            # Activos
            self.secciones[ "Principal_Activos" ] = Principal( "Activos" )
            self.secciones[ "Principal_Acciones" ] = Principal( "Acciones" )
            self.secciones[ "Principal_Bonos" ] = Principal( "Bonos" )
            # Estrategias
            self.secciones[ "Principal_Estrategias" ] = Principal( "Estrategias" )
            self.secciones[ "Principal_DGI" ] = Principal( "DGI" )
            self.secciones[ "Principal_Grow" ] = Principal( "Grow" )
            # ************************************** SESION ************************************* #
            self.secciones[ "InicioSesion" ] = InicioSesion()           
            self.secciones[ "CerrarSesion" ] = CerrarSesion()             
            # ************************************* REGISTRO ************************************ #
            self.secciones[ "Registro" ] = Registro()             
            # ********************************** CONFIGURACION ********************************** #
            self.secciones[ "Perfil" ] = Perfil()
            self.secciones[ "Estilos" ] = Estilos() 
            # *********************************** ADMISIONES ************************************ #
            self.secciones[ "Admision" ] = Admision()                      
            self.secciones[ "Administracion" ] = Administracion()
            self.secciones[ "Accesos" ] = Accesos()
            # ************************************* GESTION ************************************* #
            self.secciones[ "Gestion" ] = Gestion() 
            # ************************************* GESTION ************************************* #
            self.secciones[ "Analisis" ] = Analisis() 
            # ********************************** IMPORTACIONES ********************************** #
            self.secciones[ "Importaciones" ] = Importaciones()
            self.secciones[ "Exportaciones" ] = Exportaciones()
            # ************************************* FILTROS ************************************* #
            self.secciones[ "Filtros" ] = Filtros() 
   
            
        #Parametros: SubFormulario   ;   Ordenar
        def getParametros( self , pClass ): 
            parametro = ""
            if pClass in self.parametros: parametro = self.parametros[ pClass ]    
            return parametro
        
        def setParametros( self , pClass , pParametro ): self.parametros[ pClass ] = pParametro
        
        
        def reportarError( self , pMensaje ): self.mensaje = pMensaje
        def agregarError( self , pMensaje ): self.mensaje += pMensaje + "<br />"
            
        
        def redireccionar( self , pSubSeccion ):
            self.subseccion_actual = pSubSeccion
            self.seccion_actual = self.secciones[ pSubSeccion ].seccion
         
        
        def generarRedireccion( self , pRedireccion ):           
            SEPARADOR_PARAMETROS = '/'
            if pRedireccion.count( SEPARADOR_PARAMETROS ) == 1:
                direccion , parametros = pRedireccion.split( SEPARADOR_PARAMETROS )
                self.setParametros( 'SubFormulario' , parametros )
            else:
                direccion = pRedireccion
            if direccion in self.secciones:
                if self.secciones[ direccion ].comprobarAcceso():             
                    self.redireccionar( direccion )                    
                else:
                    #mensaje = "Te he redirigido a InicioSesion porque no tenias acceso a la seccion " + pRedireccion
                    self.redireccionar( 'InicioSesion' )
                    #self.reportarError( mensaje )
            else:  
                mensaje = "Te he redirigido a Principal porque la sección " + pRedireccion + " no existe"
                self.redireccionar( 'Principal' )
                self.reportarError( mensaje )
            return redirect( '/' ) 
        
        
        def generarIndice( self ):
            informacion = ""
            informacion += self.generarIndicePrincipal()
            informacion += self.generarIndiceSecundario()
            informacion += self.generarIndiceEspecial()
            return informacion
            
        def generarIndicePrincipal( self ):
            # TODO hacerque sea dinamico en funcion de las secciones que existan
            indice = []            
            if sesion.Sesion().comprobarPermisos( "=" , 0 ):
                indice.append( ( "Registro" , "Registro" ) )
                indice.append( ( "InicioSesion" , "Iniciar Sesión" ) )
            if sesion.Sesion().comprobarPermisos( ">=" , 2 ):
                indice.append( ( "Administracion" , "Admisiones" ) )                
            if sesion.Sesion().comprobarPermisos( ">=" , 1 ):
                indice.append( ( "Perfil" , "Configuración" ) )
                indice.append( ( "Gestion" , "Transacciones" ) )
                indice.append( ( "Importaciones" , "Importaciones" ) )
                indice.append( ( "Analisis" , "Análisis" ) )
                indice.append( ( "CerrarSesion" , "Cerrar Sesión" ) )                  
            return html.indice( "IndicePrincipal" , "principal" , indice )
        
        def generarIndiceSecundario( self ):
            # TODO hacerque sea dinamico en funcion de las secciones que existan
            indice = []
            informacion = ''
            
            if self.seccion_actual == "Principal":
                indice.append( ( "Principal" , "Introducción" ) )
                indice.append( ( "Principal_Activos" , "Activos" ) )
                indice.append( ( "Principal_Estrategias" , "Estrategias" ) )
                
            if self.seccion_actual == "Configuracion":
                indice.append( ( "Perfil" , "Perfil" ) )
                indice.append( ( "Estilos" , "Estilos" ) )
                
            if self.seccion_actual == "Admisiones":
                indice.append( ( "Administracion" , "Administración" ) )
                indice.append( ( "Admision" , "Admisión" ) )
                indice.append( ( "Accesos" , "Accesos" ) )
                
            if self.seccion_actual == "Importaciones":
                indice.append( ( "Importaciones" , "Importaciones" ) )
                indice.append( ( "Exportaciones" , "Exportaciones" ) )
            
            if self.seccion_actual == "Gestion":
                informacion = self.secciones[ self.seccion_actual ].generarIndice()
            
            if self.seccion_actual == "Analisis":
                informacion = self.secciones[ self.seccion_actual ].generarIndice()
                
            if not len(indice) == 0: informacion = html.indice( "IndiceSecundario" , "secundario" , indice ) 
            return informacion

        def generarIndiceEspecial( self ):
            indice = []
            print( "seccion_actual" , self.seccion_actual , "subseccion_actual" , self.subseccion_actual )
            if self.seccion_actual == "Principal":
                if ( self.subseccion_actual == "Principal" or self.subseccion_actual == "Principal_Historia" or self.subseccion_actual == "Principal_Inflacion" ):
                    indice.append( ( "Principal_Historia" , "Historia" ) )
                    indice.append( ( "Principal_Inflacion" , "Inflación" ) )
            
                if ( self.subseccion_actual == "Principal_Activos" or self.subseccion_actual == "Principal_Acciones" or self.subseccion_actual == "Principal_Bonos"):
                    indice.append( ( "Principal_Acciones" , "Acciones" ) )
                    indice.append( ( "Principal_Bonos" , "Bonos" ) )
        
                if ( self.subseccion_actual == "Principal_Estrategias" or self.subseccion_actual == "Principal_DGI" or self.subseccion_actual == "Principal_Grow"):
                    indice.append( ( "Principal_DGI" , "Dividendos" ) )
                    indice.append( ( "Principal_Grow" , "Crecimiento" ) )
        
            informacion  = ''
            if not len( indice ) == 0: informacion += html.indice( "indiceEspecial" , "especial" , indice )
            return informacion
 
    
        def generarPagina( self ):            
            contenido = self.secciones[ self.subseccion_actual ].generarContenido()
            if contenido == '': informacion = redirect( '/' ) 
            else:
                informacion = render_template('0_index.php')
                informacion += self.generarIndice()
                print("Mensaje: " + self.subseccion_actual )
                print("Mensaje: " + self.mensaje )
                informacion += html.mensaje( self.mensaje )
                informacion += contenido
                informacion += render_template('0_footer.php')
            return informacion

            
####################################################################    
#----------------------------- Seccion ----------------------------#
####################################################################

class Seccion:
    
    def __init__( self , pSeccion , pSubSeccion , pTitulo , pPermisos , pEstricto ):   
        self.seccion = pSeccion
        self.subSeccion = pSubSeccion
        self.titulo = pTitulo
        self.permisos = pPermisos
        self.estricto = pEstricto
        self.filtro = None
    
    
    def comprobarAcceso( self ):
        caducado = False
        permiso = sesion.Sesion().comprobarPermisos( self.estricto , self.permisos );
        inicio = sesion.Sesion().comprobarSesionIniciada()
        if inicio: 
            caducado = sesion.Sesion().comprobarTiempoSesion()        
        if caducado: 
            mensaje = "El tiempo de sesión ha caducado debido a la inactividad"
            Secciones().reportarError( mensaje )
        if not permiso: 
            mensaje = "No puedes acceder a dichas funcionalidades con tu nivel de permisos actual"
            Secciones().reportarError( mensaje )     
        return permiso and not caducado
    
    
    def generarIndice( self ):
        informacion = ""
        mensaje = html.working( )
        secciones.Secciones().reportarError( mensaje )
        return informacion
    
    
    def generarContenido( self ):
        informacion = ""
        informacion += html.seccion( self.subSeccion , "contenido" )
        informacion += "<br /> <br />"
        informacion += html.titulo( self.subSeccion , "contenido" , 1 , self.titulo )
        informacion += "<br /> <br />"
        informacion += self.generarFormulario( )
        informacion += "<br /> <br />"
        informacion += "</section>"        
        redireccion = self.capturarCamposGlobal( )
        if redireccion: informacion = ''
        return informacion
    
    
    def generarFormulario( self ):
        mensaje = html.working( )
        #secciones.Secciones().reportarError( mensaje )
        return "<p> " + mensaje + " </p>"

    
    def capturarCamposGlobal( self ):
        recargarPagina = False
        if request.method == 'POST':
            redirigir = request.form['Redirigir']
            recargarPagina = self.capturarCampos( redirigir )
                   
        return recargarPagina
    

    def capturarCampos( self , redirigir ):
        mensaje = html.working( )
        secciones.Secciones().reportarError( mensaje )
        return False
    
####################################################################    
#---------------------------- Principal ---------------------------#
####################################################################

#---------------------------- Principal ---------------------------#

class Principal(Seccion):
    
    def __init__( self , pFichero ):   
        Seccion.__init__( self , 'Principal' , 'Principal' , 'Guía de utilización de la aplicación' , 0 , '>=' )
        self.fichero = pFichero   
    
    def generarContenido( self ):
        informacion = ''
        informacion += "<br /> <br />" 
        informacion = render_template('1_' + self.fichero + '.php')
        informacion += "<br /> <br />" 
        return informacion
        
####################################################################    
#------------------------------ Sesion ----------------------------#
####################################################################

# ------------------------ Inicio Sesion ------------------------- #

class InicioSesion(Seccion):
    
    def __init__( self ):   
        Seccion.__init__( self , 'Sesion' , 'InicioSesion' , 'Inicio de Sesión' , 0 , '=' )
    
        
    def generarFormulario( self ):
        informacion = ""
        informacion += html.formHeader( "login" , "login" , '/' , False )
        #$informacion += "<br />"
        informacion += "<fieldset>"
        informacion += html.formInput( "Usuario" , "login" , "Usuario" , "text" , "Nombre de usuario" , "Escriba su nombre de usuario" , "" , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Contrasena" , "login" , "Contraseña" , "password" , "********" , "Escriba su contraseña" , "" , False )
        informacion += "<br /> <br />"
        informacion += html.formHidden( 'Redirigir' , 'login' , "IniciarSesion" )
        informacion += html.formSubmit( "aceptar" , "login" , "Iniciar Sesión" )
        informacion += "</fieldset>" 
        informacion += "</form>"
        return informacion


    def capturarCampos( self , redirigir ):
        sesionIniciada = False
        
        if redirigir == "IniciarSesion":
            usuario = utils.depurarTodo( request.form['Usuario'] )
            contrasena = request.form['Contrasena']
            sesionIniciada = sesion.Sesion().iniciarSesion( usuario , contrasena )
                
        return sesionIniciada    
    
#-------------------------- Cerrar Sesion -------------------------#

class CerrarSesion(Seccion):
    
    def __init__( self ):   
        Seccion.__init__( self , 'Sesion' , 'CerrarSesion' , 'Cerrar Sesión' , 1 , '>=' )
    
    def generarContenido( self ):
        sesion.Sesion().cerrarSesion()
        return ''
               
####################################################################    
#---------------------------- Registro ----------------------------#
####################################################################

#---------------------------- Registro ----------------------------#

class Registro(Seccion):
    
    def __init__( self ):   
        Seccion.__init__( self , 'Registro' , 'Registro' , 'Registro' , 0 , '=' )
        self.usuario = ''
        self.nombre = ''
        self.primerApellido = ''
        self.segundoApellido = ''
        self.dni = ''
        self.telefono = ''
        self.email = ''
  
    def generarFormulario( self ):
        informacion = ""
        informacion += html.formHeader( "Registro" , "Registro" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        informacion += html.formInput( "Usuario" , "Registro" , "Usuario" , "text" , "NikName69" , "Escriba su nombre de usuario" , self.usuario , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Nombre" , "Registro" , "Nombre" , "text" , "Pepito" , "Escriba su nombre" , self.nombre , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "PrimerApellido" , "Registro" , "Primer Apellido" , "text" , "Gonzalez" , "Escriba su primer apellido" , self.primerApellido , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "SegundoApellido" , "Registro" , "Segundo Apellido" , "text" , "Martinez" , "Escriba su segundo apellido" , self.segundoApellido , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "DNI" , "Registro" , "DNI" , "DNI" , "12345678Z" , "Escriba su documento de identificacion" , self.dni , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Telefono" , "Registro" , "Teléfono"  , "tel" , "123456789" , "Escriba su número de teléfono" , self.telefono , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Email" , "Registro" , "Email" , "email" , "miCorreoElectronico@hotmail.com" , "Escriba correo electrónico" , self.email , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Contrasena" , "Registro" , "Contraseña" , "password" , "********" , "Escriba su contraseña" , "" , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "RepitaContrasena" , "Registro" , "Repita la contraseña" , "password" , "********" , "Repita la contraseña" , "" , False )
        informacion += "<br /> <br />"
        informacion += html.formCheckBox( "Condiciones" , "Registro" , "He leído y acepto las condiciones de uso" , 'Acepta' )
        informacion += "<br /> <br />"
        informacion += html.formHidden( 'Redirigir' , 'Registro' , "AnadirAdmision" )
        informacion += html.formSubmit( "aceptar" , "Registro" , "Registrarse" )
        informacion += "</fieldset>" 
        informacion += "</form>"
        return informacion
    
    
    def capturarCampos( self , redirigir ):
        usuarioRegistrado = False

        if redirigir == "AnadirAdmision":
            self.usuario = utils.depurarTodo( request.form['Usuario'] )
            self.nombre = utils.depurarTodo( request.form['Nombre'] )
            self.primerApellido = utils.depurarTodo( request.form['PrimerApellido'] )
            self.segundoApellido = utils.depurarTodo( request.form['SegundoApellido'] )
            self.dni = request.form['DNI']
            self.telefono = request.form['Telefono']
            self.email = request.form['Email']
            contrasena = request.form['Contrasena']
            contraseñaRPT = request.form['RepitaContrasena']
            if 'Condiciones' in request.form: condiciones = True
            else: condiciones = False 
            usuarioRegistrado = sesion.Sesion().anadirAdmision( self.usuario , self.nombre , self.primerApellido , self.segundoApellido , self.dni , self.telefono , self.email , contrasena , contraseñaRPT , condiciones )
        
        return usuarioRegistrado
        
####################################################################    
#--------------------------- Configuracion ------------------------#
####################################################################

#------------------------------ Perfil ----------------------------#

class Perfil(Seccion):
    
    def __init__( self ):   
        Seccion.__init__( self , 'Configuracion' , 'Perfil' , 'Perfil' , 1 , '>=' )


    def generarFormulario( self ):
        informacion = ""
        informacion += html.titulo( "Perfil" , "contenido" , 2 , "Editar Perfil" )
        informacion += self.formularioEditarPerfil( )
        informacion += "<br />"
        informacion += html.titulo( "Perfil" , "contenido" , 2 , "Cambiar Contraseña" )
        informacion += self.formularioEditarContrasena( )
        return informacion
    
    
    def formularioEditarPerfil( self ):
        informacion = ""
        nombre , primerApellido , segundoApellido , usuario , dni , telefono , email , contrasena , sal , permisos = sesion.Sesion().getUsuario("")
        informacion += html.formHeader( "EditarPerfil" , "Perfil" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        informacion += html.formInput( "Nombre" , "Perfil" , "Nombre" , "text" , "Pepito" , "Escriba su nombre" , nombre , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "PrimerApellido" , "Perfil" , "Primer Apellido"  , "text" , "Gonzalez" , "Escriba su primer apellido" , primerApellido , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "SegundoApellido" , "Perfil" , "Segundo Apellido"  , "text" , "Martinez" , "Escriba su segundo apellido" , segundoApellido , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "DNI" , "Perfil" , "DNI" , "DNI" , "12345678Z" , "Escriba su documento de identificación" , dni , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Telefono" , "Perfil" , "Teléfono" , "tel" , "123456789" , "Escriba su número de teléfono" , telefono , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Email" , "Perfil" , "Email" , "email" , "miCorreoElectronico@hotmail.com" , "Escriba correo electrónico " , email , False )
        informacion += "<br /> <br />"
        informacion += html.formHidden( 'Redirigir' , 'Perfil' , "EditarPerfil" )
        informacion += html.formSubmit( "aceptar" , "Perfil" , "Aplicar Cambios" )
        informacion += "</fieldset>" 
        informacion += "</form>"
        return informacion
    
    
    def formularioEditarContrasena( self ):        
        informacion = ""
        informacion += html.formHeader( "EditarContrasena" , "Perfil" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        informacion += html.formInput( "ContrasenaAnterior" , "Perfil" , "Contraseña Anterior" , "password" , "********" , "Escriba su contraseña antigua" , "" , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "ContrasenaNueva" , "Perfil" , "Contraseña Nueva" , "password" , "********" , "Escriba la nueva contraseña" , "" , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "RepitaContrasena" , "Perfil" , "Repita la Contraseña" , "password" , "********" , "Repita la nueva contraseña" , "" , False )
        informacion += "<br /> <br />"
        informacion += html.formHidden( 'Redirigir' , 'Perfil' , "EditarContrasena" )
        informacion += html.formSubmit( "aceptar" , "Perfil" , "Cambiar Contrasña" )
        informacion += "</fieldset>" 
        informacion += "</form>"
        return informacion


    def capturarCampos( self , redirigir ):
        recargarPagina = False

        if redirigir == "EditarPerfil":
            nombre = utils.depurarTodo( request.form['Nombre'] )
            primerApellido = utils.depurarTodo( request.form['PrimerApellido'] )
            segundoApellido = utils.depurarTodo( request.form['SegundoApellido'] )
            dni = request.form['DNI']
            telefono = request.form['Telefono']
            email = request.form['Email']
            sesion.Sesion().actualizarUsuario( nombre , primerApellido , segundoApellido , dni , telefono , email )
            recargarPagina = True
            
        if redirigir == "EditarContrasena":
            contrasenaAnterior = request.form['ContrasenaAnterior']
            ContraseñaNueva = request.form['ContrasenaNueva']
            RepitaContraseña = request.form['RepitaContrasena']
            recargarPagina = sesion.Sesion().actualizarCredenciales( contrasenaAnterior , ContraseñaNueva , RepitaContraseña )

        return recargarPagina

#----------------------------- Estilos ----------------------------#

class Estilos(Seccion):
    
    def __init__( self ):   
        Seccion.__init__( self, 'Configuracion' , 'Estilos' , 'Configuración gráfica' , 2 , '>=' )
        
####################################################################    
#---------------------------- Admisiones --------------------------#
####################################################################

#----------------------------- Admision ---------------------------#

class Admision(Seccion):
    
    def __init__( self ):   
        Seccion.__init__( self , 'Admisiones' , 'Admision' , 'Gestión de Admisiones' , 2 , '>=' )
        
        self.filtro = filtro.Filtro( 'Admision' , 'Admision' )
        self.filtro.anadirCampo( 'Usuario' , 'Usuario' , 'text' , 'Identificador único  de la Admisión buscada' )
        self.filtro.anadirCampo( 'DNI' , 'DNI' , 'dni' , 'DNI de la Admisión buscada')
        self.filtro.anadirCampo( 'Nombre' , 'Nombre' , 'text' , 'Nombre de la Admisión buscada' )
        self.filtro.anadirCampo( 'Apellido1' , 'Primer Apellido' , 'text' , 'Primer apellido de la Admisión buscada' )
        self.filtro.anadirCampo( 'Apellido2' ,  'Segundo Apellido' , 'text' , 'Segundo apellido de la Admisión buscada' )


    def generarFormulario( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        vUsuario = self.filtro.campos[ 'Usuario' ].getValor()
        vDNI = self.filtro.campos[ 'DNI' ].getValor()
        vNombre = self.filtro.campos[ 'Nombre' ].getValor()
        vApellido1 = self.filtro.campos[ 'Apellido1' ].getValor()
        vApellido2 = self.filtro.campos[ 'Apellido2' ].getValor()
        
        admisiones = sesion.Sesion().getAdmisionesBy( vUsuario , vDNI , vNombre , vApellido1 , vApellido2 , self.filtro.orden )
        
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarUsuario' , 'Admision' , 'etiqueta' , 'Ordenar' , 'Usuario' , 'Usuario' ) + " </th>"
        informacion += "       <th>         </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   <tr>"
        
        for nombre , primerApellido , segundoApellido , usuario , dni , telefono , email , contrasena , sal in admisiones:
            informacion += "   <tr>"
            informacion += "       <td> " + nombre + " " + primerApellido + " " + segundoApellido + " ; " + usuario + " </td>"
            informacion += "       <td> " + self.formularioAnadirUsuario( usuario ) + " </td>"
            informacion += "       <td> " + self.formularioEliminarAdmision( usuario ) + " </td>"
            informacion += "   <tr>"
        
        informacion += "</table>"    
        return informacion
        
    
    def formularioAnadirUsuario( self , pUsuario ):
        opciones = []
        opciones.append( ( "1" , 'Usuario' , False ) )
        if sesion.Sesion().comprobarPermisos( "=" , 3 ): opciones.append( ( "2" , 'Administrador' , False ) )
        informacion = ""
        informacion += html.formHeader( "AnadirUsuario" , "Admisiones" , '/' , False )
        informacion += html.formOptionList( 'Permisos' , 'Admisiones' , '' , opciones , False )
        informacion += html.formHidden( 'Usuario' , 'Admisiones' , pUsuario )
        informacion += html.formHidden( 'Redirigir' , 'Admisiones' , "AnadirUsuario" )
        informacion += html.formSubmit( "aceptar" , "Admisiones" , "Aceptar" )
        informacion += "</form>"
        return informacion
        
    
    def formularioEliminarAdmision( self , pUsuario ):
        informacion = ""
        informacion += html.formHeader( "EliminarAdmision" , "Admisiones" , '/' , False )
        informacion += html.formHidden( 'Usuario' , 'Admisiones' , pUsuario )
        informacion += html.formHidden( 'Redirigir' , 'Admisiones' , 'EliminarAdmision' )
        informacion += html.formSubmit( 'eliminar' , 'Admisiones' , 'Rechazar' )
        informacion += "</form>"               
        return informacion
        

    def capturarCampos( self , redirigir ):
        recargarPagina = False
        
        if redirigir == "AnadirUsuario":
            usuario = request.form['Usuario']
            permisos = request.form['Permisos']
            sesion.Sesion().anadirUsuario( usuario , permisos )
            sesion.Sesion().eliminarAdmision( usuario )
            recargarPagina = True
            
        if redirigir == "EliminarAdmision":
            usuario = request.form['Usuario']
            sesion.Sesion().eliminarAdmision( usuario )
            recargarPagina = True
                
        return recargarPagina
    
#-------------------------- Administracion ------------------------#

class Administracion(Seccion):
    
    def __init__( self ):   
        Seccion.__init__( self , 'Admisiones' ,'Administracion' , 'Gestión de Usuarios' , 2 , '>=' )
        
        self.filtro = filtro.Filtro( 'Administracion' , 'Administracion' ) 
        self.filtro.anadirCampo( 'Usuario' , 'Usuario' , 'text' , 'Identificador único del Usuario buscado ' )
        self.filtro.anadirCampo( 'DNI' , 'DNI' , 'dni' , 'DNI del Usuario buscado')
        self.filtro.anadirCampo( 'Nombre' , 'Nombre' , 'text' , 'Nombre del Usuario buscado' )
        self.filtro.anadirCampo( 'Apellido1' , 'Primer Apellido' , 'text' , 'Primer apellido del Usuario buscado' )
        self.filtro.anadirCampo( 'Apellido2' ,  'Segundo Apellido' , 'text' , 'Segundo apellido del Usuario buscado' )
        self.filtro.anadirCampo( 'Permisos' , 'Permisos' , 'text' , 'Permisos del Usuario buscado' )
        

    def generarFormulario( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        vUsuario = self.filtro.campos[ 'Usuario' ].getValor()
        vDNI = self.filtro.campos[ 'DNI' ].getValor()
        vNombre = self.filtro.campos[ 'Nombre' ].getValor()
        vApellido1 = self.filtro.campos[ 'Apellido1' ].getValor()
        vApellido2 = self.filtro.campos[ 'Apellido2' ].getValor()
        vPermisos = self.filtro.campos[ 'Permisos' ].getValor()
        
        admisiones = sesion.Sesion().getUsuariosBy( vUsuario , vDNI , vNombre , vApellido1 , vApellido2 , vPermisos , self.filtro.orden )
        
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarUsuario' , 'Administracion' , 'etiqueta' , 'Ordenar' , 'Usuario' , 'Usuario' ) + " </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarPermisos' , 'Administracion' , 'etiqueta' , 'Ordenar' , 'Permisos' , 'Permisos' ) + " </th>"
        informacion += "       <th>         </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   <tr>"
        
        for nombre , primerApellido , segundoApellido , usuario , dni , telefono , email , contrasena , sal , permisos in admisiones:
            informacion += "   <tr>"
            informacion += "       <td> " + nombre + " " + primerApellido + " " + segundoApellido + " ; " + usuario + " </td>"
            informacion += "       <td> " + utils.permisosToString( permisos ) + " </td>"
            informacion += "       <td> " + self.formularioActualizarPermisos( usuario , permisos ) + " </td>"
            informacion += "       <td> " + self.formularioEliminarUsuario( usuario , permisos ) + " </td>"
            informacion += "   <tr>"
        
        informacion += "</table>"    
        return informacion
        
    
    def formularioActualizarPermisos( self , pUsuario , pPermisos ):
        opciones = []
        informacion = ""
        if sesion.Sesion().comprobarPermisos( ">" , pPermisos ): 
            if sesion.Sesion().comprobarPermisos( ">" , 1 ): opciones.append( ( "1" , 'Usuario' , False ) )
            if sesion.Sesion().comprobarPermisos( ">" , 2 ): opciones.append( ( "2" , 'Administrador' , False ) )
            if sesion.Sesion().comprobarPermisos( ">" , 3 ): opciones.append( ( "3" , 'Creador' , False ) )
            informacion += html.formHeader( "ActualizarPermisos" , "Admisiones" , '/' , False )
            informacion += html.formOptionList( 'NuevosPermisos' , 'Admisiones' , '' , opciones , False )
            informacion += html.formHidden( 'Usuario' , 'Admisiones' , pUsuario )
            informacion += html.formHidden( 'Permisos' , 'Admisiones' , str(pPermisos) )
            informacion += html.formHidden( 'Redirigir' , 'Admisiones' , "ActualizarPermisos" )
            informacion += html.formSubmit( "aceptar" , "Admisiones" , "Cambiar Permisos" )
            informacion += "</form>"
        return informacion
        
    
    def formularioEliminarUsuario( self , pUsuario , pPermisos ):
        informacion = ""
        informacion += html.formHeader( "EliminarUsuario" , "Admisiones" , '/' , False )
        informacion += html.formHidden( 'Usuario' , 'Admisiones' , pUsuario )
        informacion += html.formHidden( 'Permisos' , 'Admisiones' , str(pPermisos) )
        informacion += html.formHidden( 'Redirigir' , 'Admisiones' , 'EliminarUsuario' )
        informacion += html.formSubmit( 'eliminar' , 'Admisiones' , 'Eliminar' )
        informacion += "</form>"               
        return informacion


    def capturarCampos( self , redirigir ):
        recargarPagina = False
        
        if redirigir == "ActualizarPermisos":
            usuario = request.form['Usuario']
            nuevosPermisos = request.form['NuevosPermisos']
            permisos = request.form['Permisos']
            sesion.Sesion().actualizarPermisos( usuario , int(permisos) , nuevosPermisos )
            recargarPagina = True
            
        if redirigir == "EliminarUsuario":
            usuario = request.form['Usuario']
            permisos = request.form['Permisos']
            sesion.Sesion().eliminarUsuario( usuario , int(permisos) )
            recargarPagina = True
                
        return recargarPagina
    
#----------------------------- Accesos ----------------------------#

class Accesos(Seccion):
    
    def __init__( self ):   
        Seccion.__init__( self, 'Admisiones' , 'Accesos' , 'Gestión de Accesos' , 2 , '>=' )
        
####################################################################    
#----------------------------- Gestion ----------------------------#
####################################################################

#----------------------------- Gestion ----------------------------#

class Gestion(Seccion):
    
    def __init__( self ):   
        Seccion.__init__( self , 'Gestion' , 'Gestion' , 'Transacciones' , 1 , '>=' )      
        self.formulario_actual = "Activos"
        self.subFormulario_actual = "Activos"      
        self.formularios = {}
        
        # ---------------------------- ACTIVOS ---------------------------- #
        self.formularios[ "Activos" ] = frm.Activos()         
        # ---------------------------- CUENTAS ---------------------------- #
        self.formularios[ "Cuentas" ] = frm.Cuentas()          
        # --------------------------- CATEGORIAS -------------------------- #
        self.formularios[ "Estrategias" ] = frm.Estrategias()
        self.formularios[ "Categorias" ] = frm.Categorias()    
        #self.formularios[ "Categorizacion" ] = frm.Categorizacion() 
        self.formularios[ "Productos" ] = frm.Productos()       
        # ------------------------- DISTRIBUCIONES ------------------------ #
        self.formularios[ "Allocation" ] = frm.Allocation()
        self.formularios[ "SubAllocation" ] = frm.SubAllocation()
        self.formularios[ "Clasificacion" ] = frm.Clasificacion()
        self.formularios[ "SubClasificacion" ] = frm.SubClasificacion()
        # -------------------------- OPERACIONES -------------------------- #
        self.formularios[ "Transacciones" ] = frm.Transacciones()            
        self.formularios[ "Aportaciones" ] = frm.Aportaciones() 
        self.formularios[ "Comisiones" ] = frm.Comisiones()            
        self.formularios[ "Traspasos" ] = frm.Traspasos() 


    def generarIndice( self ):
        informacion = ""
        informacion += self.generarIndicePrincipal()
        informacion += self.generarIndiceSecundario()
        return informacion
        
    
    def generarIndicePrincipal( self ):
        # TODO hacerque sea dinamico en funcion de los formularios que existan
        indice = []         
        indice.append( ( "Gestion/Cuentas" , "Cuentas" ) )
        indice.append( ( "Gestion/Activos" , "Activos" ) ) 
        indice.append( ( "Gestion/Categorias" , "Categorias" ) ) 
        indice.append( ( "Gestion/Allocation" , "Distribuciones" ) ) 
        indice.append( ( "Gestion/Aportaciones" , "Operaciones" ) )
        return html.indice( "IndiceTransaccionesPrincipal" , "secundario" , indice )  
    
    def generarIndiceSecundario( self ):
        indice = []
        informacion  = ''
        print("FORM:" , self.formulario_actual, "SUBFORM:" , self.subFormulario_actual )
        if self.formulario_actual == "Categorias":
            indice.append( ( "Gestion/Estrategias" , "Estrategias" ) )
            indice.append( ( "Gestion/Categorias" , "Categorias" ) )   
            indice.append( ( "Gestion/Productos" , "Productos" ) )
        if self.formulario_actual == "Distribuciones":
            indice.append( ( "Gestion/Allocation" , "Allocation" ) ) 
            indice.append( ( "Gestion/Clasificacion" , "Clasificación" ) )      
        if self.formulario_actual == "Operaciones":
            indice.append( ( "Gestion/Transacciones" , "Transacciones" ) ) 
            indice.append( ( "Gestion/Aportaciones" , "Aportaciones" ) ) 
            indice.append( ( "Gestion/Comisiones" , "Comisiones" ) )
            indice.append( ( "Gestion/Traspasos" , "Traspasos" ) ) 
        if not len(indice) == 0:
            informacion = html.indice( "IndiceTransaccionesSecundario" , "especial" , indice )
        return informacion
    
    
    def generarContenido( self ):
        self.capturarRedireccion()
        redireccion = self.capturarCamposGlobal()
        informacion = ""
        informacion += html.seccion( self.subFormulario_actual , "contenido" )
        informacion += "<br /> <br />"
        informacion += html.titulo( self.formulario_actual + self.subFormulario_actual , "contenido" , 1 , self.formularios[ self.subFormulario_actual ].titulo )
        informacion += "<br /> <br />"
        informacion += self.formularios[ self.subFormulario_actual ].generarFormulario()
        informacion += "<br /> <br />"
        informacion += "</section>"        
        if redireccion: informacion = ''
        return informacion
    
    
    def capturarCampos( self , redirigir ): 
        self.formularios[ self.subFormulario_actual ].capturarCampos( redirigir )

    
    def capturarRedireccion( self ):
        parametros = secciones.Secciones().getParametros( 'SubFormulario' )
        print("PARAM:" , parametros , "ESTA:" , str(parametros in self.formularios) )
        if parametros in self.formularios:
            self.subFormulario_actual = parametros
            self.formulario_actual = self.formularios[ self.subFormulario_actual ].formulario
    

####################################################################    
#----------------------------- Analisis ---------------------------#
####################################################################

#----------------------------- Analisis ---------------------------#

class Analisis(Seccion):
    
    def __init__( self ):   
        Seccion.__init__( self , 'Analisis' , 'Analisis' , 'Análisis' , 1 , '>=' )      
        self.formulario_actual = "Balance"
        self.subFormulario_actual = "Balance"      
        self.formularios = {}
        # -------------------------- Balance -------------------------- #
        self.formularios[ "Balance" ] = grf.Balance()
        # ------------------------ Patrimonio ------------------------- #
        self.formularios[ "Gastos" ] = grf.Gastos()
        self.formularios[ "Patrimonio" ] = grf.Patrimonio()
        # ------------------------- Evolucion ------------------------- #
        self.formularios[ "Evolucion" ] = grf.Evolucion()#
        self.formularios[ "Flujo" ] = grf.Flujo()
    
    def generarIndice( self ):
        informacion = ""
        informacion += self.generarIndicePrincipal()
        informacion += self.generarIndiceSecundario()
        return informacion
    
    def generarIndicePrincipal( self ):
        indice = []           
        indice.append( ( "Analisis/Balance" , "Balance" ) ) 
        indice.append( ( "Analisis/Patrimonio" , "Patrimonio" ) ) 
        indice.append( ( "Analisis/Evolucion" , "Flujo Caja" ) ) 
        return html.indice( "IndiceTransaccionesPrincipal" , "secundario" , indice )
    
    def generarIndiceSecundario( self ):
        indice = []
        informacion  = ''
        print("FORM:" , self.formulario_actual, "SUBFORM:" , self.subFormulario_actual )
        #if self.formulario_actual == "Balance":
        if self.formulario_actual == "Patrimonio":
            indice.append( ( "Analisis/Patrimonio" , "Activos" ) )
            indice.append( ( "Analisis/Gastos" , "Gastos" ) )             
        if self.formulario_actual == "Evolucion":
            indice.append( ( "Analisis/Evolucion" , "Evolución Activos" ) ) 
            indice.append( ( "Analisis/Flujo" , "Evolución Gastos" ) ) 
   
        if not len(indice) == 0:
            informacion = html.indice( "IndiceTransaccionesSecundario" , "especial" , indice )
        return informacion


    def generarContenido( self ):
        self.capturarRedireccion()
        redireccion = self.capturarCamposGlobal()
        informacion = ""
        informacion += html.seccion( self.subFormulario_actual , "contenido" )
        informacion += "<br /> <br />"
        informacion += html.titulo( self.formulario_actual + self.subFormulario_actual , "contenido" , 1 , self.formularios[ self.subFormulario_actual ].titulo )
        informacion += "<br /> <br />"
        informacion += self.formularios[ self.subFormulario_actual ].generarFormulario()
        informacion += "<br /> <br />"
        informacion += "</section>"        
        if redireccion: informacion = ''
        return informacion
    
    
    def capturarCampos( self , redirigir ): 
        self.formularios[ self.subFormulario_actual ].capturarCampos( redirigir )

    
    def capturarRedireccion( self ):
        parametros = secciones.Secciones().getParametros( 'SubFormulario' )
        print("PARAM:" , parametros , "ESTA:" , str(parametros in self.formularios) )
        if parametros in self.formularios:
            self.subFormulario_actual = parametros
            self.formulario_actual = self.formularios[ self.subFormulario_actual ].formulario


####################################################################    
#-------------------------- Importaciones -------------------------#
####################################################################

#-------------------------- Importaciones -------------------------#

class Importaciones(Seccion):
    
    def __init__( self ):   
        Seccion.__init__(self, 'Importaciones' , 'Importaciones' , 'Importación de Datos' , 1 , '>=' )
    
    
    def generarFormulario( self ):
        informacion = ""       
        informacion += html.formHeader( "Importaciones" , "Importaciones" , '/' , True )
        informacion += "<fieldset>"
        informacion += html.formFichero( "Fichero" , "Importaciones" , '.csv' )
        informacion += "<br /> <br />"
        informacion += html.formCheckBox( "Sustituir" , "Importaciones" , "Marque esta casilla para sustituir todos los datos." , 'Acepta' )
        informacion += "<br /> <br />"
        informacion += html.formHidden( 'Redirigir' , 'Perfil' , "ImportarCSV" )
        informacion += html.formSubmit( "aceptar" , "Importaciones" , "Importar" )
        informacion += "</fieldset>" 
        informacion += "</form>"
        return informacion
   
     
    def capturarCampos( self , redirigir ):
        recargarPagina = False
        
        if redirigir == "ImportarCSV":                
            fichero = request.files['Fichero']
            nombre = fichero.filename
            if 'Sustituir' in request.form: sustituir = True
            else: sustituir = False 
            ficheros.importarDatosCSV( fichero , nombre , sustituir )
            recargarPagina = True
                
        return recargarPagina

#-------------------------- Exportaciones -------------------------#

class Exportaciones(Seccion):
    
    def __init__( self ):   
        Seccion.__init__( self, 'Importaciones' , 'Exportaciones' , 'Exportación de Datos' , 2 , '>=' )
        
####################################################################    
#----------------------------- Filtros ----------------------------#
####################################################################

class Filtros(Seccion):
    
    def __init__( self ):   
        Seccion.__init__(self, 'Filtros' , 'Filtros' , 'Filtro' , 1 , '>=' )
        
    
    def generarFormulario( self ):
        seccion , subSeccion = secciones.Secciones().getParametros( 'Filtrar' ).split(';')
        if subSeccion in secciones.Secciones().secciones:
            informcion = secciones.Secciones().secciones[ subSeccion ].filtro.generarFormulario()
        else:
            informcion = secciones.Secciones().secciones[ seccion ].formularios[ subSeccion ].filtro.generarFormulario()   
        return informcion
    
    
    def capturarCampos( self , redirigir ):
        seccion , subSeccion = secciones.Secciones().getParametros( 'Filtrar' ).split(';')
        if subSeccion in secciones.Secciones().secciones:
            informcion = secciones.Secciones().secciones[ subSeccion ].filtro.capturarCampos( redirigir )
        else:
            informcion = secciones.Secciones().secciones[ seccion ].formularios[ subSeccion ].filtro.capturarCampos( redirigir ) 
        return informcion
        