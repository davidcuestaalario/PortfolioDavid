# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import send_file

from app import Sesion as sesion
from app import Seccion as secciones

#from lib import SQL as sql
from lib import HTML as html

#sesion = Sesion.Sesion( )
#seccion = Seccion.Secciones( )

####################################################################    
#----------------------- INICIAR SERVIDOR WEB ---------------------#
####################################################################

aplicacion = Flask(__name__)

####################################################################    
#---------------------------- Principal ---------------------------#
####################################################################

@aplicacion.route('/' , methods=["GET", "POST"] )
def home():
    return secciones.Secciones().generarPagina()
    
@aplicacion.route('/Principal' , methods=["GET", "POST"] )
def Principal():
    redirigir = secciones.Secciones().generarRedireccion( 'Principal' )
    return redirigir 
    
####################################################################    
#---------------------------- Redirigir ---------------------------#
####################################################################

@aplicacion.route('/Redirigir' , methods=["GET", "POST"] )
def Redirigir():  
    direccion = request.form['Redirigir']
    redirigir = secciones.Secciones().generarRedireccion( direccion )
    return redirigir

####################################################################    
#----------------------------- Ordenar ----------------------------#
####################################################################

@aplicacion.route('/Ordenar' , methods=["GET", "POST"] )
def Ordenar():  
    parametros = request.form['Parametros']
    secciones.Secciones().setParametros( 'Ordenar' , parametros )
    return redirect( '/' ) 

####################################################################    
#----------------------------- Filtrar ----------------------------#
####################################################################

@aplicacion.route('/Filtrar' , methods=["GET", "POST"] )
def Filtrar():  
    subSeccion = request.form['SubSeccion']
    seccion = request.form['Seccion']
    secciones.Secciones().setParametros( 'Filtrar' , seccion + ';' + subSeccion  )
    redirigir = secciones.Secciones().generarRedireccion( 'Filtros' )
    return redirigir 

####################################################################    
#---------------------------- Descargar ---------------------------#
####################################################################

@aplicacion.route('/Descargar' , methods=["GET", "POST"] )
def Descargar ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    ruta = request.form['Ruta']
    return send_file( ruta , as_attachment=True )





























####################################################################    
#-------------------- EJECUTAR PAGINA PRINCIPAL -------------------#
#################################################################### 
    
if __name__ == '__main__':
    aplicacion.run( )
