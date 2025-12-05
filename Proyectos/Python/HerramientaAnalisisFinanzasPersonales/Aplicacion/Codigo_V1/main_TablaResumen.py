# -*- coding: utf-8 -*-
from app import Inversion_Indices as Indices
from lib import Z_InterfazTkinter as interfaz
import tkinter

####################################################################    
#----------------------------- CALCULOS ---------------------------#
####################################################################

ruta = 'C:/Users/david/Dropbox (Personal)/Finanzas/Scraper/BaseDatos';
indices_csv = '/Indices.csv';
posIndices_csv = '/PosicionesIndices.csv';

indices = Indices.cargarIndices( 'csv' , ruta , indices_csv , posIndices_csv );
resumen = Indices.calcularResumen( indices );
informeAportaciones = Indices.generarInforme( indices );
resumenAportaciones = Indices.generarResumen( indices , resumen );

####################################################################    
#------------------------ VENTANA PRINCIPAL -----------------------#
####################################################################

titulo = "GESTION DE FINANZAS PERSONALES";
icono = "static/img/icono_0.ico";
exapnd_Alto = True;
exapnd_Ancho = True;
c_fondo = "blue";
border_type = "groove"; 
border_size = 35;
cursor_type = "pirate";

ventana = tkinter.Tk( );
ventana.title( titulo );
ventana.iconbitmap( icono );
ventana.resizable( exapnd_Alto , exapnd_Ancho );
ventana.config( bg = c_fondo );
ventana.config( relief = border_type , bd = border_size);
ventana.config( cursor = cursor_type );

# ------------------ frameInforme ------------------ #

exapnd_Alto = False;
exapnd_Ancho = False;
alineacion = tkinter.LEFT; # LEFT RIGHT TOP BOTTOM
dim_Alto = "500";
dim_Ancho = "400";
c_fondo = "lightblue";
border_type = "groove"; 
border_size = 35;
cursor_type = "hand2";

frameInforme = tkinter.Listbox( ventana );

if not exapnd_Alto and exapnd_Ancho:
    frameInforme.pack( fill = "x" );
if exapnd_Alto and not exapnd_Ancho:
    frameInforme.pack( fill = "y" , expand = True );
if exapnd_Alto and exapnd_Ancho:
    frameInforme.pack( fill = "both" , expand = True );
if not exapnd_Alto and not exapnd_Ancho:
    frameInforme.pack( side = alineacion );

frameInforme.config( width = dim_Alto , height = dim_Ancho );
frameInforme.config( bg = c_fondo );
frameInforme.config( relief = border_type , bd = border_size);
frameInforme.config( cursor = cursor_type );

scrol = tkinter.Scrollbar( ventana );
scrol.pack( side = tkinter.RIGHT , fill = "y" );   
scrol.config( command = frameInforme.yview );
frameInforme.config( yscrollcommand = scrol.set );

# ------------------ informeAportaciones ------------------ #

texto = resumenAportaciones ; 

alineacion = "right"; # LEFT RIGHT TOP BOTTOM

dim_Alto = "0";
dim_Ancho = "0";

c_fonfo = "lightblue";
c_letra = "blue";

fuente_letra = ("Calibri" , 10);

interfaz.label( texto , frameInforme , alineacion , dim_Alto , dim_Ancho , c_fonfo , c_letra , fuente_letra );

texto = informeAportaciones; 

interfaz.label( texto , frameInforme , alineacion , dim_Alto , dim_Ancho , c_fonfo , c_letra , fuente_letra );

#nombre = "Generar Informe";
#generarInformeBT = tkinter.Button( ventana , text = nombre , command = lambda: Indices.generarInforme( indices , resumen ) );
#generarInformeBT.pack();


 


####################################################################    
#---------------------------- MAIN LOOP ---------------------------#
####################################################################

ventana.mainloop();
