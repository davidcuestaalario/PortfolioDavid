# -*- coding: utf-8 -*-
import requests;
from bs4 import BeautifulSoup

####################################################################    
#----------------------- BUSCAR COTIZACIONES ----------------------#
####################################################################

def buscarCotizacionYahoo( url ):  
    peticion = requests.get( url )
    status = peticion.status_code;

    if status == 200: 
        respuesta = peticion.text;
        soup = BeautifulSoup( respuesta , "html.parser" );
        
        tag_precio = "quote-summary";
        val_precio = soup.find( id = tag_precio );
        val_precio = val_precio.findChildren("span");
        val_precio = val_precio[1].text;
        val_precio = val_precio.replace( "," , "." );
        val_precio = float(val_precio);
        return val_precio;
        
    else: print ( "------------------Fallo de Conexion------------------" );


def buscarCotizacionMorningStar( pProducto , pIsin  ):
    producto = "funds"
    if pProducto == "ETF": producto = "etf"
    url = "https://www.morningstar.es/es/" + producto + "/snapshot/p_snapshot.aspx?id=" + pIsin;
    peticion = requests.get( url )
    status = peticion.status_code;
    
    if status == 200:
        respuesta = peticion.text;
        soup = BeautifulSoup( respuesta , "html.parser" );
        
        tag_precio = "overviewQuickstatsDiv";
        val_precio = soup.find( id = tag_precio );
        val_precio = val_precio.findChildren("td");
        val_precio = val_precio[3].text;
        moneda , val_precio = val_precio.split("\xa0");
        val_precio = val_precio.replace( "," , "." );
        val_precio = float(val_precio);
        if moneda == "USD": val_precio = usd_To_eur(val_precio);
        return val_precio;
        
    else: print ( "------------------Fallo de Conexion------------------" );
        
    
def usd_To_eur( precio ):
    url = "https://es.finance.yahoo.com/quote/EURUSD=X/";
    cambio = buscarCotizacionYahoo( url );
    return precio/cambio

    
def buscarTodasCotizaciones( cotizaciones ):   
    precios = [];
    for cotizacion in cotizaciones:
        precio = buscarCotizacionYahoo( cotizacion );
        precios.append( precio );
    return precios;


def guardarTodasCotizaciones( nombre , precios ):  
    fichero = open( nombre , 'w');
    for precio in precios:
        fichero.write( precio );
        fichero.write( "\n" ); 
    fichero.close;

####################################################################    
#---------------------- BUSCAR DISTRIBUCIONES ---------------------#
####################################################################
    
def buscarDistribucionMorningStar( pDistribucion , pTabla , pColumnas , pProducto , pIsin  ):
    distribucion = []
    producto = "funds"
    if pProducto == "ETF": producto = "etf"
    url = "https://www.morningstar.es/es/" + producto + "/snapshot/p_snapshot.aspx?id=" + pIsin;
    peticion = requests.get( url )
    status = peticion.status_code;
    
    if status == 200:
        respuesta = peticion.text;
        soup = BeautifulSoup( respuesta , "html.parser" );
        
        tabla = soup.find( id = pDistribucion );
        tabla = tabla.findChildren("table")[pTabla];

        for tr in tabla.children:
            if tr.find( "td" , {'class': 'label'}):
                for cabecera , cuerpo in pColumnas:
                    nombre = tr.findChildren("td")[cabecera].text;
                    peso = tr.findChildren("td")[cuerpo].text;
                    peso = peso.replace( "," , "." );
                    peso = float(peso);
                    elemento = [ nombre , peso ]
                    distribucion.append( elemento )
                
        return distribucion
        
    else: print ( "------------------Fallo de Conexion------------------" );

def buscarColocacionActivos( pProducto , pIsin ):
    return buscarDistribucionMorningStar( "overviewPortfolioAssetAllocationDiv" , 0 , [[0,3]] , pProducto , pIsin )

def buscarRegiones( pProducto , pIsin ):
    return buscarDistribucionMorningStar( "portfolioRegionalBreakdownDiv" , 1 , [[0,1]] , pProducto , pIsin )

def buscarSectores( pProducto , pIsin ):
    return buscarDistribucionMorningStar( "portfolioSectorBreakdownDiv" , 1 , [[0,1]] , pProducto , pIsin )

def buscarCapitalizaciones( pProducto , pIsin ):
    return buscarDistribucionMorningStar( "portfolioEquityStyleDiv" , 4 , [[0,1]] , pProducto , pIsin )

def buscarVencimientos( pProducto , pIsin ):
    return buscarDistribucionMorningStar( "portfolioBondStyleDiv" , 5 , [[0,1]] , pProducto , pIsin )

def buscarCalidadCrediticia( pProducto , pIsin ):
    return buscarDistribucionMorningStar( "portfolioBondStyleDiv" , 8 , [[0,1],[3,4]] , pProducto , pIsin )

####################################################################    
#-------------------------------MAIN-------------------------------#
####################################################################

def main1():
    cotizaciones = [];
    cotizaciones.append("https://es.finance.yahoo.com/quote/0P00000WLG.F?p=0P00000WLG.F&.tsrc=fin-srch");
    cotizaciones.append("https://es.finance.yahoo.com/quote/0P00012I69.F?p=0P00012I69.F&.tsrc=fin-srch");
    cotizaciones.append("https://es.finance.yahoo.com/quote/IWDA.L?p=IWDA.L&.tsrc=fin-srch");
    cotizaciones.append("https://es.finance.yahoo.com/quote/ITX.MC?p=ITX.MC&.tsrc=fin-srch");
    
    precios = buscarTodasCotizaciones( cotizaciones );
    #guardarTodasCotizaciones( "precios.txt" , precios );   
    print(precios);

def main2():
    producto = "funds";
    isin = "F0GBR052TN";
    cotizacion = buscarColocacionActivos( producto , isin );
    for nombre , peso in cotizacion:
        print( "nombre" , nombre , "peso" , peso )
        
    producto = "etf";
    isin = "F00000T1HT";
    cotizacion = buscarCalidadCrediticia( producto , isin );
    print(cotizacion)
    for nombre , peso in cotizacion:
        print( "nombre" , nombre , "peso" , peso )
    
#main2()

    