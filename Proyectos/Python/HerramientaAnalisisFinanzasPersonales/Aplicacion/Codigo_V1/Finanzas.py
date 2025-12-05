# -*- coding: utf-8 -*-
import Z_Scraper as scraper;
import Z_SQLReader as sql;
import Z_Utils as utilidades;
#from lib import Z_Graficas as graficas;


####################################################################    
#------------------------------ CLASES ----------------------------#
####################################################################

# ----------------------------------------------- #
# -------------- LISTA OPERACIONES -------------- #
# ----------------------------------------------- #

class ListaOperaciones:
    
    def __init__( self , pUsuario ):
        # SQL
        self.usuario = pUsuario
        # listas
        self.listaOperaciones = [];
        # resumen
        self.resumenAnos = ListaResumen();
        self.resumen = Resumen( "global" )
     
    def setUsuario( self , pUsuario ): self.usuario = pUsuario;
        
    def ImportarDatos( self ):       
        resultado = sql.getFinanzas( self.usuario );    
        for date , clase , asunto , descripcion , gasto , ingreso in resultado:
            operacion = Operacion( date , clase , asunto , descripcion , gasto , ingreso )
            self.listaOperaciones.append( operacion )

        
    def calcularResumenes( self ):
        for operacion in self.listaOperaciones:
            ano = str(operacion.date.year)
            self.resumen.anadirResumen( operacion.clase , operacion.gasto , operacion.ingreso )
            self.resumenAnos.anadirResumen( ano , operacion.clase , operacion.gasto , operacion.ingreso )                   
            
        self.resumenAnos.calcularResumen();
        self.resumen.calcularResumen();
              
        
    def anadirColores( self ):
        for clase in self.resumen.clases:
            #color = utilidades.randomColorString(1)
            color = sql.getColorFinanzas( clase , self.usuario )
            self.resumen.anadirColor( clase , color )
            self.resumenAnos.anadirColor( clase , color )

    def main( self ):
        self.ImportarDatos(); 
        self.calcularResumenes();
        self.anadirColores()

    def clear( self ):
        # listas
        self.listaOperaciones = [];
        # resumen
        self.resumenAnos = ListaResumen();
        self.resumen = Resumen( "global" )
        
# --------------------------------------- #
# -------------- OPERACION -------------- #
# --------------------------------------- #

class Operacion:
    
    def __init__( self , pDate , pClase , pAsunto , pDescripcion , pGasto , pIngreso ):       
        # datos
        self.date = pDate;
        self.clase = pClase;
        self.asunto = pAsunto; 
        self.descripcion = pDescripcion;
        self.gasto = pGasto;
        self.ingreso = pIngreso;

  
    def print( self ):
         print( "   - " , self.date , self.clase , self.gasto , self.ingreso );
    

# ---------------------------------------- #
# ------------ LISTA RESUMEN ------------- #
# ---------------------------------------- #

class ListaResumen:
    
    def __init__( self ):
        self.listaResumen = {}

    # ------------ SETTERS ------------- #
    def anadirResumen( self , pResumen , pclase , pGasto , pIngreso ):        
        if pResumen in self.listaResumen:
            self.listaResumen[ pResumen ].anadirResumen( pclase , pGasto , pIngreso )
        else:
            resumen = Resumen( pResumen )
            resumen.anadirResumen( pclase , pGasto , pIngreso )
            self.listaResumen[ pResumen ] =  resumen;
    
    
    def anadirColor( self , pclase , pColor ):
        for resumen in self.listaResumen:
            self.listaResumen[resumen].anadirColor( pclase , pColor )
        
    # ------------ CALCULOS ------------- #
    def calcularResumen( self ):
        for resumen in self.listaResumen:
            self.listaResumen[ resumen ].calcularResumen()
    
    
    # ------------ GETTERS ------------- #
    def getCabeceras( self ):
        cabeceras = {}
        for resumen in self.listaResumen:
            clases = self.listaResumen[ resumen ].clases
            for clase in clases:
                if clase not in cabeceras: cabeceras[ clase ] = clases[ clase ].color
        return cabeceras

    def getCuerpo( self ):
        cuerpoGastos = {}
        cuerpoIngresos = {}
        for resumen in self.listaResumen:            
            cuerpoGastos[ resumen ] = self.listaResumen[resumen].getGastos();
            cuerpoIngresos[ resumen ] = self.listaResumen[resumen].getIngresos();
        return cuerpoGastos , cuerpoIngresos;

    def getResumenes( self ):        
        return self.listaResumen
           
    # ------------ PRINT ------------- #    
    def print( self ):
        for resumen in self.listaResumen:
            self.listaResumen[resumen].print()

# ---------------------------------------- #
# --------------- RESUMEN ---------------- #
# ---------------------------------------- #
    
class Resumen:
    
    def __init__( self , pDescripcion ):
        self.descripcion = pDescripcion;
        # listas
        self.clases = {};
        # resumen
        self.totalIngresos = 0;
        self.totalGastos = 0;
        self.ahorrado = 0;
        self.invertido = 0;

     # ------------ SETTERS ------------- #
    def anadirResumen( self , pClase , pGasto , pIngreso ):
        if pClase in self.clases:
            self.clases[ pClase ].anadirResumen( pGasto , pIngreso )
        else:
            clase = Clase( pClase , pGasto , pIngreso )
            self.clases[ pClase ] = clase
            
    def anadirColor( self , pClase , pColor ):
        if pClase in self.clases:
            self.clases[ pClase ].anadirColor( pColor )

    # ------------ CALCULOS ------------- #
    def calcularResumen( self ):
        for clase in self.clases:
            self.totalGastos += self.clases[clase].gasto        
            self.totalIngresos += self.clases[clase].ingreso
        
        self.ahorrado = self.totalIngresos - self.totalGastos;
        
        if "Inversion" in self.clases: 
            self.invertido += self.clases["Inversion"].gasto;
            del self.clases["Inversion"]
        if "Inversion" in self.clases: 
            self.invertido -= self.clases["Inversion"].ingreso;
            del self.clases["Inversion"]
            
    # ------------ GETTERS ------------- #
    def getGastos( self ):
        gastos = {}
        for clase in self.clases:
            gastos[clase] = self.clases[clase].gasto
        return gastos
    
    def getIngresos( self ):
        ingresos = {}
        for clase in self.clases:
            ingresos[clase] = self.clases[clase].ingreso
        return ingresos
    
    def getColores( self ):
        colores = []
        for clase in self.clases:
            colores[clase] = self.clases[clase].color
        return colores
    

    def getCabeceras( self ):
        cabeceras = []
        for clase in self.clases:
            cabeceras.append( clase )
        return cabeceras
    
    def getAtributo( self , pAtributo ):
        atributos = []
        for clase in self.clases:
            if pAtributo == "ingreso": atributos.append( self.clases[clase].ingreso )
            elif pAtributo == "color": atributos.append( self.clases[clase].color )
            else: atributos.append( self.clases[clase].gasto )
        return atributos
        
    # ------------ PRINT ------------- #
    def print( self ):
        print("################ " + self.descripcion + " ################");
        print("-------- Gastos --------")
        for clase in self.clases:
            print( clase , self.clases[clase].gasto )        
        print("-------- Ingresos --------")
        for clase in self.clases:
            print( clase , self.clases[clase].ingreso )
        print("-------- Resumen --------")
        print("Ingresado" , self.totalIngresos )
        print("Gastado" , self.totalGastos )        
        print("Ahorrado" , self.ahorrado )
        print("Invertido" , self.invertido )
        print("-------- Colores --------")
        for clase in self.clases:
            self.clases[ clase ].print() 
            
# ---------------------------------------- #
# ---------------- CLASE ----------------- #
# ---------------------------------------- #

class Clase:
    
    def __init__( self , pDescripcion , pGasto , pIngreso ):
        self.descripcion = pDescripcion;
        self.gasto = pGasto;
        self.ingreso = pIngreso;
        self.color = "";

    # ------------ SETTERS ------------- #
    def anadirResumen( self , pGasto , pIngreso ):
        self.gasto += pGasto;
        self.ingreso += pIngreso;
        
    def anadirColor( self , pColor ):
         self.color = pColor;
    
    def print( self ):
        print( "  - " , self.descripcion , self.color );
        
####################################################################    
#------------------------------- MAIN -----------------------------#
####################################################################                
                
       
def main_1():
    
    fuente = 'bd'; # 'bd'
    #ruta = 'C:/Users/david/Dropbox (Personal)/Finanzas/Scraper/BaseDatos';
    ruta = 'C:/Users/Devilvil/Desktop/Scraper/BaseDatos';
    finanzas_csv = '/FinanzasPersonales.csv';
    usuario = 'davidcuesta';
    
    listaOperaciones = ListaOperaciones( usuario )
    listaOperaciones.main();
    
    for operacion in listaOperaciones.listaOperaciones:      
        print( operacion.descripcion );
        operacion.print()

def main_2():
    fuente = 'bd'; # 'bd'
    #ruta = 'C:/Users/david/Dropbox (Personal)/Finanzas/Scraper/BaseDatos';
    ruta = 'C:/Users/Devilvil/Desktop/Scraper/BaseDatos';
    finanzas_csv = '/FinanzasPersonales.csv';
    usuario = 'davidcuesta';
        
    listaOperaciones = ListaOperaciones( usuario )
    listaOperaciones.main();
    
    listaOperaciones.resumenAnos.print()
    listaOperaciones.resumen.print()      
    #print( listaOperaciones.resumenAnos.getCabeceras() )
    #print( listaOperaciones.resumenAnos.getCuerpo() )
    

def main_3():
    
    fuente = 'bd'; # 'bd'
    #ruta = 'C:/Users/david/Dropbox (Personal)/Finanzas/Scraper/BaseDatos';
    ruta = 'C:/Users/Devilvil/Desktop/Scraper/BaseDatos';
    finanzas_csv = '/FinanzasPersonales.csv';
    usuario = 'davidcuesta';
    
    listaOperaciones = ListaOperaciones( usuario )
    listaOperaciones.main();
    
    print( listaOperaciones.resumen.getCabeceras() )
    print(  listaOperaciones.resumen.getAtributo( "gasto" ) )
    print(  listaOperaciones.resumen.getAtributo( "color" ) )
    
    
#main_1( );
        