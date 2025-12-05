# -*- coding: utf-8 -*-
import random;
import seaborn;
import binascii

####################################################################    
#----------------------------- COLORES ----------------------------#
#################################################################### 

def randomColor():
    levels = range(32,256,32);
    return tuple(random.choice(levels) for _ in range(3));

def randomColorString( pOpacidad ):
    r = str(random.randint(0,255));   g = str(random.randint(0,255));   b = str(random.randint(0,255));
    color = "rgba( " + r + ", " + g + ", " + b + ", " + str(pOpacidad) + " )"
    return color
    
def getDegradado( r , g , b ):
    pVelocidad = 50;
    #          (  R  ,   G   ,   B   )       (  R  ,   G   ,   B   )
    # Fase 1:  ( 250 ,  5    ,  5    )  To   ( 250 ,  250  ,  5    )  g --> 250
    # Fase 2:  ( 250 ,  250  ,  5    )  To   ( 5   ,  250  ,  5    )  r --> 5
    # Fase 3:  ( 5   ,  250  ,  5    )  To   ( 5   ,  250  ,  250  )  b --> 250
    # Fase 4:  ( 5   ,  250  ,  250  )  To   ( 5   ,  5    ,  250  )  g --> 5
    # Fase 5:  ( 5   ,  5    ,  250  )  To   ( 250 ,  5    ,  250  )  r --> 250
    # Fase 6:  ( 250 ,  5    ,  250  )  To   ( 255 ,  5    ,  5    )  b --> 5  

    if   r == 250 and g < 250  and b == 0  : g += pVelocidad;
    elif r > 0    and g == 250 and b == 0  : r -= pVelocidad;
    elif r == 0   and g == 250 and b < 250 : b += pVelocidad;
    elif r == 0   and g > 0    and b == 250: g -= pVelocidad;
    elif r < 250  and g == 0   and b == 250: r += pVelocidad;
    elif r == 250 and g == 0   and b > 0   : b -= pVelocidad;
    return r , g , b;
    
def colorHexadecimalToRGB( pColor ):
    color = pColor.lstrip('#')
    color = tuple( int( color[i:i+2] , 16 ) for i in ( 0 , 2 , 4 ) )
    color = "rgba( " + str(color[0]) + " , " + str(color[1]) + " , " + str(color[2]) + " , 1 )"
    return color

def colorRGBToHexadecimal( pColor ):
    color = pColor.lstrip( 'rgba(' ).replace( " " , "" );
    r , g , b , o = color.split(',')
    r = intToHex(r);
    g = intToHex(g);
    b = intToHex(b);
    color = "#" + r + g + b;
    return color

####################################################################    
#------------------------------ PARSER ----------------------------#
####################################################################

def parseMesToInt( pMes ):
    if pMes == "Enero" or pMes == "enero": mes = 1;
    elif pMes == "Febrero" or pMes == "febrero": mes = 2;
    elif pMes == "Marzo" or pMes == "marzo": mes = 3;
    elif pMes == "Abril" or pMes == "abril": mes = 4;
    elif pMes == "Mayo" or pMes == "mayo": mes = 5;
    elif pMes == "Junio" or pMes == "junio": mes = 6;
    elif pMes == "Julio" or pMes == "julio": mes = 7;
    elif pMes == "Agosto" or pMes == "agosto": mes = 8;
    elif pMes == "Septiembre" or pMes == "septiembre": mes = 9;
    elif pMes == "Octubre" or pMes == "octubre": mes = 10;
    elif pMes == "Noviembre" or pMes == "noviembre": mes = 11;
    elif pMes == "Diciembre" or pMes == "diciembre": mes = 12;
    else: mes = 0; print( "ERROR se ha introducido un mes que no existe: " , pMes )
    return mes;

def intToHex( pInt ):
    resultado = int(pInt); 
    if resultado == 0:
       resultado = "00"
    else: 
        if resultado > 255 or resultado < 0: resultado = 255;
        resultado = hex( resultado ).lstrip('0x');
        if len(resultado) != 2: resultado = "0" + resultado;
    return resultado;


def getYear( date ):
    if date == "": return "";
    else:
        ano , mes , dia = date.split("-")
        return ano;

####################################################################    
#-------------------------------MAIN-------------------------------#
####################################################################

def main():
    i  = 0;
    r = 250;  g = 5;   b = 5;
    while i<500:
        i += 1
        r , g , b = getDegradado( r , g , b )
        print( r , g , b )

#main()
#print( colorHexadecimalToRGB( "#8346cb" ) )
#print( colorRGBToHexadecimal( 'rgba( 7 , 181 , 42 , 1 )' ) )