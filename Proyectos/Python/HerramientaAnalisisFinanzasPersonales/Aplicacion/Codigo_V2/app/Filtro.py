# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from lib import HTML as html
from lib import Utils as utils

from app import Sesion as sesion
from app import Seccion as secciones

####################################################################    
#------------------------------ Campo -----------------------------#
####################################################################

class Campo:
    
    def __init__( self , pID , pLabel , pTipo , pTitulo ):
        self.id = pID
        self.label = pLabel
        self.titulo = pTitulo
        self.valor = ''
        
        if utils.isLista( pTipo ):
            self.tipo = 'OptionList'
            self.options = pTipo 
        else:
           self.tipo = pTipo
           self.options = None


    
    def getValor( self ): return self.valor
    def setValor( self , pValor ): self.valor = pValor
        
    
    def generarFormulario( self ):
        informacion = ""
        if self.tipo == 'OptionList': informacion += html.formOptionList( self.id , 'Filtro' , self.label , self.options , False ) 
        else: informacion += html.formInput( self.id , 'Filtro' , self.label , self.tipo , '' , self.titulo , self.valor , False )
        informacion += "<br /> <br />"
        return informacion


    def capturarCampos( self ): self.valor = request.form[ self.id ]
            
####################################################################    
#------------------------------ Filtro ----------------------------#
####################################################################

class Filtro:
    
    def __init__( self , pSeccion , pSubSeccion ):
        self.seccion = pSeccion
        self.subSeccion = pSubSeccion
        self.orden = ''
        self.ordenTipo = ''
        self.campos = {}
        
        
    def anadirCampo( self , pID , pLabel , pTipo , pTitulo ):
        if pID not in self.campos:
            self.campos[ pID ] = Campo( pID , pLabel , pTipo , pTitulo )
    
    
    def ordenar( self , pCampo ):
        if pCampo in self.campos:
            #if self.ordenTipo == 'ASC': self.ordenTipo = 'DESC' 
            #else: self.ordenTipo = 'ASC'
            self.ordenTipo = 'ASC'
            self.orden = pCampo + " " + self.ordenTipo
             
    
    def formularioEditarFiltros( self ):
        informacion = ""
        informacion += html.formHeader( 'EditarFiltros' , 'Filtro' , '/Filtrar' , False )
        informacion += html.formHidden( 'Seccion' , 'Filtro' , self.seccion )
        informacion += html.formHidden( 'SubSeccion' , 'Filtro' , self.subSeccion )
        informacion += html.formSubmit( 'editar' , 'Filtro' , 'Editar Filtros' )
        informacion += "</form>"               
        return informacion
    
    
    def generarFormulario( self ):
        informacion = ""
        informacion += self.generarFormularioFiltrar()
        informacion += self.generarFormularioRestablecerFiltros()
        return informacion
    
    
    def generarFormularioFiltrar( self ):
        titulo = "Filtrar " + self.subSeccion
        informacion = ""
        informacion += html.titulo( self.seccion + self.subSeccion , "contenido" , 2 , titulo )
        informacion += html.formHeader( "AnadirEditar" , "Filtro" , '/' , False )
        informacion += "<br />"
        informacion += "<fieldset>"
        
        for campo in self.campos: informacion += self.campos[ campo ].generarFormulario()

        informacion += html.formHidden( 'Redirigir' , 'Filtro' , 'Filtrar' )
        informacion += html.formSubmit( "aceptar" , "Filtro" , 'Aplicar Filtro' )
        informacion += "</fieldset>" 
        informacion += "</form>"  
        return informacion


    def generarFormularioRestablecerFiltros( self ):
        informacion = ""
        informacion += html.formHeader( "AnadirEditar" , "Filtro" , '/' , False )
        informacion += "<br />"
        informacion += html.formHidden( 'Redirigir' , 'Filtro' , 'RestablecerFiltro' )
        informacion += html.formSubmit( "eliminar" , "Filtro" , 'Restablecer Filtro' )
        informacion += "</form>"  
        return informacion
    
    
    def capturarCampos( self , redirigir ):
        recargarPagina = False
        
        if redirigir == 'Filtrar':
           for campo in self.campos: self.campos[ campo ].capturarCampos()
           recargarPagina = True
           redirigir = secciones.Secciones().redireccionar( self.seccion )
        
        if redirigir == 'RestablecerFiltro':
            for campo in self.campos: self.campos[ campo ].setValor( '' )
            recargarPagina = True
            redirigir = secciones.Secciones().redireccionar( self.seccion )
        
        return recargarPagina