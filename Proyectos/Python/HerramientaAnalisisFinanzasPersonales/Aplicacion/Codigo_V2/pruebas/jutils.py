# -*- coding: utf-8 -*-

from app import Seccion as secciones
from lib import SQL as sql
from lib import Ficheros as ficheros
from lib import Utils as utils

from pruebas import Jsql as jsql


def jutils():
    print("####################################################################")   
    print("#------------------------------ UTILS -----------------------------#")
    print("####################################################################")
    parser()
    






####################################################################    
#----------------------------- COLORES ----------------------------#
####################################################################


####################################################################    
#------------------------------ Fechas ----------------------------#
####################################################################



####################################################################    
#-------------------------- CAMBIO DE BASE ------------------------#
####################################################################



####################################################################    
#------------------------------ PARSER ----------------------------#
####################################################################


def parser():
    print("# ---------------------------------------- #")
    print("#----------------- Parser -----------------#")
    print("# ---------------------------------------- #")
    print( "isFloat:  " , str( isFloat( ) ) )
    print( "getHash:  " , str( getHash( ) ) )


def isFloat( ):
    funciona = True
    if not utils.isFloat("1234"): 
        funciona = False
        print( "  * '1234' si es un numero" )
    if not utils.isFloat(1234): 
        funciona = False
        print( "  * 1234 si es un numero" )
    if not utils.isFloat("12.34"): 
        funciona = False
        print( "  * '12.34' si es un numero" )
    if not utils.isFloat(12.34): 
        funciona = False
        print( "  * 12.34 si es un numero" )
    if utils.isFloat("abdef"): 
        funciona = False
        print( "  * abdef no es un numero" )
    if utils.isFloat("ab3def"): 
        funciona = False
        print( "  * ab3def no es un numero" )
    if utils.isFloat("1*4"): 
        funciona = False
        print( "  * 1*4 no es un numero" )
    return funciona


####################################################################    
#------------------------------ HASH ------------------------------#
####################################################################

def getHash( ):
    funciona = True
    if not utils.getHash( "1234" + "1234" ) == "1718c24b10aeb8099e3fc44960ab6949ab76a267352459f203ea1036bec382c2":
        funciona = False


####################################################################    
#------------------------------ LISTAS ----------------------------#
####################################################################

def diferenciaListas( ):
    a = [ "a" , "b" , "c" , "d" ]
    return True

