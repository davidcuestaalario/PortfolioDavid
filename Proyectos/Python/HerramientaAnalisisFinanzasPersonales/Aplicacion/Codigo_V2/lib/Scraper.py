# -*- coding: utf-8 -*-
import datetime
import requests
import numpy
import pandas
import json

from pandas_datareader import data
from bs4 import BeautifulSoup

from lib import Utils as utils 

msgFalloConexion = "------------------Fallo de Conexion------------------"

ApiKey_Alphavantage = '2TVVG7U8MMGINE1T'

####################################################################    
#----------------------------- SCRAPER ----------------------------#
####################################################################

#------------------------------------------------------------------#    
#------------------------------ Cache -----------------------------#
#------------------------------------------------------------------#

COTIZACIONFECHA = {}
SERIECOTIZACIONES = {}

def limpiarCache():
    COTIZACIONFECHA.clear()
    SERIECOTIZACIONES.clear()

#------------------------------------------------------------------#    
#--------------------------- Cotizaciones -------------------------#
#------------------------------------------------------------------#

#--------------------------- YahooFinance -------------------------#

def cotizacionActual_YahooFinance( pProducto ):  
    url = "https://es.finance.yahoo.com/quote/" + pProducto + "?p=" + pProducto
    print( url )
    headers = {"User-Agent":"Mozilla/5.0"}
    
    peticion = requests.get( url , headers=headers )
    status = peticion.status_code
    if status == 200: 
        respuesta = peticion.text
        soup = BeautifulSoup( respuesta , "html.parser" )
        
        tag_precio = "quote-summary";
        val_precio = soup.find( id = tag_precio )
        val_precio = val_precio.findChildren("td")        
        val_precio = val_precio[1].text
        val_precio = val_precio.replace( "," , "." )
        print( "val_precio : " + val_precio )
        return float ( val_precio )
        
    else: print( msgFalloConexion )


def cotizacionFecha_YahooFinance( pProducto , pFecha ):
    pFecha = utils.ajustarSoloFecha( pFecha )
    val_precio = None
    codigo = pProducto + '_' + str( pFecha )
    if codigo in COTIZACIONFECHA:
        val_precio = COTIZACIONFECHA[ codigo ]
        #print( "En Cache: " + codigo )
    else:
        if pFecha == datetime.datetime.now().date():
            val_precio = cotizacionActual_YahooFinance( pProducto )
        else:
            val_precio = serieCotizaciones_YahooFinance( pProducto , pFecha , utils.nextMonth( pFecha ) )
            if val_precio != None: fecha , val_precio = val_precio[0] 
        COTIZACIONFECHA[ codigo ] = val_precio
    return val_precio


def serieCotizaciones_YahooFinance( pProducto , pFechaInicio , pFechaFin ):
    pFechaInicio = utils.ajustarSoloFecha( pFechaInicio )
    pFechaFin = utils.ajustarSoloFecha( pFechaFin )
    serie = None
    
    codigo = pProducto + '_' + str( pFechaInicio ) + '_' + str( pFechaFin )
    if codigo in SERIECOTIZACIONES:
        serie = SERIECOTIZACIONES[ codigo ]
        print( "En Cache: " + codigo )
    else:
        try: 
            serie = data.DataReader( pProducto , data_source = 'yahoo' , start = pFechaInicio , end = pFechaFin )
            serie = serie.reset_index().to_json(None, orient='records', date_format='iso')
            serie = utils.ajustarSerieCotizaciones_YahooFinance( serie , 'Adj Close' ) # Close
            SERIECOTIZACIONES[ codigo ] = serie
        except: print( msgFalloConexion )      
    return serie
    

#--------------------------- Morning Star -------------------------#


def cotizacionActual_MorningStar( pProducto , pIsin  ):
    producto = "funds"
    if pProducto == "ETF": producto = "etf"
    url = "https://www.morningstar.es/es/" + producto + "/snapshot/p_snapshot.aspx?id=" + pIsin
    peticion = requests.get( url )
    status = peticion.status_code
    
    if status == 200:
        respuesta = peticion.text;
        soup = BeautifulSoup( respuesta , "html.parser" )
        
        tag_precio = "overviewQuickstatsDiv"
        val_precio = soup.find( id = tag_precio )
        val_precio = val_precio.findChildren("td")
        val_precio = val_precio[3].text;
        moneda , val_precio = val_precio.split("\xa0")
        val_precio = val_precio.replace( "," , "." )
        val_precio = float(val_precio)
        val_precio = val_precio * tipoCambio_YahooFinance( moneda , datetime.datetime.now().date() )
        return val_precio
        
    else: print( msgFalloConexion )
    

def serieCotizaciones_MorningStar( pProducto , pFechaInicio , pFechaFin ):
    try: 
        serie = data.DataReader( pProducto , data_source = 'morningstar' , start = pFechaInicio , end = pFechaFin )
        serie.reset_index().to_json(None, orient='records', date_format='iso')
        return serie
    except: print( msgFalloConexion )

#--------------------------- Alphavantage -------------------------#


def serieCotizaciones_Alphavantage( pProducto ):
    funcion = 'TIME_SERIES_WEEKLY'
    url = "https://www.alphavantage.co/query?function=" + funcion + "&symbol=" + pProducto + "&apikey=" + ApiKey_Alphavantage

    peticion = requests.get( url )
    status = peticion.status_code
    
    if status == 200: return peticion.json();
    else: print( msgFalloConexion );
  
    
#------------------------------------------------------------------#    
#-------------------------- Cambios Divisa ------------------------#
#------------------------------------------------------------------#

#--------------------------- YahooFinance -------------------------#

def tipoCambio_YahooFinance( pMoneda , pFecha ):
    tipoCambio = 1
    if pMoneda == 'USD': tipoCambio = 1/cotizacionFecha_YahooFinance( 'EURUSD%3DX' , pFecha )
    return tipoCambio

#------------------------------------------------------------------#    
#--------------------------- Allocations --------------------------#
#------------------------------------------------------------------#

#--------------------------- Morning Star -------------------------#


def allocation_MorningStar( pDistribucion , pTabla , pColumnas , pProducto , pIsin  ):
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
        
    else: print( msgFalloConexion );


def allocationComposicion_MorningStar( pProducto , pIsin ):
    return allocation_MorningStar( "overviewPortfolioAssetAllocationDiv" , 0 , [[0,3]] , pProducto , pIsin )

def allocationRegion_MorningStar( pProducto , pIsin ):
    return allocation_MorningStar( "portfolioRegionalBreakdownDiv" , 1 , [[0,1]] , pProducto , pIsin )

def allocationSector_MorningStar( pProducto , pIsin ):
    return allocation_MorningStar( "portfolioSectorBreakdownDiv" , 1 , [[0,1]] , pProducto , pIsin )

def allocationCapitalizacion_MorningStar( pProducto , pIsin ):
    return allocation_MorningStar( "portfolioEquityStyleDiv" , 4 , [[0,1]] , pProducto , pIsin )

def allocationVencimiento_MorningStar( pProducto , pIsin ):
    return allocation_MorningStar( "portfolioBondStyleDiv" , 5 , [[0,1]] , pProducto , pIsin )

def allocationCalidadCrediticia_MorningStar( pProducto , pIsin ):
    return allocation_MorningStar( "portfolioBondStyleDiv" , 8 , [[0,1],[3,4]] , pProducto , pIsin )


