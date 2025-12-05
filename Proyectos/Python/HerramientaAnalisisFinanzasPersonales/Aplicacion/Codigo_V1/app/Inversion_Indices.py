# -*- coding: utf-8 -*-
from lib import Z_Scraper as scraper;
from lib import Z_SQLReader as sql;
from lib import Z_Graficas as graficas;
from lib import Z_Utils as utils;

####################################################################    
#------------------------------ CLASES ----------------------------#
####################################################################

# ------------------------------------ #
# -------------- INDICE -------------- #
# ------------------------------------ #

class Indice:
        
    def __init__( self , pIsin , pLink , pMoneda , pDescripcion , pCotizacion ):
        self.isin = pIsin;
        self.link = pLink;
        self.moneda = pMoneda;
        self.descripcion = pDescripcion;
        self.cotizacion = pCotizacion;
        self.aportaciones = [];
        self.resumen = 0;


    def anadirAportacion( self , aportacion ):
        self.aportaciones.append( aportacion );


    def calcularResumen( self ):
        aportaciones = 0;
        valorActual = 0;
        beneficio = 0;        
        for aportacion in self.aportaciones:
            aportacion.calcularResumen( self.cotizacion );
            aportaciones += aportacion.resumen.aportaciones;
            valorActual += aportacion.resumen.valorActual;
            beneficio += aportacion.resumen.beneficio;       
        self.resumen = Resumen( aportaciones , valorActual , beneficio );

        
    def informacion( self ):
        informacion = "";
        informacion += "*************** " + self.descripcion + " *************** \n";
        informacion += "  * ISIN: " + self.isin + "\n";
        informacion += "  * COTIZACION: " + "{:.2f}".format(self.cotizacion) + "\n";
        #informacion += "  * LINK: " + self.link + "\n";
        informacion += "\n";
        return informacion;    
    
    
    def consultarAportaciones( self ):
        informacion = "";
        informacion += "    " + "FECHA" + "        ";
        informacion += "TITULOS" + "    ";
        informacion += "PRECIO COMPRA" + "    ";
        informacion += "BROKER" + "    " + "\n";
        for aportacion in self.aportaciones:
            informacion += aportacion.consultarAportacion();
        informacion += "\n";
        return informacion;
      

    def mostrarResumenIndice( self ):
        informacion = "";
        informacion += "*************** " + self.descripcion + "*************** \n";
        informacion += "    " + "APORTACIONES" + "    ";
        informacion += "VALOR ACTUAL" + "    ";
        informacion += "BENEFICIO" + "    " + "\n";
        for aportacion in self.aportaciones:
            informacion += aportacion.mostrarResumen();
        informacion += "-------------------------------------------------" + "\n";
        informacion += self.resumen.mostrarResumen( );
        informacion += "\n";
        return informacion;
    
# ------------------------------------ #
# ------------ APORTACION ------------ #
# ------------------------------------ #

class Aportacion_Indice:
        
    def __init__( self , pDate , pTitulos , pPrecio , pBroker , pOperacion ):       
        self.date = pDate;
        self.titulos = pTitulos;
        self.precio = pPrecio; 
        self.broker = pBroker;
        self.operacion = pOperacion;
        self.resumen = 0;

    
    def calcularResumen( self , cotizacion ):      
        aportaciones = self.titulos * self.precio;
        valorActual = self.titulos * cotizacion;
        if self.operacion == "venta":
            aportaciones = -aportaciones;
            valorActual = -valorActual;
        beneficio = valorActual - aportaciones;
        self.resumen = Resumen( aportaciones , valorActual , beneficio ); 
     
    
    def informacion( self ):
        informacion = "";
        pDate = self.date.strftime( "%Y-%m-%d" );
        informacion += "  * FECHA: " + pDate + "\n"
        informacion += "  * TITULOS: " + "{:.2f}".format(self.titulos) + "\n";
        informacion += "  * PRECIO COMPRA: " + "{:.2f}".format(self.precio) + "\n";
        informacion += "  * BROKER: " + self.broker + "\n";
        return informacion;
        
    
    def consultarAportacion( self ):
        informacion = "";
        pDate = self.date.strftime( "%Y-%m-%d" );
        informacion += "    " + pDate + "    "
        informacion += "{:.2f}".format(self.titulos) + "        ";
        informacion += "{:.2f}".format(self.precio) + "        ";
        informacion += self.broker + "    " + "\n";
        return informacion;
 
       
    def mostrarResumen( self ):
        return self.resumen.mostrarResumen( );
        
# ------------------------------------ #
# -------------- RESUMEN ------------- #
# ------------------------------------ #

class Resumen:
    
    def __init__( self , pAportaciones , pValorActual , pBeneficio ):
        self.aportaciones = pAportaciones;
        self.valorActual = pValorActual;
        self.beneficio = pBeneficio;

        
    def informacion( self ):
        informacion = "";
        informacion += "  * APORTACIONES: " + "{:.2f}".format(self.aportaciones) + "\n";
        informacion += "  * VALOR ACTUAL: " + "{:.2f}".format(self.valorActual) + "\n";
        informacion += "  * BENEFICIO: " + "{:.2f}".format(self.beneficio) + "\n";
        return informacion;
        
        
    def mostrarResumen( self ):
        informacion = "        ";
        informacion += "{:.2f}".format(self.aportaciones) + "        ";  
        informacion += "{:.2f}".format(self.valorActual) + "        ";
        informacion += "{:.2f}".format(self.beneficio) + "        " + "\n";
        return informacion;
    
####################################################################    
#--------------------------- CARGAR DATOS -------------------------#
####################################################################

def cargarIndices( fuente , ruta , indices_csv , posIndices_csv ):
    
    indices = []    
    resultado = sql.getIndices( fuente , ruta , indices_csv );
    
    for isin , descripcion , moneda , link in resultado:
        cotizacion = scraper.buscarCotizacionYahoo( link );
        cotizacion = cotizacion.replace( "," , "." )
        cotizacion = float( cotizacion )
        if( moneda == "usd" ):
            cotizacion = scraper.usd_To_eur( cotizacion );
            moneda = "eur";
            
        indice = Indice( isin , link , moneda , descripcion , cotizacion );
        indices.append( indice );
                 
    resultado = sql.getPosicionesIndices( fuente , ruta , posIndices_csv );
    
    for date , isin , titulos , precio , broker , operacion in resultado:
        aportacion = Aportacion_Indice( date , titulos , precio , broker , operacion );
        for indice in indices:
            if indice.isin == isin:
                indice.anadirAportacion( aportacion );
    
    return indices;

####################################################################    
#------------------------------ BALANCE ---------------------------#
####################################################################

def calcularResumen( indices ):
    
    aportaciones = 0;
    valorActual = 0;
    beneficio = 0;
    
    for indice in indices:       
        
        indice.calcularResumen();
        
        aportaciones += indice.resumen.aportaciones;
        valorActual += indice.resumen.valorActual;
        beneficio += indice.resumen.beneficio;
        
    resumen = Resumen( aportaciones , valorActual , beneficio );
    return resumen;

####################################################################    
#---------------------------- INFORMACION -------------------------#
####################################################################

def mostrarInformacion( indices ):
    informacion = "";
    for indice in indices:
        informacion += indice.informacion();
        informacion += indice.consultarAportaciones();
    return informacion;


def mostrarResumenGloval( indices , resumen ):
    informacion = "";
    for indice in indices:
        informacion += indice.mostrarResumenIndice();        
    informacion += "===================== TOTAL ===================== \n";
    informacion += "    " + "APORTACIONES" + "    ";
    informacion += "VALOR ACTUAL" + "    ";
    informacion += "BENEFICIO" + "    " + "\n";
    informacion += resumen.mostrarResumen();
    return informacion;


def generarInforme( indices ):
    informacion = "\n";
    informacion += "#################################################" + "\n";
    informacion += "#----------INFORMACION SOBRE LOS TITULOS--------#" + "\n";
    informacion += "#################################################" + "\n";
    informacion += "\n";
    informacion += mostrarInformacion( indices );
    informacion += "\n";
    return informacion;

def generarResumen( indices , resumen ): 
    informacion = "\n";
    informacion += "#################################################" + "\n";
    informacion += "#--------------RESUMEN POR INDICES--------------#" + "\n"; 
    informacion += "#################################################" + "\n";
    informacion += "\n";
    informacion += mostrarResumenGloval( indices , resumen );
    informacion += "\n";
    return informacion;

def guardarInforme( nombre , informacion ):
    nombre += ".txt";
    fichero = open( nombre , 'w');
    fichero.write( informacion );
    fichero.write( "\n" ); 
    fichero.close;

####################################################################    
#----------------------------- GRAFICAS ---------------------------#
####################################################################

def generarGrafica( indices ):
    
    titulo = "AssetAllocationIndices";
    valores = [];
    etiquetas = [];
    coloresFondo = [];
    coloresLetra = [];
    numIndices = 0;
    
    for indice in indices:
        valores.append( indice.resumen.valorActual );
        etiquetas.append( indice.descripcion );
        coloresFondo.append( utils.getColor( "pastel" , numIndices ) );
        coloresLetra.append( utils.getColor( "dark" , numIndices ) );
        numIndices += 1;
    
    graficas.circular(titulo, valores, etiquetas, coloresFondo, coloresLetra);
      
####################################################################    
#------------------------------- MAIN -----------------------------#
####################################################################

def mainResumen( fuente , ruta , indices_csv , posIndices_csv ):

    indices = cargarIndices( fuente , ruta , indices_csv , posIndices_csv );
    resumen = calcularResumen( indices );

    informe = generarInforme( indices );
    informe += generarResumen( indices , resumen );
    guardarInforme( "res/pruebas" , informe )
    #print( informe );

def mainGraficas( fuente , ruta , indices_csv , posIndices_csv ):
    
    indices = cargarIndices( fuente , ruta , indices_csv , posIndices_csv );
    resumen = calcularResumen( indices );
    generarGrafica( indices );


fuente = 'csv'; # 'bd'
ruta = 'C:/Users/david/Dropbox (Personal)/Finanzas/Scraper/BaseDatos';
indices_csv = '/Indices.csv';
posIndices_csv = '/PosicionesIndices.csv';

# mainResumen( fuente , ruta , indices_csv , posIndices_csv );

    
    
    