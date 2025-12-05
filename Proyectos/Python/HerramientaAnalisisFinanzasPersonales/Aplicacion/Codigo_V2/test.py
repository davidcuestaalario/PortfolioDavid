# -*- coding: utf-8 -*-
import datetime

from app import Seccion as secciones

from lib import SQL as sql
from lib import Ficheros as ficheros
from lib import Utils as utils
from lib import Scraper as scraper

from pruebas import Jsql as jsql
from pruebas import jutils

####################################################################    
#------------------------------ TESTS -----------------------------#
####################################################################

def main0():
    jsql.jsql()
    jutils.jutils()




def main1():
    #matriz = [ ["1;2;3;4;5" ] , ["1;2;3;4;5" ] ]
    #ficheros.crearFichero( "Hola3" , matriz )
    
    pVector = ["aaaaaaaaaaa;1.566","22;1.555;blabla"]
    pVector = utils.concatenarStringVector( pVector )
    print(pVector)


    a = [ "a" , "b" , "c" , "d" ]
    b = [ "a" , "d" ]
    c = [ [ "a" , "d" ] , [ "b" , "d" ] , [ "c" , "d" ] , [ "d" , "d" ] ]
    d = []
    for x , y in c: d.append( x ) 

    print ( "LA LISTA " , utils.isStr( a ) )
    print ( "LA ESTRING " , utils.isStr( "Hola que ase" ) )
    #print ( utils.diferenciaListas( a , b ) )
    #print ( utils.diferenciaListas( d , b ) )


def main2():
    producto = "funds";
    isin = "F0GBR052TN";
    cotizacion = scraper.allocationComposicion_MorningStar( producto , isin )
    for nombre , peso in cotizacion:
        print( "nombre" , nombre , "peso" , peso )
        
    producto = "etf";
    isin = "F00000T1HT";
    cotizacion = scraper.allocationCalidadCrediticia_MorningStar( producto , isin );
    print(cotizacion)
    for nombre , peso in cotizacion:
        print( "nombre" , nombre , "peso" , peso )

    
def main3():
    cotizacion = scraper.serieCotizaciones_YahooFinance( "AAPL" , datetime.datetime(2000,1,1) , datetime.datetime(2000,2,1) )
    print( cotizacion )


def main4():
    cotizacion1 = scraper.cotizacionFecha_YahooFinance( "0P00011HBM.F" , datetime.date(2021,9,9) )
    cotizacion2 = scraper.cotizacionFecha_YahooFinance( "0P00011HBM.F" , '2021-9-12' )
    print( cotizacion1 )
    print( cotizacion2 )
    
    
def main5():
    i  = 0;
    r = 250;  g = 0;   b = 0;
    while i<500:
        i += 1
        r , g , b = utils.getDegradado( r , g , b , 100 )
        color = "rgba( " + str(r) + ", " + str(g) + ", " + str(b) + ", 1 )"
        print( color )

main4()



