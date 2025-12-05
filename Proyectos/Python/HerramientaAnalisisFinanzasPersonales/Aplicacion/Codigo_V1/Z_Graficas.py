# -*- coding: utf-8 -*-
from matplotlib import pyplot;
import pandas
import seaborn

####################################################################    
#-----------------------------CIRCULAR-----------------------------#
####################################################################

def circular( titulo , valores , etiquetas , coloresFondo , coloresLetra  ):
    
    #pyplot.rcParams['toolbar'] = 'none';
        
    etiquetas = pyplot.pie( valores , colors = coloresFondo , labels = etiquetas , 
                           autopct = '%1.1f%%' , shadow = True );
    
    i = 0;
    for etiqueta in etiquetas[2]:
        etiqueta.set_color( coloresLetra[ i ] );
        i += 1;
    
    pyplot.axis('equal');
    #pyplot.legend( labels = etiquetas );
    pyplot.title( titulo );
    pyplot.show();
    pyplot.savefig( "res/" + titulo + ".png" );

####################################################################    
#------------------------ DESDE FICHEROS CSV ----------------------#
####################################################################

def cargarCSV( csv ):  
    csv = "csv/" + csv + ".csv";
    datos = pandas.read_csv( csv , sep = 'delimiter' , header = 0);
    tabla = pandas.DataFrame( datos );
    return tabla;

def finanzasPersonales(  ):
    # Dia ; Mes ; Ano ; Clasificacion ; Asunto ; Descripcion ; Gasto ; Ingreso
    csv = "FinanzasPersonales";
    tabla = cargarCSV( csv );
    print( "COLUMNAS   " + tabla.colums )
    tabla.columns = [u'Dia', u'Mes', u'Ano', u'Clasificacion', u'Asunto', u'Descripcion', u'Gasto', u'Ingreso' ]
    
    #totalGastos = tabla.groupby("Clasificacion")['Gasto'].sum()
    #totalGastos.plot( kind = 'bar' , legends = 'reverse' )
    

####################################################################    
#------------------------------- MAIN -----------------------------#
####################################################################

def main():
    titulo = "prueba";
    etiquetas = ("a","b","c");
    valores = (10 , 5 , 1);
    coloresFondo = ('red' , 'blue', 'green');
    coloresLetra = ('white', 'black' , 'pink');
    
    circular( titulo , valores , etiquetas , coloresFondo , coloresLetra );

    
#finanzasPersonales();