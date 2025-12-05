# -*- coding: utf-8 -*-
import datetime

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from lib import HTML as html
from lib import Utils as utils
from lib import Ficheros as ficheros

from app import Sesion as sesion
from app import Seccion as secciones
from app import Filtro as filtro

####################################################################    
#--------------------------- FORMULARIOS --------------------------#
####################################################################

class Formulario:
    
    def __init__( self , pFormulario , pSubFormulario , pTitulo ):
        self.formulario = pFormulario
        self.subFormulario = pSubFormulario
        self.titulo = pTitulo
        self.accion = 'Tabla'
        self.parametros = ''
        self.filtro = None
        
    
    def setAccion( self , pAccion ): self.accion = pAccion
    
    
    def generarFormulario( self ):
        informacion = ''
        if   self.accion == 'Anadir': informacion += self.formularioAnadirEditar( )
        elif self.accion == 'Editar': informacion += self.formularioAnadirEditar( )
        else:                         informacion += self.formularioTabla( )
        return informacion 
        
    
    def formularioRedirigirCancelar( self ):
        informacion = "<br />"
        informacion += html.formHeader( "RedirigirTabla" , "Transacciones" , '/' , False )
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "RedirigirTabla" )
        informacion += html.formSubmit( "eliminar" , "Transacciones" , "Cancelar" )
        informacion += "</form>" 
        return informacion 
            
    
    def formularioRedirigirAnadir( self ):
        informacion = ""
        informacion += html.formHeader( "RedirigirAnadir" , "Transacciones" , '/' , False )
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , 'RedirigirAnadir' )
        informacion += html.formSubmit( 'aceptar' , 'Transacciones' , 'Añadir' )
        informacion += "</form>"               
        return informacion
    
    
    def formularioRedirigirEditar( self , pParametros ):
        informacion = ""
        informacion += html.formHeader( "RedirigirEditar" , "Transacciones" , '/' , False )
        informacion += html.formHidden( 'Parametros' , 'Transacciones' , pParametros )
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , 'RedirigirEditar' )
        informacion += html.formSubmit( 'editar' , 'Transacciones' , 'Editar' )
        informacion += "</form>"               
        return informacion
    
    
    def formularioRedirigirEliminar( self , pParametros ):
        informacion = ""
        informacion += html.formHeader( "RedirigirEliminar" , "Transacciones" , '/' , False )
        informacion += html.formHidden( 'Parametros' , 'Transacciones' , pParametros )
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , 'RedirigirEliminar' )
        informacion += html.formSubmit( 'eliminar' , 'Transacciones' , 'Eliminar' )
        informacion += "</form>"               
        return informacion 
    
    
    def formularioTabla( self ):
        mensaje = html.working( )
        secciones.Secciones().reportarError( mensaje )
        return "<p> " + mensaje + " </p>" 

    
    def formularioAnadirEditar( self ):
        mensaje = html.working( )
        secciones.Secciones().reportarError( mensaje )
        return "<p> " + mensaje + " </p>" 


    def capturarCampos( self ):
        mensaje = html.working( )
        secciones.Secciones().reportarError( mensaje )
        return False
    
    
    def capturarRedirigir( self , redirigir ):
        recargarPagina = False
        
        if redirigir == "RedirigirAnadir":
            self.accion ='Anadir'
            recargarPagina = True
        
        if redirigir == "RedirigirEditar":
            parametros = request.form['Parametros']
            self.parametros = parametros
            self.accion ='Editar'
            recargarPagina = True
         
        if redirigir == "RedirigirTabla":
            self.accion ='Tabla'
            recargarPagina = True
        
        return recargarPagina
    
####################################################################    
#----------------------------- Activos ----------------------------#
####################################################################


class Activos(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Activos' , 'Activos' , 'Gestión de Activos' )
        self.formularioDistribucion = Distribucion()
        self.formularioCategorizacion = Categorizacion()
        self.filtro = filtro.Filtro( 'Gestion' , 'Activos' )
        
        
    def inicializarFiltro( self ):
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        activos = sesion.Sesion().getActivos()
        for isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia in activos:
             opciones.append( ( isin , descripcion , False ) )     
        self.filtro.anadirCampo( 'ISIN' , 'ISIN' , opciones , 'Identificador único del Activo buscado' )
        
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        opciones.append( ( 'Accion' , 'Accion' , False ) ) 
        opciones.append( ( 'Fondo' , 'Fondo' , False ) ) 
        opciones.append( ( 'ETF' , 'ETF' , False ) ) 
        self.filtro.anadirCampo( 'Producto' , 'Producto' , opciones , 'Permite filtrar los activos por Producto' )
        
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        estrategias = sesion.Sesion().getEstrategias()
        for estrategia , color , descripcion in estrategias:
            opciones.append( ( estrategia , estrategia , False ) )
        self.filtro.anadirCampo( 'Estrategia' , 'Estrategia' , opciones , 'Permite filtrar los activos por Estrategia' )
        
        
    def formularioTabla( self ):
        self.inicializarFiltro()
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        vIsin = self.filtro.campos[ 'ISIN' ].getValor() 
        vProducto = self.filtro.campos[ 'Producto' ].getValor() 
        vEstrategia = self.filtro.campos[ 'Estrategia' ].getValor()
        
        activos = sesion.Sesion().getActivosBy( vIsin , vProducto , vEstrategia , self.filtro.orden )
        
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarISIN' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'ISIN' , 'ISIN' ) + "    </th>"
        informacion += "       <th> Descripción </th>"
        informacion += "       <th> Color </th>"
        informacion += "       <th> Precio      </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarProducto' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Producto' , 'Producto' ) + "     </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarEstrategia' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Estrategia' , 'Estrategia' ) + "     </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()  + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        
        for isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia in activos:
            print( "COLOR: " + color )
            informacion += "   <tr>"
            informacion += "       <td> " + isin        + " </td>"
            informacion += "       <td> <a rel='author' href='https://es.finance.yahoo.com/quote/" + link + "?p=" + link + "' target='blank'>"  + descripcion + " </a> </td>"
            informacion += "       <td> " + html.formInput( "Color" , "Transacciones" , "" , "color" , '#000000 ' , "Color asignado al SubAllocation" , utils.colorRGBToHexadecimal( color ) , False ) + " </td>"
            informacion += "       <td> " + html.representarNumero( precio , False ) + " " + moneda + " </td>"
            informacion += "       <td> " + tipo_producto + " </td>"
            informacion += "       <td> " + estrategia + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( isin ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( isin ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
    
    
    def formularioAnadirEditar( self ):
        informacion = ""
        informacion += self.formularioAnadirEditarActivos( )
        if self.accion == 'Editar':
            informacion += "<br /> <br />"
            informacion += self.formularioDistribucion.generarFormulario( )
            informacion += "<br /> <br />"
            informacion += self.formularioCategorizacion.generarFormulario( )
            if self.formularioDistribucion.accion == 'Tabla' and self.formularioCategorizacion.accion == 'Tabla': 
                informacion += self.formularioRedirigirCancelar()
        
        if self.formularioDistribucion.accion == 'Editar' or self.formularioDistribucion.accion == 'Anadir':
            informacion = ""
            informacion += self.formularioDistribucion.generarFormulario( )
            
        if self.formularioCategorizacion.accion == 'Editar' or self.formularioCategorizacion.accion == 'Anadir':
            informacion = ""
            informacion += self.formularioCategorizacion.generarFormulario( )   
        
        return informacion
    
    
    def formularioAnadirEditarActivos( self ):
        pIsin = "" ; pDescripcion = "" ; pColor = "rgba( 250 ,  250  ,  250  , 1 )" ; pEmisor = "" ; pMoneda = "" ; pFuente = "" ; pLink = "" ; pTipoProducto = "" ; pDescripcionTipoProducto = "" ; pEstrategia = "" ;
        titulo = "Formulario para Crear Activos"
        if self.accion == 'Editar':
            pIsin , pTipoProducto , pEmisor , pFuente , pLink , pMoneda , pDescripcion , pColor , pPrecio , pDescripcionTipoProducto , pEstrategia = sesion.Sesion().getActivo( self.parametros )
            titulo = "Formulario para Editar el Activo " + pIsin
            self.formularioDistribucion.setIsin( pIsin )
            self.formularioCategorizacion.setIsin( pIsin )
            
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        if self.accion == 'Anadir': 
            informacion += html.formInput( "ISIN" , "Transacciones" , "ISIN" , "text" , "IE00B03HD191" , "Identificador único oficial del producto financiero" , pIsin , False )
            informacion += "<br /> <br />"
        if self.accion == 'Editar':
            informacion += html.formHidden( 'ISIN' , 'Transacciones' , pIsin )
        informacion += html.formInput( "Descripcion" , "Transacciones" , "Descripción" , "text" , "Nombre completo del producto financiero" , "Nombre completo del producto financiero" , pDescripcion , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Color" , "Transacciones" , "Color" , "color" , '#000000 ' , "Color asignado" , utils.colorRGBToHexadecimal( pColor ) , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Emisor" , "Transacciones" , "Emisor" , "text" , "Vanguard" , "Nombre de la comercializadora que ofrece el producto. No confundir con el banco custodio." , pEmisor , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Moneda" , "Transacciones" , "Moneda" , "text" , "EUR" , "Moneda en la que se comercializa el producto" , pMoneda , False )
        informacion += "<br /> <br />"
        
        opciones = []
        opciones.append( ( 'MorningStar' , 'MorningStar' , ( pFuente == 'MorningStar' ) ) )
        opciones.append( ( 'YahooFinance' , 'YahooFinance' , ( pFuente == 'YahooFinance' ) ) )
        informacion += html.formOptionList( 'FuenteDatos' , 'Transacciones' , 'Fuente de datos' , opciones , False )
        informacion += "<br /> <br />"
        
        informacion += html.formInput( "Link" , "Transacciones" , "Enlace a la fuente de datos" , "text" , "F0GBR052TN" , "Identificador único de MorningStar del producto financiero" , pLink , False )
        informacion += "<br /> <br />"
        
        opciones = []
        opciones.append( ( 'Accion' , 'Acción' , ( pTipoProducto == 'Accion' ) ) )
        opciones.append( ( 'ETF' , 'ETF' , ( pTipoProducto == 'ETF' ) ) )
        opciones.append( ( 'Fondo' , 'Fondo' , ( pTipoProducto == 'Fondo' ) ) )
        informacion += html.formOptionList( 'TipoProducto' , 'Transacciones' , 'Tipo' , opciones , False )
        informacion += "<br /> <br />"
        
        opciones = []
        productos = sesion.Sesion().getProductos()
        for producto , color , descripcion in productos:
            opciones.append( ( producto , producto , ( pDescripcionTipoProducto == producto ) ) )
        informacion += html.formOptionList( 'DescripcionTipoProducto' , 'Transacciones' , 'Categoría' , opciones , False )
        informacion += "<br /> <br />"
        
        opciones = []
        estrategias = sesion.Sesion().getEstrategias()
        for estrategia , color , descripcion in estrategias:
            opciones.append( ( estrategia , estrategia , ( pEstrategia == estrategia ) ) )
        informacion += html.formOptionList( 'Estrategia' , 'Transacciones' , 'Estrategia' , opciones , False )
        
        informacion += "<br /> <br />"
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"   
        return informacion 
    
    
    def capturarCampos( self , redirigir ):
        subFormulario = request.form['SubFormulario']
        if subFormulario == 'Activos': self.capturarCamposActivos( redirigir )
        if subFormulario == 'Distribucion': self.formularioDistribucion.capturarCampos( redirigir )
        if subFormulario == 'Categorizacion': self.formularioCategorizacion.capturarCampos( redirigir )
        
        
    def capturarCamposActivos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
         
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            sesion.Sesion().eliminarActivo( parametros )
            recargarPagina = True
                 
        if redirigir == "AnadirEditar":
            isin = request.form['ISIN']
            descripcion = request.form['Descripcion']
            color = request.form['Color']
            tipo_emisor = request.form['Emisor']
            moneda = request.form['Moneda']
            fuente = request.form['FuenteDatos']
            link = request.form['Link']
            tipo_producto = request.form['TipoProducto']
            producto = request.form['DescripcionTipoProducto']
            estrategia = request.form['Estrategia']
            if self.accion == 'Anadir': sesion.Sesion().anadirActivo( isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , utils.colorHexadecimalToRGB( color ) , producto , estrategia )
            if self.accion == 'Editar': sesion.Sesion().actualizarActivo( isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , utils.colorHexadecimalToRGB( color ) , producto , estrategia )
            self.accion = 'Tabla'
            recargarPagina = True
                 
        return recargarPagina
    
    
####################################################################    
#----------------------------- Cuentas ----------------------------#
####################################################################


class Cuentas(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Cuentas' , 'Cuentas' , 'Gestión de Cuentas' )
        self.filtro = filtro.Filtro( 'Gestion' , 'Cuentas' )
    
    
    def inicializarFiltro( self ):
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        cuentas = sesion.Sesion().getCuentasBy( '' ,  '' ,  '' , 'cuenta ASC' )
        for cuenta , color , descripcion , moneda , pais in cuentas: opciones.append( ( cuenta , cuenta , False ) )
        self.filtro.anadirCampo( 'Cuenta' , 'Cuenta' , opciones , 'Nombre de la cuenta buscada' )
        self.filtro.anadirCampo( 'Moneda' , 'Moneda' , 'text' , 'Permite filtrar las cuentas por Moneda' )
        self.filtro.anadirCampo( 'Pais' , 'Pais' , 'text' , 'Permite filtrar las cuentas por País' )
        
        
    def formularioTabla( self ):
        self.inicializarFiltro()
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        vCuenta = self.filtro.campos[ 'Cuenta' ].getValor() 
        vMoneda = self.filtro.campos[ 'Moneda' ].getValor()
        vPais = self.filtro.campos[ 'Pais' ].getValor()
        
        cuentas = sesion.Sesion().getCuentasBy( vCuenta , vMoneda , vPais , self.filtro.orden )
        
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarCuenta' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Cuenta' , 'Cuenta' ) + "    </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarMoneda' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Moneda' , 'Moneda' ) + "     </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarPais' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Pais' , 'Pais' ) + "     </th>"
        informacion += "       <th> Color      </th>"
        informacion += "       <th> Descripción </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()  + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        
        for cuenta , color , descripcion , moneda , pais in cuentas:
            informacion += "   <tr>"
            informacion += "       <td> " + cuenta        + " </td>"
            informacion += "       <td> " + moneda + " </td>"
            informacion += "       <td> " + pais   + " </td>"
            informacion += "       <td> " + html.formInput( "Color" , "Transacciones" , "" , "color" , '#000000 ' , "Color asignado al SubAllocation" , utils.colorRGBToHexadecimal( color ) , False ) + " </td>"
            informacion += "       <td> " + str(descripcion) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( cuenta ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( cuenta ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
    
        
    def formularioAnadirEditar( self ):
        pCuenta = "" ; pColor = "rgba( 250 ,  250  ,  250  , 1 )" ; pDescripcion = "" ; pMoneda = "" ; pPais = "" ; 
        titulo = "Formulario para Crear Cuentas"
        if self.accion == 'Editar':
            pCuenta , pColor , pDescripcion , pMoneda , pPais = sesion.Sesion().getCuenta( self.parametros )
            titulo = "Formulario para Editar la Cuenta " + pCuenta
            
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        if self.accion == 'Anadir': 
            informacion += html.formInput( "Cuenta" , "Transacciones" , "Cuenta" , "text" , "Bankia" , "Identificador único de la cuenta" , pCuenta , False )
            informacion += "<br /> <br />"
        
        if self.accion == 'Editar':
            informacion += html.formHidden( 'Cuenta' , 'Transacciones' , pCuenta )
        
        informacion += html.formInput( "Descripcion" , "Transacciones" , "Descripción" , "text" , "Fondo de emergencia" , "Nombre completo de la cuenta" , str( pDescripcion ) , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Pais" , "Transacciones" , "País" , "text" , "España" , "Nacionalidad de la cuenta" , pPais , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Moneda" , "Transacciones" , "Moneda" , "text" , "EUR" , "Moneda en que se gestiona la cuenta" , pMoneda , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Color" , "Transacciones" , "Color" , "color" , '#000000 ' , "Color asignado al SubAllocation" , utils.colorRGBToHexadecimal( pColor ) , False )
        informacion += "<br /> <br />"
 
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion 
    
    
    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
         
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            sesion.Sesion().eliminarCuenta( parametros )
            recargarPagina = True
                 
        if redirigir == "AnadirEditar":
            cuenta = request.form['Cuenta']
            descripcion = request.form['Descripcion']
            pais = request.form['Pais']
            moneda = request.form['Moneda']
            color = request.form['Color']
            if self.accion == 'Anadir': sesion.Sesion().anadirCuenta( cuenta , utils.colorHexadecimalToRGB( color ) , descripcion , moneda , pais )
            if self.accion == 'Editar': sesion.Sesion().actualizarCuenta( cuenta , utils.colorHexadecimalToRGB( color ) , descripcion , moneda , pais )
            self.accion = 'Tabla'
            recargarPagina = True
                 
        return recargarPagina        
  
      
####################################################################    
#---------------------------- Categorias --------------------------#
####################################################################
    
#--------------------------- Estrategias --------------------------#


class Estrategias(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Categorias' , 'Estrategias' , 'Gestión de Estrategias' )
        self.filtro = filtro.Filtro( 'Gestion' , 'Estrategias' )
        self.filtro.anadirCampo( 'Estrategia' , 'Estrategia' , 'text' , 'Nombre de la Estrategia buscada' )
        
        
    def formularioTabla( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        estrategias = sesion.Sesion().getEstrategiasBy( self.filtro.campos[ 'Estrategia' ].getValor() , self.filtro.orden )
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarEstrategia' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Estrategia' , 'Estrategia' ) + "     </th>"
        informacion += "       <th> Color      </th>"
        informacion += "       <th> Descripción </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()  + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        
        for estrategia , color , descripcion in estrategias:
            informacion += "   <tr>"
            informacion += "       <td> " + estrategia        + " </td>"
            informacion += "       <td> " + html.formInput( "Color" , "Transacciones" , "" , "color" , '#000000 ' , "Color asignado" , utils.colorRGBToHexadecimal( color ) , False ) + " </td>"
            informacion += "       <td> " + str(descripcion) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( estrategia ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( estrategia ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
    
        
    def formularioAnadirEditar( self ):
        pEstrategia = "" ; pColor = "rgba( 250 ,  250  ,  250  , 1 )" ; pDescripcion = "" ; 
        titulo = "Formulario para Crear Estrategias"
        if self.accion == 'Editar':
            pEstrategia , pColor , pDescripcion = sesion.Sesion().getEstrategia( self.parametros )
            titulo = "Formulario para Editar la Estrategia " + pEstrategia
            
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        if self.accion == 'Anadir': 
            informacion += html.formInput( "Estrategia" , "Transacciones" , "Estrategia" , "text" , "Boogle" , "Identificador único de la Estrategia" , pEstrategia , False )
            informacion += "<br /> <br />"
        
        if self.accion == 'Editar':
            informacion += html.formHidden( 'Estrategia' , 'Transacciones' , pEstrategia )
        
        informacion += html.formInput( "Descripcion" , "Transacciones" , "Descripción" , "text" , "Consiste en equilibrar renta Fija y renta Variable" , "Nombre completo de la estrategia" , str( pDescripcion ) , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Color" , "Transacciones" , "Color" , "color" , '#000000 ' , "Color asignado" , utils.colorRGBToHexadecimal( pColor ) , False )
        informacion += "<br /> <br />"
 
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion 
    
    
    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
         
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            sesion.Sesion().eliminarEstrategia( parametros )
            recargarPagina = True
                 
        if redirigir == "AnadirEditar":
            estrategia = request.form['Estrategia']
            descripcion = request.form['Descripcion']
            color = request.form['Color']
            if self.accion == 'Anadir': sesion.Sesion().anadirEstrategia( estrategia , utils.colorHexadecimalToRGB( color ) , descripcion )
            if self.accion == 'Editar': sesion.Sesion().actualizarEstrategia( estrategia , utils.colorHexadecimalToRGB( color ) , descripcion )
            self.accion = 'Tabla'
            recargarPagina = True
                 
        return recargarPagina         
    
        
#---------------------------- Categorias --------------------------#


class Categorias(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Categorias' , 'Categorias' , 'Gestión de Categorias' )
        self.filtro = filtro.Filtro( 'Gestion' , 'Categorias' )
        self.filtro.anadirCampo( 'Categoria' , 'Categoria' , 'text' , 'Nombre de la Categoria buscada' )
        
        
    def formularioTabla( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        categorias = sesion.Sesion().getCategoriasBy( self.filtro.campos[ 'Categoria' ].getValor() , self.filtro.orden )
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarCategorias' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Categoria' , 'Categoria' ) + "     </th>"
        informacion += "       <th> Color      </th>"
        informacion += "       <th> Descripción </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()  + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        
        for categoria , color , descripcion in categorias:
            informacion += "   <tr>"
            informacion += "       <td> " + categoria        + " </td>"
            informacion += "       <td> " + html.formInput( "Color" , "Transacciones" , "" , "color" , '#000000 ' , "Color asignado" , utils.colorRGBToHexadecimal( color ) , False ) + " </td>"
            informacion += "       <td> " + str(descripcion) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( categoria ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( categoria ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
    
        
    def formularioAnadirEditar( self ):
        pCategoria = "" ; pColor = "rgba( 250 ,  250  ,  250  , 1 )" ; pDescripcion = "" ; 
        titulo = "Formulario para Crear Estrategias"
        if self.accion == 'Editar':
            pCategoria , pColor , pDescripcion = sesion.Sesion().getCategoria( self.parametros )
            titulo = "Formulario para Editar la Categoria " + pCategoria
            
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        if self.accion == 'Anadir': 
            informacion += html.formInput( "Categoria" , "Transacciones" , "Categoria" , "text" , "Boogle" , "Identificador único de la Categoria" , pCategoria , False )
            informacion += "<br /> <br />"
        
        if self.accion == 'Editar':
            informacion += html.formHidden( 'Categoria' , 'Transacciones' , pCategoria )
        
        informacion += html.formInput( "Descripcion" , "Transacciones" , "Descripción" , "text" , "Consiste en equilibrar renta Fija y renta Variable" , "Nombre completo de la categoria" , str( pDescripcion ) , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Color" , "Transacciones" , "Color" , "color" , '#000000 ' , "Color asignado" , utils.colorRGBToHexadecimal( pColor ) , False )
        informacion += "<br /> <br />"
 
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion 
    
    
    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
         
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            sesion.Sesion().eliminarCategoria( parametros )
            recargarPagina = True
                 
        if redirigir == "AnadirEditar":
            categoria = request.form['Categoria']
            descripcion = request.form['Descripcion']
            color = request.form['Color']
            if self.accion == 'Anadir': sesion.Sesion().anadirCategoria( categoria , utils.colorHexadecimalToRGB( color ) , descripcion )
            if self.accion == 'Editar': sesion.Sesion().actualizarCategoria( categoria , utils.colorHexadecimalToRGB( color ) , descripcion )
            self.accion = 'Tabla'
            recargarPagina = True
                 
        return recargarPagina


#---------------------------- Productos ---------------------------#


class Productos(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Categorias' , 'Productos' , 'Gestión de Productos' )    
        self.filtro = filtro.Filtro( 'Gestion' , 'Productos' )
        self.filtro.anadirCampo( 'Producto' , 'Producto' , 'text' , 'Nombre del Producto buscado' )
        
        
    def formularioTabla( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        productos = sesion.Sesion().getProductosBy( self.filtro.campos[ 'Producto' ].getValor() , self.filtro.orden )
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarProductos' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Producto' , 'Producto' ) + "     </th>"
        informacion += "       <th> Color      </th>"
        informacion += "       <th> Descripción </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()  + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        
        for producto , color , descripcion in productos:
            informacion += "   <tr>"
            informacion += "       <td> " + producto        + " </td>"
            informacion += "       <td> " + html.formInput( "Color" , "Transacciones" , "" , "color" , '#000000 ' , "Color asignado" , utils.colorRGBToHexadecimal( color ) , False ) + " </td>"
            informacion += "       <td> " + str(descripcion) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( producto ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( producto ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
    
        
    def formularioAnadirEditar( self ):
        pCategoria = "" ; pColor = "rgba( 250 ,  250  ,  250  , 1 )" ; pDescripcion = "" ; 
        titulo = "Formulario para Crear Estrategias"
        if self.accion == 'Editar':
            pCategoria , pColor , pDescripcion = sesion.Sesion().getProducto( self.parametros )
            titulo = "Formulario para Editar la Producto " + pCategoria
            
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        if self.accion == 'Anadir': 
            informacion += html.formInput( "Producto" , "Transacciones" , "Producto" , "text" , "Boogle" , "Identificador único de la Producto" , pCategoria , False )
            informacion += "<br /> <br />"
        
        if self.accion == 'Editar':
            informacion += html.formHidden( 'Producto' , 'Transacciones' , pCategoria )
        
        informacion += html.formInput( "Descripcion" , "Transacciones" , "Descripción" , "text" , "Consiste en equilibrar renta Fija y renta Variable" , "Nombre completo de la categoria" , str( pDescripcion ) , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Color" , "Transacciones" , "Color" , "color" , '#000000 ' , "Color asignado" , utils.colorRGBToHexadecimal( pColor ) , False )
        informacion += "<br /> <br />"
 
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion 
    
    
    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
         
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            sesion.Sesion().eliminarProducto( parametros )
            recargarPagina = True
                 
        if redirigir == "AnadirEditar":
            producto = request.form['Producto']
            descripcion = request.form['Descripcion']
            color = request.form['Color']
            if self.accion == 'Anadir': sesion.Sesion().anadirProducto( producto , utils.colorHexadecimalToRGB( color ) , descripcion )
            if self.accion == 'Editar': sesion.Sesion().actualizarProducto( producto , utils.colorHexadecimalToRGB( color ) , descripcion )
            self.accion = 'Tabla'
            recargarPagina = True
                 
        return recargarPagina

        
#-------------------------- Categorizacion ------------------------#


class Categorizacion(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Categorias' , 'Categorizacion' , 'Asignación de Categorias' )
        self.isin = ''
        self.filtro = filtro.Filtro( 'Gestion' , 'Categorizacion' )
        self.filtro.anadirCampo( 'Categoria' , 'Categoria' , 'text' , 'Nombre de la Categoria buscada' )


    def setIsin( self , pISIN ): self.isin = pISIN
        
        
    def formularioTabla( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        categorizaciones = sesion.Sesion().getCategorizacionesBy( self.isin , self.filtro.orden )
        titulo = "Formulario para Editar los Categorias del Activo " + self.isin
        
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br /> <br />"
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarCategorizacion' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Categoria' , 'Categoria' ) + "    </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()     + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"

        for isin , categoria in categorizaciones:
            informacion += "   <tr>"
            informacion += "       <td> " + categoria + " </td>"
            informacion += "       <td>                        </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( categoria ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion        
        
        
    def formularioAnadirEditar( self ):
        titulo = "Formulario para Añadir Categorizaciones al Activo " + self.isin
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br /> <br />"
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        opciones = []
        categoriasTodas = []
        categorizacionesTodas = []
        categorizaciones = sesion.Sesion().getCategorizacionesBy( self.isin , 'Categoria ASC' )
        categorias = sesion.Sesion().getCategorias( )
        for categoria , color , descripcion in categorias: categoriasTodas.append( categoria )
        for isin , categoria in categorizaciones: categorizacionesTodas.append( categoria )   
        categorizaciones = utils.diferenciaListas( categoriasTodas , categorizacionesTodas )
        for categoria in categorizaciones: opciones.append( ( categoria , categoria , False ) )
        informacion += html.formOptionList( 'Categoria' , 'Transacciones' , 'Categoria' , opciones , False )
        informacion += "<br /> <br />"
            
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion
        
        
    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
    
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            sesion.Sesion().eliminarCategorizacion( self.isin , parametros )
            self.accion = 'Tabla'
            recargarPagina = True
       
        if redirigir == "AnadirEditar":
            categoria = request.form['Categoria']
            if self.accion == 'Anadir': sesion.Sesion().anadirCategorizacion( self.isin , categoria )
            self.accion = 'Tabla'
            recargarPagina = True

        return recargarPagina
    
    
####################################################################    
#-------------------------- Distribuciones ------------------------#
####################################################################
  
#---------------------------- Allocation --------------------------#


class Allocation(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Distribuciones' , 'Allocation' , 'Gestión de Allocations' )
        self.formularioSubAllocations = SubAllocation()
        self.filtro = filtro.Filtro( 'Gestion' , 'Allocation' )
        self.filtro.anadirCampo( 'Allocation' , 'Allocation' , 'text' , 'Nombre del Allocation buscado' )
    
    
    def formularioTabla( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        allocations = sesion.Sesion().getAllocationsBy( self.filtro.campos[ 'Allocation' ].getValor() , self.filtro.orden )
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarAllocation' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Allocation' , 'Allocation' ) + "    </th>"
        informacion += "       <th> Descripción  </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()     + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"

        for allocation , descripcion in allocations:
            informacion += "   <tr>"
            informacion += "       <td> " + allocation        + " </td>"
            informacion += "       <td> " + str(descripcion) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( allocation )   + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( allocation ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
        
    
    def formularioAnadirEditar( self ):
        informacion = ""
        if self.formularioSubAllocations.accion == 'Tabla': 
            informacion += self.formularioAnadirEditarAllocations( )
        if self.accion == 'Editar':
            informacion += "<br /> <br />"
            informacion +=  self.formularioSubAllocations.generarFormulario( )
        if self.formularioSubAllocations.accion == 'Tabla': 
            informacion += self.formularioRedirigirCancelar() 
        return informacion
    
    
    def formularioAnadirEditarAllocations( self ):
        pAllocation = "" ; pDescripcion = "" ;
        titulo = "Formulario para Crear Allocations"
        if self.accion == 'Editar':
            pAllocation , pDescripcion = sesion.Sesion().getAllocation( self.parametros )
            titulo = "Formulario para Editar el Allocation " + pAllocation
            self.formularioSubAllocations.setAllocation( pAllocation )
        
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br /> <br />"
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        if self.accion == 'Anadir':
            informacion += html.formInput( "Allocation" , "Transacciones" , "Allocation" , "text" , "Region" , "Identificador único del Allocation" , pAllocation , False )
            informacion += "<br /> <br />"
        if self.accion == 'Editar':
            informacion += html.formHidden( "Allocation" , "Transacciones" , pAllocation )
        informacion += html.formInput( "Descripcion" , "Transacciones" , "Descripción" , "text" , "Permite agrupar los activos por zonas geográficas" , "Descripción de las características comunes de los activos que contiene" , str(pDescripcion) , False )
        informacion += "<br /> <br />"
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        return informacion
    
    
    def capturarCampos( self , redirigir ):
        subFormulario = request.form['SubFormulario']
        if subFormulario == 'Allocation': self.capturarCamposAllocations( redirigir )
        if subFormulario == 'SubAllocation': self.formularioSubAllocations.capturarCampos( redirigir )
        
        
    def capturarCamposAllocations( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
        
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            sesion.Sesion().eliminarAllocation( parametros )
            recargarPagina = True

        if redirigir == "AnadirEditar":
            allocation = request.form['Allocation']
            descripcion = request.form['Descripcion']
            if self.accion == 'Anadir': sesion.Sesion().anadirAllocation( allocation , descripcion )
            if self.accion == 'Editar': sesion.Sesion().actualizarAllocation( allocation , descripcion )
            self.accion = 'Tabla'
            recargarPagina = True

        return recargarPagina


#-------------------------- Sub Allocation -------------------------#


class SubAllocation(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Distribuciones' , 'SubAllocation' , 'Gestión de Sub-Allocations' )
        self.allocation = ''
        self.filtro = filtro.Filtro( 'Gestion' , 'SubAllocation' )
        self.filtro.anadirCampo( 'SubAllocation' , 'SubAllocation' , 'text' , 'Nombre del SubAllocation buscado' ) 


    def setAllocation( self , pAllocation ): self.allocation = pAllocation


    def formularioTabla( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        subAllocations = sesion.Sesion().getSubAllocationsBy( self.allocation , self.filtro.campos[ 'SubAllocation' ].getValor() , self.filtro.orden )
        titulo = "Formulario para Editar los SubAllocation del Allocation " + self.allocation
        
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br /> <br />"
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarSubAllocation' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'SubAllocation' , 'SubAllocation' ) + "    </th>"
        informacion += "       <th> Descripción  </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()     + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"

        for subAllocation , color , allocation in subAllocations:
            informacion += "   <tr>"
            informacion += "       <td> " + subAllocation        + " </td>"
            informacion += "       <td> " + html.formInput( "Color" , "Transacciones" , "" , "color" , '#000000 ' , "Color asignado al SubAllocation" , utils.colorRGBToHexadecimal( color ) , False ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( subAllocation )   + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( subAllocation ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
    
    
    def formularioAnadirEditar( self ):
        pSubAllocation = "" ; pColor = "rgba( 250 ,  250  ,  250  , 1 )" ;
        titulo = "Formulario para Crear SubAllocations del Allocation " + self.allocation
        if self.accion == 'Editar':
            pSubAllocation , pColor , pAllocation = sesion.Sesion().getSubAllocation( self.parametros )
            titulo = "Formulario para Editar el subAllocation " + pSubAllocation + " del Allocation " + self.allocation
            
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br /> <br />"
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        if self.accion == 'Anadir':
            informacion += html.formInput( "SubAllocation" , "Transacciones" , "SubAllocation" , "text" , "Region" , "Identificador único del SubAllocation" , pSubAllocation , False )
            informacion += "<br /> <br />"
        if self.accion == 'Editar':
            informacion += html.formHidden( "SubAllocation" , "Transacciones" , pSubAllocation )
        informacion += html.formInput( "Color" , "Transacciones" , "Color" , "color" , '#000000 ' , "Color asignado al SubAllocation" , utils.colorRGBToHexadecimal( pColor ) , False )
        informacion += "<br /> <br />"
        informacion += html.formHidden( "Allocation" , "Transacciones" , self.allocation )
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion


    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
        
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            sesion.Sesion().eliminarSubAllocation( parametros )
            recargarPagina = True
       
        if redirigir == "AnadirEditar":
            allocation = request.form['Allocation']
            subAllocation = request.form['SubAllocation']
            color = request.form['Color']
            if self.accion == 'Anadir': sesion.Sesion().anadirSubAllocation( allocation , subAllocation , utils.colorHexadecimalToRGB( color ) )
            if self.accion == 'Editar': sesion.Sesion().actualizarSubAllocation( allocation , subAllocation , utils.colorHexadecimalToRGB( color ) )
            self.accion = 'Tabla'
            recargarPagina = True

        return recargarPagina

    
#--------------------------- Clasificacion -------------------------#


class Clasificacion(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Distribuciones' , 'Clasificacion' , 'Gestión de Clasificaciones' )
        self.formularioSubClasificacion = SubClasificacion()
        self.filtro = filtro.Filtro( 'Gestion' , 'Clasificacion' )
        self.filtro.anadirCampo( 'Clasificacion' , 'Clasificacion' , 'text' , 'Nombre de la Clasificacion buscada' )


    def formularioTabla( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        clasificaciones = sesion.Sesion().getClasificacionesBy( self.filtro.campos[ 'Clasificacion' ].getValor() , self.filtro.orden )
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarClasificacion' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'clasificacion' , 'Clasificación' ) + "    </th>"
        informacion += "       <th> Descripción  </th>"
        informacion += "       <th> Color  </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()     + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"

        for clasificacion , color , descripcion in clasificaciones:
            informacion += "   <tr>"
            informacion += "       <td> " + clasificacion        + " </td>"
            informacion += "       <td> " + str(descripcion) + " </td>"
            informacion += "       <td> " + html.formInput( "Color" , "Transacciones" , "" , "color" , '#000000 ' , "Color asignado a la clasificación" , utils.colorRGBToHexadecimal( color ) , False ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( clasificacion )   + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( clasificacion ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion


    def formularioAnadirEditar( self ):
        informacion = ""
        if self.formularioSubClasificacion.accion == 'Tabla': 
            informacion += self.formularioAnadirEditarClasificaciones( )
        if self.accion == 'Editar':
            informacion += "<br /> <br />"
            informacion +=  self.formularioSubClasificacion.generarFormulario( )
        if self.formularioSubClasificacion.accion == 'Tabla': 
            informacion += self.formularioRedirigirCancelar() 
        return informacion
    
    
    def formularioAnadirEditarClasificaciones( self ):
        pClasificacion = "" ; pDescripcion = "" ; pColor = "rgba( 250 ,  250  ,  250  , 1 )" ;
        titulo = "Formulario para Crear Clasificaciones"
        if self.accion == 'Editar':
            pClasificacion , pColor , pDescripcion = sesion.Sesion().getClasificacion( self.parametros )
            titulo = "Formulario para Editar la Clasificación " + pClasificacion
            self.formularioSubClasificacion.setClasificacion( pClasificacion )
        
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br /> <br />"
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        if self.accion == 'Anadir':
            informacion += html.formInput( "Clasificacion" , "Transacciones" , "Clasificación" , "text" , "Transporte" , "Identificador único de la Clasificación" , pClasificacion , False )
            informacion += "<br /> <br />"
        if self.accion == 'Editar':
            informacion += html.formHidden( "Clasificacion" , "Transacciones" , pClasificacion )
        informacion += html.formInput( "Descripcion" , "Transacciones" , "Descripción" , "text" , "Permite agrupar los gastos de trasporte" , "Descripción de las características comunes de los gastos que contiene" , str(pDescripcion) , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Color" , "Transacciones" , "Color" , "color" , '#000000 ' , "Color asignado a la Clasificación" , utils.colorRGBToHexadecimal( pColor ) , False )
        informacion += "<br /> <br />"
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        return informacion


    def capturarCampos( self , redirigir ):
        subFormulario = request.form['SubFormulario']
        if subFormulario == 'Clasificacion': self.capturarCamposClasificaciones( redirigir )
        if subFormulario == 'SubClasificacion': self.formularioSubClasificacion.capturarCampos( redirigir )
        
        
    def capturarCamposClasificaciones( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
        
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            sesion.Sesion().eliminarClasificacion( parametros )
            recargarPagina = True

        if redirigir == "AnadirEditar":
            clasificacion = request.form['Clasificacion']
            color = request.form['Color']
            descripcion = request.form['Descripcion']
            if self.accion == 'Anadir': sesion.Sesion().anadirClasificacion( clasificacion , utils.colorHexadecimalToRGB( color ) , descripcion )
            if self.accion == 'Editar': sesion.Sesion().actualizarClasificacion( clasificacion , utils.colorHexadecimalToRGB( color ) , descripcion )
            self.accion = 'Tabla'
            recargarPagina = True

        return recargarPagina


#-------------------------- Sub Clasificacion -------------------------#


class SubClasificacion(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Distribuciones' , 'SubClasificacion' , 'Gestión de Sub-Clasificaciones' )
        self.clasificacion = ''
        self.filtro = filtro.Filtro( 'Gestion' , 'SubClasificacion' )
        self.filtro.anadirCampo( 'SubClasificacion' , 'SubClasificacion' , 'text' , 'Nombre de la SubClasificación buscada' )


    def setClasificacion( self , pClasificacion ): self.clasificacion = pClasificacion


    def formularioTabla( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        subClasificaciones = sesion.Sesion().getSubClasificacionesBy( self.clasificacion , self.filtro.campos[ 'SubClasificacion' ].getValor() , self.filtro.orden )
        titulo = "Formulario para Editar las SubClasificaciones de la clasificación " + self.clasificacion
        
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br /> <br />"
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarSubClasificacion' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'SubClasificacion' , 'Sub-Clasificacion' ) + "    </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()     + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"

        for subClasificacion , clasificacion in subClasificaciones:
            informacion += "   <tr>"
            informacion += "       <td> " + subClasificacion        + " </td>"
            informacion += "       <td>                                 </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( subClasificacion ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion


    def formularioAnadirEditar( self ):
        pSubClasificacion = "" ;
        titulo = "Formulario para Crear SubClasificaciones de la Clasificación " + self.clasificacion
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br /> <br />"
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        informacion += html.formInput( "SubClasificacion" , "Transacciones" , "SubClasificacion" , "text" , "Region" , "Identificador único de la SubClasificación" , pSubClasificacion , False )
        informacion += "<br /> <br />"
        informacion += html.formHidden( "Clasificacion" , "Transacciones" , self.clasificacion )
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion


    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
        
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            sesion.Sesion().eliminarSubClasificacion( parametros )
            recargarPagina = True
       
        if redirigir == "AnadirEditar":
            clasificacion = request.form['Clasificacion']
            subClasificacion = request.form['SubClasificacion']
            sesion.Sesion().anadirSubClasificacion( clasificacion , subClasificacion )
            self.accion = 'Tabla'
            recargarPagina = True

        return recargarPagina


#--------------------------- Distribucion --------------------------#


class Distribucion(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Distribuciones' , 'Distribucion' , 'Asignacion de Allocations' )
        self.isin = ''
        self.filtro = filtro.Filtro( 'Gestion' , 'Distribucion' )
        self.filtro.anadirCampo( 'Allocation' , 'Allocation' , 'text' , 'Nombre del Allocation buscado' )


    def setIsin( self , pISIN ): self.isin = pISIN


    def formularioTabla( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        allocations = sesion.Sesion().getAllocationsOf( self.isin , self.filtro.orden )
        titulo = "Formulario para Editar los sub-Allocations del Activo " + self.isin
        
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br /> <br />"
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarAllocation' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Allocation' , 'Allocation' ) + "    </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()     + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"

        for allocation in allocations:
            informacion += "   <tr>"
            informacion += "       <td> " + allocation        + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( self.isin + "/" + allocation ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( self.isin + "/" + allocation ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion


    def formularioAnadirEditar( self ):
        informacion = ''
        if self.accion == 'Anadir': informacion += self.formularioAnadir()
        if self.accion == 'Editar': informacion += self.formularioEditar()
        return informacion
    
    
    def formularioAnadir( self ):
        titulo = "Formulario para Añadir Allocations al Activo " + self.isin
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br /> <br />"
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        opciones = []
        allocationsTodas = []
        allocationsOf = sesion.Sesion().getAllocationsOf( self.isin , 'Allocation ASC' )
        allocationsBy = sesion.Sesion().getAllocationsBy( '' , 'Allocation ASC' )
        for allocation , descripcion in allocationsBy: allocationsTodas.append( allocation )
        allocations = utils.diferenciaListas( allocationsTodas , allocationsOf )
        for allocation in allocations: opciones.append( ( allocation , allocation , False ) )
        informacion += html.formOptionList( 'Allocation' , 'Transacciones' , 'Allocation' , opciones , False )
        informacion += "<br /> <br />"
        
        informacion += html.formHidden( "ISIN" , "Transacciones" , self.isin )
        
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion


    def formularioEditar( self ):
        isin , allocation = self.parametros.split('/')
        titulo = "Formulario para Editar el Sub-Allocation " + allocation + " del Activo " + self.isin
        subAllocations = sesion.Sesion().getSubAllocationsOf( allocation , isin , self.filtro.orden )
        
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        for isin , subAllocation , porcentaje in subAllocations:
            informacion += html.formInput( subAllocation , "Transacciones" , subAllocation , "number" , str(porcentaje) , "Peso del allocation " + allocation + " para el Sub-Allocation " + subAllocation , str(porcentaje) , False )
            informacion += "<br /> <br />"
        
        informacion += html.formHidden( "ISIN" , "Transacciones" , self.isin )
        informacion += html.formHidden( 'Allocation' , 'Transacciones' , allocation )
        
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion


    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
        
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            isin , allocation = parametros.split('/')
            subAllocations = sesion.Sesion().getSubAllocationsBy( allocation , '' , 'subAllocation ASC' )
            for subAllocation , color , allocation in subAllocations:
                sesion.Sesion().eliminarDistribucion( isin , subAllocation )
            self.accion = 'Tabla'
            recargarPagina = True
       
        if redirigir == "AnadirEditar":
            isin = request.form['ISIN']
            allocation = request.form['Allocation']
            subAllocations = sesion.Sesion().getSubAllocationsBy( allocation , '' , 'subAllocation ASC' )
            for subAllocation , color , allocation in subAllocations:
                if self.accion == 'Anadir': sesion.Sesion().anadirDistribucion( isin , subAllocation , 0 )
                if self.accion == 'Editar': sesion.Sesion().actualizarDistribucion( isin , subAllocation , request.form[ subAllocation ] )
            self.accion = 'Tabla'
            recargarPagina = True

        return recargarPagina
        
####################################################################    
#--------------------------- Operaciones --------------------------#
####################################################################

#-------------------------- Transacciones -------------------------#


class Transacciones(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Operaciones' , 'Transacciones' , 'Gestión de Transacciones' )
        self.filtro = filtro.Filtro( 'Gestion' , 'Transacciones' )
        
        
    def inicializarFiltro( self ):
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        cuentas = sesion.Sesion().getCuentasBy( '' ,  '' ,  '' , 'cuenta ASC' )
        for cuenta , color , descripcion , moneda , pais in cuentas: opciones.append( ( cuenta , cuenta , False ) ) 
        self.filtro.anadirCampo( 'Cuenta' , 'Cuenta' , opciones , 'Nombre de la Cuenta buscada' )
        
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        subClasificaciones = sesion.Sesion().getSubClasificacionesBy( '' , '' , 'CLASIFICACION ASC' )
        for subClasificacion , clasificacion  in subClasificaciones: opciones.append( ( subClasificacion , clasificacion + "   --->   " + subClasificacion , False ) )
        self.filtro.anadirCampo( 'SubClasificacion' , 'SubClasificacion' , opciones , 'Filtrar por la SubClasificación de la transacción' )
        
        self.filtro.anadirCampo( 'FechaInicio' , 'Fecha Inicio' , 'date' , 'Filtrar por fechas superiores a la seleccionada'  )
        self.filtro.anadirCampo( 'FechaFin' , 'Fecha Fin' , 'date' , 'Filtrar por fechas inferiores a la seleccionada'  )


    def formularioTabla( self ):
        self.inicializarFiltro()
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        vFechaInicio = self.filtro.campos[ 'FechaInicio' ].getValor()
        vFechaFin = self.filtro.campos[ 'FechaFin' ].getValor()
        vCuenta = self.filtro.campos[ 'Cuenta' ].getValor()
        vSubClasificacion = self.filtro.campos[ 'SubClasificacion' ].getValor()
        
        transacciones = sesion.Sesion().getTransaccionesBy( vFechaInicio , vFechaFin , vCuenta , vSubClasificacion , self.filtro.orden )
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarFecha' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Fecha' , 'Fecha' ) + "    </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarCuenta' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Cuenta' , 'Cuenta' ) + "     </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarSubClasificacion' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'SubClasificacion' , 'Sub-Clasificación' ) + "     </th>"
        informacion += "       <th> Gasto        </th>"
        informacion += "       <th> Ingreso        </th>"
        informacion += "       <th> Descripción   </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()  + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        
        for cuenta , subClasificacion , fecha , gasto , ingreso , faborita , descripcion in transacciones:
            informacion += "   <tr>"
            informacion += "       <td> " + html.formInput( "Fecha" , "Transacciones" , '' , "date" , str(datetime.datetime.now().date()) , "Fecha en la que se realiza el Traspaso" , str(fecha) , False )        + " </td>"
            informacion += "       <td> " + cuenta + " </td>"
            informacion += "       <td> " + subClasificacion + " </td>"
            informacion += "       <td> " + html.representarNumero( -gasto , True ) + " </td>"
            informacion += "       <td> " + html.representarNumero( ingreso , True ) + " </td>"
            informacion += "       <td> " + str(descripcion) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( cuenta + '/' + subClasificacion + '/' + str(fecha) ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( cuenta + '/' + subClasificacion + '/' + str(fecha) ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
    
    
    def formularioAnadirEditar( self ):
        pCuenta = "" ; pSubClasificacion = "" ; pFecha = "" ; pGasto = "" ; pIngreso = "" ; pDescripcion = "" ;
        titulo = "Formulario para Crear Transacciones"
        if self.accion == 'Editar':
            pCuenta , pSubClasificacion , pFecha = self.parametros.split('/')
            pCuenta , pSubClasificacion , pFecha , pGasto , pIngreso , faborita , pDescripcion = sesion.Sesion().getTransaccion( str(pFecha) , pCuenta , pSubClasificacion )
            titulo = "Formulario para Editar la transaccion del " + str(pFecha) + ' de ' + pCuenta
            
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        if self.accion == 'Anadir': 
            informacion += html.formInput( "Fecha" , "Transacciones" , "Fecha" , "date" , str(datetime.datetime.now().date()) , "Fecha en la que se realiza el Traspaso" , str(pFecha) , False )
            informacion += "<br /> <br />"
            
            opciones = []
            cuentas = sesion.Sesion().getCuentasBy( '' ,  '' ,  '' , 'cuenta ASC' )
            for cuenta , color , descripcion , moneda , pais in cuentas: opciones.append( ( cuenta , cuenta , False ) )
            informacion += html.formOptionList( 'Cuenta' , 'Transacciones' , 'Cuenta de Origen' , opciones , False )
            informacion += "<br /> <br />"
            
            opciones = []
            subClasificaciones = sesion.Sesion().getSubClasificacionesBy( '' , '' , 'CLASIFICACION ASC' )
            for subClasificacion , clasificacion  in subClasificaciones: opciones.append( ( subClasificacion , clasificacion + "   --->   " + subClasificacion , False ) )
            informacion += html.formOptionList( 'subClasificacion' , 'Transacciones' , 'subClasificacion' , opciones , False )
            informacion += "<br /> <br />"
        
        if self.accion == 'Editar':
            informacion += html.formHidden( 'Fecha' , 'Transacciones' , str(pFecha) )
            informacion += html.formHidden( 'Cuenta' , 'Transacciones' , pCuenta )
            informacion += html.formHidden( 'subClasificacion' , 'Transacciones' , pSubClasificacion )
        
        informacion += html.formInput( "Gasto" , 'Transacciones' , "Gasto" , "float" , "15.5" , "Gasto que supone la transacción" , str(pGasto) , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Ingreso" , 'Transacciones' , "Ingreso" , "float" , "15.5" , "Ingreso percibido por la transacción" , str(pIngreso) , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Descripcion" , 'Transacciones' , "Descripción" , "text" , "Motivo de la transacción" , "Motivo de la transacción" , pDescripcion , False )
        informacion += "<br /> <br />"
        
        informacion += html.formCheckBox( 'Favorita' , 'Transacciones' , 'Marcar como favorita' , 'Si' )
        informacion += "<br /> <br />"
        
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion 
    
    
    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
         
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            cuenta , subClasificacion , fecha = parametros.split('/')
            sesion.Sesion().eliminarTransaccion( cuenta , subClasificacion , fecha )
            recargarPagina = True
                 
        if redirigir == "AnadirEditar":
            fecha = request.form['Fecha']
            cuenta = request.form['Cuenta']
            subClasificacion = request.form['subClasificacion']
            gasto = request.form['Gasto']
            ingreso = request.form['Ingreso']
            descripcion = request.form['Descripcion'] 
            if 'Favorita' in request.form: favorita = 'Si'
            else: favorita = 'No'
            if self.accion == 'Anadir': sesion.Sesion().anadirTransaccion( fecha , cuenta , '' , subClasificacion , gasto , ingreso , favorita , descripcion )
            if self.accion == 'Editar': sesion.Sesion().actualizarTransaccion( cuenta , subClasificacion , fecha , gasto , ingreso , favorita , descripcion )
            self.accion = 'Tabla'
            recargarPagina = True
                 
        return recargarPagina        
     
        
#-------------------------- Aportaciones --------------------------#


class Aportaciones(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Operaciones' , 'Aportaciones' , 'Gestión de Aportaciones' )       
        self.filtro = filtro.Filtro( 'Gestion' , 'Aportaciones' )
        
        
    def inicializarFiltro( self ):        
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        cuentas = sesion.Sesion().getCuentasBy( '' ,  '' ,  '' , 'cuenta ASC' )
        for cuenta , color , descripcion , moneda , pais in cuentas: opciones.append( ( cuenta , cuenta , False ) ) 
        self.filtro.anadirCampo( 'Cuenta' , 'Cuenta' , opciones , 'Filtrar las transacciones por cuentas' )
        
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        activos = sesion.Sesion().getActivos()
        for isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia in activos:
             opciones.append( ( isin , descripcion , False ) )    
        self.filtro.anadirCampo( 'ISIN' , 'ISIN' , opciones , 'Filtrar las transacciones por el ISIN del producto' )
        
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        opciones.append( ( "Compra" , "Compra " , False ) )
        opciones.append( ( "Venta" , "Venta " , False ) )
        self.filtro.anadirCampo( 'TIPO_OPERACION' , 'Tipo de Operacion' , opciones , 'Filtrar las transacciones por el tipo de operación' )
        
        self.filtro.anadirCampo( 'FechaInicio' , 'Fecha Inicio' , 'date' , 'Filtrar por fechas superiores a la seleccionada'  )
        self.filtro.anadirCampo( 'FechaFin' , 'Fecha Fin' , 'date' , 'Filtrar por fechas inferiores a la seleccionada'  )


    def formularioTabla( self ):
        self.inicializarFiltro()
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        vFechaInicio = self.filtro.campos[ 'FechaInicio' ].getValor()
        vFechaFin = self.filtro.campos[ 'FechaFin' ].getValor()
        vCuenta = self.filtro.campos[ 'Cuenta' ].getValor()
        vISIN = self.filtro.campos[ 'ISIN' ].getValor()
        vTipo = self.filtro.campos[ 'TIPO_OPERACION' ].getValor()
        
        aportaciones = sesion.Sesion().getAportacionesBy( vFechaInicio , vFechaFin , vCuenta , vISIN , vTipo , self.filtro.orden )
        
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarFecha' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Fecha' , 'Fecha' ) + "    </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarCuenta' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Cuenta' , 'Cuenta' ) + "     </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarISIN' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'ISIN' , 'ISIN' ) + "     </th>"
        informacion += "       <th> Precio       </th>"
        informacion += "       <th> Titulos     </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarTipo' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'TIPO_OPERACION' , 'Tipo' ) + "     </th>"
        informacion += "       <th> Descripción   </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()  + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        
        for isin , cuenta , fecha , precio , titulos , cambio , tipo , faborita , descripcion in aportaciones:
            informacion += "   <tr>"
            informacion += "       <td> " + html.formInput( "Fecha" , "Transacciones" , '' , "date" , str(datetime.datetime.now().date()) , "Fecha en la que se realiza el Traspaso" , str(fecha) , False )        + " </td>"
            informacion += "       <td> " + cuenta + " </td>"
            informacion += "       <td> " + isin + " </td>"
            informacion += "       <td> " + html.representarNumero( precio , True ) + " </td>"
            informacion += "       <td> " + html.representarNumero( titulos , False ) + " </td>"
            informacion += "       <td> " + tipo + " </td>"
            informacion += "       <td> " + str(descripcion) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( isin + '/' + cuenta + '/' + str(fecha) + '/' + tipo ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( isin + '/' + cuenta + '/' + str(fecha) + '/' + tipo  ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
    
    
    def formularioAnadirEditar( self ):
        pISIN = "" ; pCuenta = "" ; pFecha = "" ; pPrecio = "" ; pTitulos = "" ; pCambio = "" ; pTipo = "" ; pDescripcion = "" ;
        titulo = "Formulario para Crear Aportaciones"
        if self.accion == 'Editar':
            pISIN , pCuenta , pFecha , pTipo = self.parametros.split('/')
            pISIN , pCuenta , pFecha , pPrecio , pTitulos , pCambio , pTipo , faborita , pDescripcion = sesion.Sesion().getAportacion( str(pFecha) , pCuenta , pISIN , pTipo )
            titulo = "Formulario para Editar la aportacion del " + str(pFecha) + ' de ' + pCuenta + ', ' + pISIN
            
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        if self.accion == 'Anadir': 
            informacion += html.formInput( "Fecha" , "Transacciones" , "Fecha" , "date" , str(datetime.datetime.now().date()) , "Fecha en la que se realiza el Traspaso" , str(pFecha) , False )
            informacion += "<br /> <br />"
            
            opciones = []
            cuentas = sesion.Sesion().getCuentasBy( '' ,  '' ,  '' , 'cuenta ASC' )
            for cuenta , color , descripcion , moneda , pais in cuentas: opciones.append( ( cuenta , cuenta , False ) )
            informacion += html.formOptionList( 'Cuenta' , 'Transacciones' , 'Cuenta' , opciones , False )
            informacion += "<br /> <br />"
            
            opciones = []
            activos = sesion.Sesion().getActivos( )
            for isin , tipo , emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia in activos: opciones.append( ( isin , descripcion , False ) )
            informacion += html.formOptionList( 'ISIN' , 'Transacciones' , 'Activo comerciado' , opciones , False )
            informacion += "<br /> <br />"
            
            opciones = []
            opciones.append( ( "Compra" , "Compra " +  pCuenta , True ) )
            opciones.append( ( "Venta" , "Venta " +  pCuenta , True ) )
            informacion += html.formOptionList( 'Tipo' , 'Transacciones' , 'Tipo de comision comision' , opciones , False )
            informacion += "<br /> <br />"
        
        if self.accion == 'Editar':
            informacion += html.formHidden( 'Fecha' , 'Transacciones' , str(pFecha) )
            informacion += html.formHidden( 'Cuenta' , 'Transacciones' , pCuenta )
            informacion += html.formHidden( 'ISIN' , 'Transacciones' , pISIN )
            informacion += html.formHidden( 'Tipo' , 'Transacciones' , pTipo )
        
        informacion += html.formInput( "Precio" , 'Transacciones' , "Precio" , "float" , "15.5" , "Coste del activo negociado" , str(pPrecio) , False )
        informacion += "<br /> <br />"  
        informacion += html.formInput( "Titulos" , 'Transacciones' , "Titulos" , "float" , "15.5" , "Número de Valores comerciados" , str(pTitulos) , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Cambio" , 'Transacciones' , "Cambio Divisa" , "float" , "1" , "Si el activo está en una divisa distinta indique el tipo de cambio al que se realizó la transacción" , str(pCambio) , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Descripcion" , 'Transacciones' , "Descripción" , "text" , "Motivo de la adquisición o venta" , "Motivo de la adquisición o venta" , pDescripcion , False )
        informacion += "<br /> <br />"
        
        informacion += html.formCheckBox( 'Favorita' , 'Transacciones' , 'Marcar como favorita' , 'Si' )
        informacion += "<br /> <br />"
        
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion 
    
    
    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
         
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            isin , cuenta , fecha , tipo = parametros.split('/')
            sesion.Sesion().eliminarAportacion( isin , cuenta , tipo , fecha )
            recargarPagina = True
                 
        if redirigir == "AnadirEditar":
            fecha = request.form['Fecha']
            cuenta = request.form['Cuenta']
            isin = request.form['ISIN']
            tipo = request.form['Tipo']
            precio = request.form['Precio']
            titulos = request.form['Titulos']
            cambio = request.form['Cambio']
            descripcion = request.form['Descripcion']           
            if 'Favorita' in request.form: favorita = 'Si'
            else: favorita = 'No'
            if self.accion == 'Anadir': sesion.Sesion().anadirAportacion( fecha , cuenta , isin , tipo , precio , titulos , cambio , favorita , descripcion )
            if self.accion == 'Editar': sesion.Sesion().actualizarAportacion( isin , cuenta , fecha , precio , titulos , cambio , tipo , favorita , descripcion )
            self.accion = 'Tabla'
            recargarPagina = True
                 
        return recargarPagina


#---------------------------- Comisiones --------------------------#


class Comisiones(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Operaciones' , 'Comisiones' , 'Gestión de Comisiones' )
        self.filtro = filtro.Filtro( 'Gestion' , 'Comisiones' )
        
        
    def inicializarFiltro( self ): 
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        cuentas = sesion.Sesion().getCuentasBy( '' ,  '' ,  '' , 'cuenta ASC' )
        for cuenta , color , descripcion , moneda , pais in cuentas: opciones.append( ( cuenta , cuenta , False ) ) 
        self.filtro.anadirCampo( 'Cuenta' , 'Cuenta' , opciones , 'Filtra las comisiones por cuenta' )
        
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        activos = sesion.Sesion().getActivos()
        for isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia in activos:
             opciones.append( ( isin , descripcion , False ) )    
        self.filtro.anadirCampo( 'ISIN' , 'ISIN' , opciones , 'Filtra las comisiones por producto' )
        
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        opciones.append( ( "Comision" , "Comisión " , False ) )
        opciones.append( ( "Compensacion" , "Compensación " , False ) )
        opciones.append( ( "Dividendo" , "Dividendo " , False ) )
        opciones.append( ( "Impuesto" , "Impuesto " , False ) )
        opciones.append( ( "Interes" , "Interes " , False ) )
        self.filtro.anadirCampo( 'TIPO_OPERACION' , 'Tipo de Operación' , opciones , 'Filtrar las comisiones por el tipo de operación' )
        
        self.filtro.anadirCampo( 'FechaInicio' , 'Fecha Inicio' , 'date' , 'Filtrar por fechas superiores a la seleccionada'  )
        self.filtro.anadirCampo( 'FechaFin' , 'Fecha Fin' , 'date' , 'Filtrar por fechas inferiores a la seleccionada'  )


    def formularioTabla( self ):
        self.inicializarFiltro()
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        vFechaInicio = self.filtro.campos[ 'FechaInicio' ].getValor()
        vFechaFin = self.filtro.campos[ 'FechaFin' ].getValor()
        vCuenta = self.filtro.campos[ 'Cuenta' ].getValor()
        vISIN = self.filtro.campos[ 'ISIN' ].getValor()
        vTipo = self.filtro.campos[ 'TIPO_OPERACION' ].getValor()
        
        comisiones = sesion.Sesion().getComisionesBy( vFechaInicio , vFechaFin , vCuenta , vISIN , vTipo , self.filtro.orden )
        
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarFecha' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Fecha' , 'Fecha' ) + "    </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarCuenta' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Cuenta' , 'Cuenta' ) + "     </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarISIN' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'ISIN' , 'ISIN' ) + "     </th>"
        informacion += "       <th> Gasto       </th>"
        informacion += "       <th> Ingreso     </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarTipo' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'TIPO_OPERACION' , 'Tipo' ) + "     </th>"
        informacion += "       <th> Descripción   </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()  + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        
        for isin , cuenta , fecha , gasto , ingreso , tipo , faborita , descripcion in comisiones:
            informacion += "   <tr>"
            informacion += "       <td> " + html.formInput( "Fecha" , "Transacciones" , '' , "date" , str(datetime.datetime.now().date()) , "Fecha en la que se realiza el Traspaso" , str(fecha) , False )        + " </td>"
            informacion += "       <td> " + cuenta + " </td>"
            informacion += "       <td> " + isin + " </td>"
            informacion += "       <td> " + html.representarNumero( -gasto , True ) + " </td>"
            informacion += "       <td> " + html.representarNumero( ingreso , True ) + " </td>"
            informacion += "       <td> " + tipo + " </td>"
            informacion += "       <td> " + str(descripcion) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( isin + '/' + cuenta + '/' + str(fecha) + '/' + tipo ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( isin + '/' + cuenta + '/' + str(fecha) + '/' + tipo  ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
    
    
    def formularioAnadirEditar( self ):
        pISIN = "" ; pCuenta = "" ; pFecha = "" ; pGasto = "" ; pIngreso = "" ; pTipo = "" ; pDescripcion = "" ;
        titulo = "Formulario para Crear Comisiones"
        if self.accion == 'Editar':
            pISIN , pCuenta , pFecha , pTipo = self.parametros.split('/')
            pISIN , pCuenta , pFecha , pGasto , pIngreso , pTipo , faborita , pDescripcion = sesion.Sesion().getComision( str(pFecha) , pCuenta , pISIN , pTipo )
            titulo = "Formulario para Editar la comision del " + str(pFecha) + ' de ' + pCuenta + ', ' + pISIN
            
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        if self.accion == 'Anadir': 
            informacion += html.formInput( "Fecha" , "Transacciones" , "Fecha" , "date" , str(datetime.datetime.now().date()) , "Fecha en la que se realiza el Traspaso" , str(pFecha) , False )
            informacion += "<br /> <br />"
            
            opciones = []
            cuentas = sesion.Sesion().getCuentasBy( '' ,  '' ,  '' , 'cuenta ASC' )
            for cuenta , color , descripcion , moneda , pais in cuentas: opciones.append( ( cuenta , cuenta , False ) )
            informacion += html.formOptionList( 'Cuenta' , 'Transacciones' , 'Cuenta que cobra la comisión' , opciones , False )
            informacion += "<br /> <br />"
            
            opciones = []
            activos = sesion.Sesion().getActivos( )
            opciones.append( ( "*" , "La comision es de la cuenta " , True ) )
            for isin , tipo , emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia in activos: opciones.append( ( isin , descripcion , False ) )
            informacion += html.formOptionList( 'ISIN' , 'Transacciones' , 'Producto sobre el que se cobra la comisión' , opciones , False )
            informacion += "<br /> <br />"
            
            opciones = []
            opciones.append( ( "Comision" , "Comisión " +  pCuenta , True ) )
            opciones.append( ( "Compensacion" , "Compensación " +  pCuenta , True ) )
            opciones.append( ( "Dividendo" , "Dividendo " +  pCuenta , True ) )
            opciones.append( ( "Impuesto" , "Impuesto " +  pCuenta , True ) )
            opciones.append( ( "Interes" , "Interes " +  pCuenta , True ) )
            informacion += html.formOptionList( 'Tipo' , 'Transacciones' , 'Tipo de comision comisión' , opciones , False )
            informacion += "<br /> <br />"
        
        if self.accion == 'Editar':
            informacion += html.formHidden( 'Fecha' , 'Transacciones' , str(pFecha) )
            informacion += html.formHidden( 'Cuenta' , 'Transacciones' , pCuenta )
            informacion += html.formHidden( 'ISIN' , 'Transacciones' , pISIN )
            informacion += html.formHidden( 'Tipo' , 'Transacciones' , pTipo )
        
        informacion += html.formInput( "Gasto" , 'Transacciones' , "Gasto" , "float" , "15.5" , "Gasto producido por la comisión" , str(pGasto) , False )
        informacion += "<br /> <br />"  
        informacion += html.formInput( "Ingreso" , 'Transacciones' , "Ingreso" , "float" , "15.5" , "Ingreso producido por la comisión" , str(pIngreso) , False )
        informacion += "<br /> <br />"
        informacion += html.formInput( "Descripcion" , 'Transacciones' , "Descripción" , "text" , "Motivo del Traspaso" , "Motivo del Traspaso" , pDescripcion , False )
        informacion += "<br /> <br />"
        
        informacion += html.formCheckBox( 'Favorita' , 'Transacciones' , 'Marcar como favorita' , 'Si' )
        informacion += "<br /> <br />"
        
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion 
    
    
    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
         
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            isin , cuenta , fecha , tipo = parametros.split('/')
            sesion.Sesion().eliminarComision( isin , cuenta , tipo , fecha )
            recargarPagina = True
                 
        if redirigir == "AnadirEditar":
            fecha = request.form['Fecha']
            cuenta = request.form['Cuenta']
            isin = request.form['ISIN']
            tipo = request.form['Tipo']
            gasto = request.form['Gasto']
            ingreso = request.form['Ingreso']
            descripcion = request.form['Descripcion']           
            if 'Favorita' in request.form: favorita = 'Si'
            else: favorita = 'No'
            if self.accion == 'Anadir': sesion.Sesion().anadirComision( fecha , cuenta , tipo , isin , gasto , ingreso , favorita , descripcion )
            if self.accion == 'Editar': sesion.Sesion().actualizarComision( isin , cuenta , fecha , gasto , ingreso , tipo , favorita , descripcion )
            self.accion = 'Tabla'
            recargarPagina = True
                 
        return recargarPagina
     
        
#---------------------------- Traspasos ---------------------------#


class Traspasos(Formulario):
    
    def __init__( self ):   
        Formulario.__init__( self , 'Operaciones' , 'Traspasos' , 'Gestión de Traspasos' )
        self.filtro = filtro.Filtro( 'Gestion' , 'Traspasos' )


    def inicializarFiltro( self ): 
        opciones = []
        opciones.append( ( "" , " --------- " , True ) )
        cuentas = sesion.Sesion().getCuentasBy( '' ,  '' ,  '' , 'cuenta ASC' )
        for cuenta , color , descripcion , moneda , pais in cuentas: opciones.append( ( cuenta , cuenta , False ) )
        self.filtro.anadirCampo( 'Origen' , 'Origen' , opciones , 'Filtrar los traspasos por cuenta de origen' )
        self.filtro.anadirCampo( 'Destino' , 'Destino' , opciones , 'Filtrar los traspasos por cuenta de destino' )
        self.filtro.anadirCampo( 'FechaInicio' , 'Fecha Inicio' , 'date' , 'Filtrar por fechas superiores a la seleccionada'  )
        self.filtro.anadirCampo( 'FechaFin' , 'Fecha Fin' , 'date' , 'Filtrar por fechas inferiores a la seleccionada'  )


    def formularioTabla( self ):
        self.inicializarFiltro()
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        vFechaInicio = self.filtro.campos[ 'FechaInicio' ].getValor()
        vFechaFin = self.filtro.campos[ 'FechaFin' ].getValor()
        vOrigen = self.filtro.campos[ 'Origen' ].getValor()
        vDestino = self.filtro.campos[ 'Destino' ].getValor()
        
        traspasos = sesion.Sesion().getTraspasosBy( vFechaInicio , vFechaFin , vOrigen , vDestino , self.filtro.orden )
        
        informacion = ""
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarFecha' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Fecha' , 'Fecha' ) + "    </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarOrigen' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Origen' , 'Origen' ) + "     </th>"
        informacion += "       <th> " + html.refrescar( 'OrdenarDestino' , 'Transacciones' , 'etiqueta' , 'Ordenar' , 'Destino' , 'Destino' ) + "     </th>"
        informacion += "       <th> Precio        </th>"
        informacion += "       <th> Descripción   </th>"
        informacion += "       <th> " + self.formularioRedirigirAnadir()  + " </th>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        
        for origen , destino , fecha , precio , faborita , descripcion in traspasos:
            informacion += "   <tr>"
            informacion += "       <td> " + html.formInput( "Fecha" , "Transacciones" , '' , "date" , str(datetime.datetime.now().date()) , "Fecha en la que se realiza el Traspaso" , str(fecha) , False )        + " </td>"
            informacion += "       <td> " + origen + " </td>"
            informacion += "       <td> " + destino + " </td>"
            informacion += "       <td> " + html.representarNumero( precio , True ) + " </td>"
            informacion += "       <td> " + str(descripcion) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEditar( origen + '/' + destino + '/' + str(fecha) ) + " </td>"
            informacion += "       <td> " + self.formularioRedirigirEliminar( origen + '/' + destino + '/' + str(fecha) ) + " </td>"
            informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
    
    
    def formularioAnadirEditar( self ):
        pOrigen = "" ; pDestino = "" ; pFecha = "" ; pPrecio = "" ; pDescripcion = "" ;
        titulo = "Formulario para Crear Traspasos"
        if self.accion == 'Editar':
            pOrigen , pDestino , pFecha = self.parametros.split('/')
            pOrigen , pDestino , pFecha , pPrecio , faborita , pDescripcion = sesion.Sesion().getTraspaso( str(pFecha) , pOrigen , pDestino )
            titulo = "Formulario para Editar el traspaso del " + str(pFecha) + ' de ' + pOrigen + ' a ' + pDestino
            
        informacion = ""
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += html.formHeader( "AnadirEditar" , "Transacciones" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        if self.accion == 'Anadir': 
            informacion += html.formInput( "Fecha" , "Transacciones" , "Fecha del traspaso" , "date" , str(datetime.datetime.now().date()) , "Fecha en la que se realiza el Traspaso" , str(pFecha) , False )
            informacion += "<br /> <br />"
            opciones = []
            cuentas = sesion.Sesion().getCuentasBy( '' ,  '' ,  '' , 'cuenta ASC' )
            for cuenta , color , descripcion , moneda , pais in cuentas: opciones.append( ( cuenta , cuenta , False ) )
            informacion += html.formOptionList( 'CuentaOrigen' , 'Transacciones' , 'Cuenta de Origen' , opciones , False )
            informacion += "<br /> <br />"
            informacion += html.formOptionList( 'CuentaDestino' , 'Transacciones' , 'Cuenta de Destino' , opciones , False )
            informacion += "<br /> <br />"
        
        if self.accion == 'Editar':
            informacion += html.formHidden( 'Fecha' , 'Transacciones' , str(pFecha) )
            informacion += html.formHidden( 'CuentaOrigen' , 'Transacciones' , pOrigen )
            informacion += html.formHidden( 'CuentaDestino' , 'Transacciones' , pDestino )
       
        informacion += html.formInput( "Precio" , 'Transacciones' , "Cantidad Traspasada" , "float" , "15.5" , "Cantidad Traspasada desde la cuenta de Origen hasta la cuenta de Destino" , str(pPrecio) , False )
        informacion += "<br /> <br />"   
        informacion += html.formInput( "Descripcion" , 'Transacciones' , "Descripción" , "text" , "Motivo del Traspaso" , "Motivo del Traspaso" , pDescripcion , False )
        informacion += "<br /> <br />"
        
        informacion += html.formCheckBox( 'Favorita' , 'Transacciones' , 'Marcar como favorita' , 'Si' )
        informacion += "<br /> <br />"
        
        informacion += html.formHidden( 'SubFormulario' , 'Transacciones' , self.subFormulario )
        informacion += html.formHidden( 'Redirigir' , 'Transacciones' , "AnadirEditar" )
        informacion += html.formSubmit( "aceptar" , "Transacciones" , self.accion )
        informacion += "</fieldset>" 
        informacion += "</form>"
        informacion += self.formularioRedirigirCancelar()    
        return informacion 
    
    
    def capturarCampos( self , redirigir ):
        recargarPagina = self.capturarRedirigir( redirigir )
         
        if redirigir == "RedirigirEliminar":
            parametros = request.form['Parametros']
            origen , destino , fecha = parametros.split('/')
            sesion.Sesion().eliminarTraspaso( origen , destino , fecha )
            recargarPagina = True
                 
        if redirigir == "AnadirEditar":
            fecha = request.form['Fecha']
            origen = request.form['CuentaOrigen']
            destino = request.form['CuentaDestino']
            precio = request.form['Precio']
            descripcion = request.form['Descripcion']
            if 'Favorita' in request.form: favorita = 'Si'
            else: favorita = 'No'
            if self.accion == 'Anadir': sesion.Sesion().anadirTraspaso( fecha , origen , destino , precio , favorita , descripcion )
            if self.accion == 'Editar': sesion.Sesion().actualizarTraspaso( origen , destino , fecha , precio , favorita , descripcion )
            self.accion = 'Tabla'
            recargarPagina = True
                 
        return recargarPagina
    
    
     

