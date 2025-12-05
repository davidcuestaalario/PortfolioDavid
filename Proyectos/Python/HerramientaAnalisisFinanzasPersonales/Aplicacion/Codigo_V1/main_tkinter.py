# -*- coding: utf-8 -*-
from app import Inversion_Indices as Indices
import tkinter

####################################################################    
#----------------------------- CALCULOS ---------------------------#
####################################################################

ruta = 'C:/Users/david/Dropbox (Personal)/Finanzas/Scraper/BaseDatos';
indices_csv = '/Indices.csv';
posIndices_csv = '/PosicionesIndices.csv';

indices = Indices.cargarIndices( 'csv' , ruta , indices_csv , posIndices_csv );
resumenIndices = Indices.calcularResumen( indices );

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

####################################################################    
#----------------------------- CUERPO -----------------------------#
####################################################################

titulo_colorFondo = "lightblue";
titulo_colorLetra = "black";
titulo_fuente = ("Calibri" , 15);
titulo_padx = 10;
titulo_pady = 10; 
titulo_ancho = 8;

cabecera_colorFondo = "lightblue";
cabecera_colorLetra = "blue";
cabecera_fuente = ("Calibri" , 10);
cabecera_padx = 5;
cabecera_pady = 5; 
cabeceras = ('ISIN' , 'Fecha' , 'Titulos' , 'PrecioCompra' , 'PrecioActual' , 'ValorCompra' , 'ValorActual' , 'Beneficio');

compra_colorFondo = "lightblue";
compra_colorLetra = "blue";
compra_fuente = ("Calibri" , 10);
compra_padx = 5;
compra_pady = 5;

venta_colorFondo = "lightblue";
venta_colorLetra = "red";
venta_fuente = ("Calibri" , 10);
venta_padx = 5;
venta_pady = 5;

resumen_colorFondo = "lightblue";
resumen_colorLetra = "blue";
resumen_fuente = ("Calibri" , 10);
resumen_padx = 5;
resumen_pady = 5;

fil = 0;
col = 0;

for indice in indices:
    
    # ------------------ Titulo ------------------ #
    
    informacion = "*************** " + indice.descripcion + " *************** \n";
    label = tkinter.Label( frameInforme , text = informacion );
    # --------------- TAMANO -------------- #
    label.grid( row = fil , column = col , padx = titulo_padx , pady = titulo_pady , columnspan = titulo_ancho );
    label.config( width = "0" , height = "0" );
    # --------------- COLOR --------------- #
    label.config( bg = titulo_colorFondo , fg = titulo_colorLetra );
    # --------------- LETRA --------------- #
    label.config( font = titulo_fuente );
    
    # ------------------ Cebecera ------------------ #
    
    fil += 1;
    col = 0;
    for cabecera in cabeceras:  
        informacion = cabecera;
        label = tkinter.Label( frameInforme , text = informacion );
        # --------------- TAMANO -------------- #
        label.grid( row = fil , column = col , padx = cabecera_padx , pady = cabecera_pady );
        label.config( width = "0" , height = "0" );
        # --------------- COLOR --------------- #
        label.config( bg = cabecera_colorFondo , fg = cabecera_colorLetra );
        # --------------- LETRA --------------- #
        label.config( font = cabecera_fuente );
        col += 1; 
    
    fil += 1;
    
    # ------------------ Aportaciones ------------------ #
    
    for aportacion in indice.aportaciones:
        
        if aportacion.operacion == "compra":
            operacion_colorFondo = compra_colorFondo;
            operacion_colorLetra = compra_colorLetra;
            operacion_fuente = compra_fuente;
            operacion_padx = compra_padx;
            operacion_pady = compra_pady;
        else:
            operacion_colorFondo = venta_colorFondo;
            operacion_colorLetra = venta_colorLetra;
            operacion_fuente = venta_fuente;
            operacion_padx = venta_padx;
            operacion_pady = venta_pady;
          
        # ISIN
        col = 0;
        informacion = indice.isin;
        label = tkinter.Label( frameInforme , text = informacion );
        # --------------- TAMANO -------------- #
        label.grid( row = fil , column = col , padx = operacion_padx , pady = operacion_pady );
        label.config( width = "0" , height = "0" );
        # --------------- COLOR --------------- #
        label.config( bg = operacion_colorFondo , fg = operacion_colorLetra );
        # --------------- LETRA --------------- #
        label.config( font = operacion_fuente );
        
        # Fecha
        col = 1;
        informacion = aportacion.date;
        label = tkinter.Label( frameInforme , text = informacion );
        # --------------- TAMANO -------------- #
        label.grid( row = fil , column = col , padx = operacion_padx , pady = operacion_pady );
        label.config( width = "0" , height = "0" );
        # --------------- COLOR --------------- #
        label.config( bg = operacion_colorFondo , fg = operacion_colorLetra );
        # --------------- LETRA --------------- #
        label.config( font = operacion_fuente );
        
        # Titulos
        col = 2;
        informacion = aportacion.titulos;
        label = tkinter.Label( frameInforme , text = informacion );
        # --------------- TAMANO -------------- #
        label.grid( row = fil , column = col , padx = operacion_padx , pady = operacion_pady );
        label.config( width = "0" , height = "0" );
        # --------------- COLOR --------------- #
        label.config( bg = operacion_colorFondo , fg = operacion_colorLetra );
        # --------------- LETRA --------------- #
        label.config( font = operacion_fuente );
        
        # PrecioCompra
        col = 3;
        informacion = aportacion.precio;
        label = tkinter.Label( frameInforme , text = informacion );
        # --------------- TAMANO -------------- #
        label.grid( row = fil , column = col , padx = operacion_padx , pady = operacion_pady );
        label.config( width = "0" , height = "0" );
        # --------------- COLOR --------------- #
        label.config( bg = operacion_colorFondo , fg = operacion_colorLetra );
        # --------------- LETRA --------------- #
        label.config( font = operacion_fuente );
        
        # PrecioActual
        col = 4;
        informacion = indice.cotizacion;
        label = tkinter.Label( frameInforme , text = informacion );
        # --------------- TAMANO -------------- #
        label.grid( row = fil , column = col , padx = operacion_padx , pady = operacion_pady );
        label.config( width = "0" , height = "0" );
        # --------------- COLOR --------------- #
        label.config( bg = operacion_colorFondo , fg = operacion_colorLetra );
        # --------------- LETRA --------------- #
        label.config( font = operacion_fuente );
        
        # ValorCompra
        col = 5; 
        informacion = "{:.2f}".format(aportacion.resumen.aportaciones);
        label = tkinter.Label( frameInforme , text = informacion );
        # --------------- TAMANO -------------- #
        label.grid( row = fil , column = col , padx = operacion_padx , pady = operacion_pady );
        label.config( width = "0" , height = "0" );
        # --------------- COLOR --------------- #
        label.config( bg = operacion_colorFondo , fg = operacion_colorLetra );
        # --------------- LETRA --------------- #
        label.config( font = operacion_fuente );
        
        # ValorActual
        col = 6; 
        informacion = "{:.2f}".format(aportacion.resumen.valorActual);
        label = tkinter.Label( frameInforme , text = informacion );
        # --------------- TAMANO -------------- #
        label.grid( row = fil , column = col , padx = operacion_padx , pady = operacion_pady );
        label.config( width = "0" , height = "0" );
        # --------------- COLOR --------------- #
        label.config( bg = operacion_colorFondo , fg = operacion_colorLetra );
        # --------------- LETRA --------------- #
        label.config( font = operacion_fuente );
        
        # Beneficio
        col = 7;
        informacion = "{:.2f}".format(aportacion.resumen.beneficio);
        label = tkinter.Label( frameInforme , text = informacion );
        # --------------- TAMANO -------------- #
        label.grid( row = fil , column = col , padx = operacion_padx , pady = operacion_pady );
        label.config( width = "0" , height = "0" );
        # --------------- COLOR --------------- #
        label.config( bg = operacion_colorFondo , fg = operacion_colorLetra );
        # --------------- LETRA --------------- #
        label.config( font = operacion_fuente );
        
        fil += 1;
        
    # ------------------ Resumen ------------------ #
    
    # ValorCompra
    col = 5;
    informacion = "{:.2f}".format(indice.resumen.aportaciones);
    label = tkinter.Label( frameInforme , text = informacion );
    # --------------- TAMANO -------------- #
    label.grid( row = fil , column = col , padx = resumen_padx , pady = resumen_pady );
    label.config( width = "0" , height = "0" );
    # --------------- COLOR --------------- #
    label.config( bg = resumen_colorFondo , fg = resumen_colorLetra );
    # --------------- LETRA --------------- #
    label.config( font = resumen_fuente );
        
    # ValorActual
    col = 6;
    informacion = "{:.2f}".format(indice.resumen.valorActual);
    label = tkinter.Label( frameInforme , text = informacion );
    # --------------- TAMANO -------------- #
    label.grid( row = fil , column = col , padx = resumen_padx , pady = resumen_pady );
    label.config( width = "0" , height = "0" );
    # --------------- COLOR --------------- #
    label.config( bg = resumen_colorFondo , fg = resumen_colorLetra );
    # --------------- LETRA --------------- #
    label.config( font = resumen_fuente );
        
    # Beneficio
    col = 7;
    informacion = "{:.2f}".format(indice.resumen.beneficio);
    label = tkinter.Label( frameInforme , text = informacion );
    # --------------- TAMANO -------------- #
    label.grid( row = fil , column = col , padx = resumen_padx , pady = resumen_pady );
    label.config( width = "0" , height = "0" );
    # --------------- COLOR --------------- #
    label.config( bg = resumen_colorFondo , fg = resumen_colorLetra );
    # --------------- LETRA --------------- #
    label.config( font = resumen_fuente );
    
    fil += 1;
    col = 0;


# ------------------ Resumen ------------------ #

col = 0;
fil += 1;
    
informacion = "****************************** Resumen ****************************** \n";
label = tkinter.Label( frameInforme , text = informacion );
# --------------- TAMANO -------------- #
label.grid( row = fil , column = col , padx = titulo_padx , pady = titulo_pady , columnspan = titulo_ancho );
label.config( width = "0" , height = "0" );
# --------------- COLOR --------------- #
label.config( bg = titulo_colorFondo , fg = titulo_colorLetra );
# --------------- LETRA --------------- #
label.config( font = titulo_fuente );

fil += 1;
    
# ValorCompra
col = 5;
informacion = "{:.2f}".format(resumenIndices.aportaciones);
label = tkinter.Label( frameInforme , text = informacion );
# --------------- TAMANO -------------- #
label.grid( row = fil , column = col , padx = resumen_padx , pady = resumen_pady );
label.config( width = "0" , height = "0" );
# --------------- COLOR --------------- #
label.config( bg = resumen_colorFondo , fg = resumen_colorLetra );
# --------------- LETRA --------------- #
label.config( font = resumen_fuente );
        
# ValorActual
col = 6;
informacion = "{:.2f}".format(resumenIndices.valorActual);
label = tkinter.Label( frameInforme , text = informacion );
# --------------- TAMANO -------------- #
label.grid( row = fil , column = col , padx = resumen_padx , pady = resumen_pady );
label.config( width = "0" , height = "0" );
# --------------- COLOR --------------- #
label.config( bg = resumen_colorFondo , fg = resumen_colorLetra );
# --------------- LETRA --------------- #
label.config( font = resumen_fuente );
        
# Beneficio
col = 7;
informacion = "{:.2f}".format(resumenIndices.beneficio);
label = tkinter.Label( frameInforme , text = informacion );
# --------------- TAMANO -------------- #
label.grid( row = fil , column = col , padx = resumen_padx , pady = resumen_pady );
label.config( width = "0" , height = "0" );
# --------------- COLOR --------------- #
label.config( bg = resumen_colorFondo , fg = resumen_colorLetra );
# --------------- LETRA --------------- #
label.config( font = resumen_fuente );


 


####################################################################    
#---------------------------- MAIN LOOP ---------------------------#
####################################################################

ventana.mainloop();
