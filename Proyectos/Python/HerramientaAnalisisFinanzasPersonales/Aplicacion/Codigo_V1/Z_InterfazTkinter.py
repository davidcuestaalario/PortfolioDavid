# -*- coding: utf-8 -*-
import tkinter

####################################################################    
#----------------------------- VENTANA ----------------------------#
####################################################################

def ventana( titulo , icono , exapnd_Alto , exapnd_Ancho , c_fondo , border_type , border_size , cursor_type ):
    
    ventana = tkinter.Tk( );

    # -------------- VENTANA -------------- #
    ventana.title( titulo );
    ventana.iconbitmap( icono );

    # --------------- RESIZE -------------- #
    ventana.resizable( exapnd_Alto , exapnd_Ancho );

    # --------------- COLOR --------------- #
    ventana.config( bg = c_fondo );

    # --------------- BORDE --------------- #
    ventana.config( relief = border_type , bd = border_size);

    # --------------- CURSOR -------------- #
    ventana.config( cursor = cursor_type );
    
    # --------------- SCROL --------------- #
    #scrol = tkinter.Scrollbar( ventana );
    #scrol.pack( side = tkinter.RIGHT , fill = "y" );
    
    #box = tkinter.Listbox( ventana );
    #box.pack( fill = tkinter.BOTH );
    #scrol.config( command = box.yview );
    
    return ventana;

####################################################################    
#------------------------------ FRAME -----------------------------#
####################################################################

def listbox( VentanaInforme , exapnd_Alto , exapnd_Ancho , alineacion , dim_Alto , dim_Ancho , c_fondo , border_type , border_size , cursor_type ):
 
    frame = tkinter.Listbox( VentanaInforme );

    # --------------- RESIZE -------------- #
    if not exapnd_Alto and exapnd_Ancho:
        frame.pack( fill = "x" );
    if exapnd_Alto and not exapnd_Ancho:
        frame.pack( fill = "y" , expand = True );
    if exapnd_Alto and exapnd_Ancho:
        frame.pack( fill = "both" , expand = True );
    if not exapnd_Alto and not exapnd_Ancho:
        frame.pack( side = alineacion );

    # --------------- TAMANO -------------- #
    frame.config( width = dim_Alto , height = dim_Ancho );

    # --------------- COLOR --------------- #
    frame.config( bg = c_fondo );

    # --------------- BORDE --------------- #
    frame.config( relief = border_type , bd = border_size);

    # --------------- CURSOR -------------- #
    frame.config( cursor = cursor_type );
    
    return frame;

def frame( exapnd_Alto , exapnd_Ancho , alineacion , dim_Alto , dim_Ancho , c_fondo , border_type , border_size , cursor_type ):
 
    frame = tkinter.Frame();

    # --------------- RESIZE -------------- #
    if not exapnd_Alto and exapnd_Ancho:
        frame.pack( fill = "x" );
    if exapnd_Alto and not exapnd_Ancho:
        frame.pack( fill = "y" , expand = True );
    if exapnd_Alto and exapnd_Ancho:
        frame.pack( fill = "both" , expand = True );
    if not exapnd_Alto and not exapnd_Ancho:
        frame.pack( side = alineacion );

    # --------------- TAMANO -------------- #
    frame.config( width = dim_Alto , height = dim_Ancho );

    # --------------- COLOR --------------- #
    frame.config( bg = c_fondo );

    # --------------- BORDE --------------- #
    frame.config( relief = border_type , bd = border_size);

    # --------------- CURSOR -------------- #
    frame.config( cursor = cursor_type );
    
    return frame;

####################################################################    
#------------------------------ LABEL -----------------------------#
####################################################################

def label( texto , frame , alineacion , dim_Alto , dim_Ancho , c_fonfo , c_letra , fuente_letra ):
    
    label = tkinter.Label( frame , text = texto );
     
    # --------------- TAMANO -------------- #
    label.pack( side = alineacion ); # LEFT RIGHT TOP BOTTOM
    label.config( width = dim_Alto , height = dim_Ancho );
    
    # --------------- COLOR --------------- #
    label.config( bg = c_fonfo , fg = c_letra  );
    
    # --------------- LETRA --------------- #
    label.config( font = fuente_letra  );
    
    return label;


def labelxy( texto , frame , fil , col , alineacion , dim_Alto , dim_Ancho , c_fonfo , c_letra , fuente_letra ):
    
    label = tkinter.Label( frame , text = texto );
    
    # --------------- TAMANO -------------- #
    label.grid( row = fil , column = col );
    label.config( width = dim_Alto , height = dim_Ancho );
    label.config( sticky = alineacion  ); # n s e w 
    
    # --------------- COLOR --------------- #
    label.config( bg = c_fonfo , fg = c_letra  );
    
    # --------------- LETRA --------------- #
    label.config( font = fuente_letra );
    
    return label;

####################################################################    
#------------------------------ IMAGEN ----------------------------#
####################################################################
    
def imagen( img , frame , fil , col , alineacion):
  
    label = tkinter.Label( frame , image = img ); # png gif
    
    # --------------- TAMANO -------------- #
    label.grid( row = fil , column = col );
    label.config( sticky = alineacion ); # n s e w 
    
    return label;
    
####################################################################    
#------------------------------ IMPUT -----------------------------#
####################################################################
    
def imput( frame , fil , col , alineacion , dim_Alto , dim_Ancho , c_fonfo , c_letra , fuente_letra ):
    
    label = tkinter.entry( frame );
    
    # --------------- TAMANO -------------- #
    label.grid( row = fil , column = col );
    label.config( width = dim_Alto , height = dim_Ancho );
    label.config( sticky = alineacion  ); # n s e w 
    
    # --------------- COLOR --------------- #
    label.config( bg = c_fonfo , fg = c_letra  );
    
    # --------------- LETRA --------------- #
    label.config( font = fuente_letra );
    
    return label;


def text( frame , fil , col , alineacion , dim_Alto , dim_Ancho , c_fonfo , c_letra , fuente_letra ):
    
    label = tkinter.text( frame );
    
    # --------------- TAMANO -------------- #
    label.grid( row = fil , column = col );
    label.config( width = dim_Alto , height = dim_Ancho );
    label.config( sticky = alineacion  ); # n s e w 
    
    # --------------- COLOR --------------- #
    label.config( bg = c_fonfo , fg = c_letra  );
    
    # --------------- LETRA --------------- #
    label.config( font = fuente_letra );
    
    # --------------- SCROL --------------- #
    scrol = tkinter.scrollbar( frame , command = label );
    scrol.grid( row = fil , column = col+1 );
    label.config( yscrollcommand = scrollvert.set ); 
    
    return label;


def boton( texto , frame , fil , col , alineacion , dim_Alto , dim_Ancho , c_fonfo , c_letra , fuente_letra ):
    
    label = tkinter.button( frame , text = texto );
    
    # --------------- TAMANO -------------- #
    label.grid( row = fil , column = col );
    label.config( width = dim_Alto , height = dim_Ancho );
    label.config( sticky = alineacion  ); # n s e w 
    
    # --------------- COLOR --------------- #
    label.config( bg = c_fonfo , fg = c_letra  );
    
    # --------------- LETRA --------------- #
    label.config( font = fuente_letra );
    
    return label;