# -*- coding: utf-8 -*-
import Z_Scraper as scraper;
import Z_SQLReader as sql;
import Z_Utils as utilidades;
import Z_html as html;
#import Z_Graficas as graficas;

####################################################################    
#------------------------------ CLASES ----------------------------#
####################################################################

# ----------------------------------------------- #
# -------------- LISTA INVERSIONES -------------- #
# ----------------------------------------------- #

class ListaInversiones:
    
    def __init__( self , pUsuario ):
        # SQL
        self.usuario = pUsuario
        # listas
        self.listaInversiones = [];
        # resumen
        self.resumenActivos = ListaResumen();
        self.resumenEstrategias = ListaResumen();
        self.resumenCategorias = ListaResumen();
        self.resumenBrokers = ListaResumen();
        self.resumen = Resumen( "global" )

    def setUsuario( self , pUsuario ): self.usuario = pUsuario;
        
    def ImportarDatos( self ): 
        # -------------- ACTIVOS -------------- #
        resultado = sql.getActivos( self.usuario );    
        for isin , producto , categoria , estrategia , descripcion , link in resultado:
            cotizacion = 0;
            if producto != "Accion":
               cotizacion = scraper.buscarCotizacionMorningStar( producto , link );
            else:
                cotizacion = scraper.buscarCotizacionYahoo(link);
                
            inversion = Inversion( isin , link , producto , categoria , estrategia , descripcion , cotizacion );
            self.listaInversiones.append( inversion );
    
        # -------------- POSICIONES -------------- #       
        resultado = sql.getPosiciones( self.usuario );        
        for date , isin , titulos , precio , broker , operacion in resultado:
            aportacion = Aportacion( date , titulos , precio , broker , operacion );
            for inversion in self.listaInversiones:
                if inversion.isin == isin:
                    inversion.anadirAportacion( aportacion );
        
        # -------------- COMISIONES -------------- #
        resultado = sql.getComisiones( self.usuario );
        for date , isin , broker , comision , precio in resultado:
            comision = Comision( date , precio , broker , comision );
            for inversion in self.listaInversiones:
                if inversion.isin == isin:
                    inversion.anadirComision( comision );       
    
        # -------------- COMPOSICIONES -------------- #
        allocations = sql.getAllocations( self.usuario );
        regiones = sql.getRegiones( self.usuario );
        sectores = sql.getSectores( self.usuario );
        capitalizaciones = sql.getCapitalizaciones( self.usuario );
        vencimientos = sql.getVencimientos( self.usuario );
        calidades = sql.getCalidadesCrediticias( self.usuario );
        entidades = sql.getEntidadesEmisoras( self.usuario );
        
        for inversion in self.listaInversiones:
            # ---------------- REGIONES ---------------- #
            for isin , allocation , porcentaje  in allocations:               
                if inversion.isin == isin:
                    inversion.anadirAllocation ( allocation , porcentaje );
            # ---------------- REGIONES ---------------- #
            for isin , region , porcentaje  in regiones:               
                if inversion.isin == isin:
                    inversion.anadirRegion ( region , porcentaje );
            # ---------------- SECTORES ---------------- #
            for isin , sector , porcentaje in sectores:            
                if inversion.isin == isin:
                    inversion.anadirSector ( sector , porcentaje );
            # ---------------- CAPITALIZACIONES ---------------- #
            for isin , capitalizacion , porcentaje in capitalizaciones:            
                if inversion.isin == isin:
                    inversion.anadirCapitalizacion ( capitalizacion , porcentaje );
            # ---------------- VENCIMIENTOS ---------------- #        
            for isin , vencimiento , porcentaje in vencimientos:            
                if inversion.isin == isin:
                    inversion.anadirVencimiento ( vencimiento , porcentaje );
            # ---------------- CALIDADES ---------------- #        
            for isin , calidad , porcentaje in calidades:            
                if inversion.isin == isin:
                    inversion.anadirCalidad ( calidad , porcentaje );
            # ---------------- ENTIDADES ---------------- #        
            for isin , entidad , porcentaje in entidades:            
                if inversion.isin == isin:
                    inversion.anadirEntidad ( entidad , porcentaje );
                    
                    
    def calcularResumenes( self ):                
        for inversion in self.listaInversiones:
            # ---------------- RESUMIR APORTACIONES ---------------- #
            for aportacion in inversion.listaAportaciones:
                valor = aportacion.titulos * aportacion.precio
                # ---------------- ACTIVOS ---------------- #
                self.resumenActivos.anadirAportacion( inversion.descripcion , aportacion , inversion.cotizacion )
                self.resumenActivos.ponderarComposiciones( inversion.descripcion , valor , inversion.composiciones  )
                # -------------- ESTRATEGIAS -------------- #
                self.resumenEstrategias.anadirAportacion( inversion.estrategia , aportacion , inversion.cotizacion )
                self.resumenEstrategias.ponderarComposiciones( inversion.estrategia , valor , inversion.composiciones )
                # --------------- CATEGORIAS -------------- #
                self.resumenCategorias.anadirAportacion( inversion.categoria , aportacion , inversion.cotizacion )
                self.resumenCategorias.ponderarComposiciones( inversion.categoria , valor , inversion.composiciones )
                # ---------------- BROKERS ---------------- #  
                self.resumenBrokers.anadirAportacion( aportacion.broker , aportacion , inversion.cotizacion )
                self.resumenBrokers.ponderarComposiciones( aportacion.broker , valor , inversion.composiciones )
                # ---------------- GLOBAL ----------------- #
                self.resumen.anadirAportacion( aportacion , inversion.cotizacion );
                self.resumen.ponderarComposiciones( valor , inversion.composiciones )                
            # ---------------- RESUMIR COMISIONES ---------------- #
            for comision in inversion.listaComisiones:
                # ---------------- ACTIVOS ---------------- #
                self.resumenActivos.anadirComision( inversion.descripcion , comision )
                # -------------- ESTRATEGIAS -------------- #
                self.resumenEstrategias.anadirComision( inversion.estrategia , comision )
                # --------------- CATEGORIAS -------------- #
                self.resumenCategorias.anadirComision( inversion.categoria , comision )
                # ---------------- BROKERS ---------------- #  
                self.resumenBrokers.anadirComision( comision.broker , comision )
                # ---------------- GLOBAL ----------------- #
                self.resumen.anadirComision( comision );
        
        self.resumenActivos.calcularResumen()
        self.resumenEstrategias.calcularResumen()
        self.resumenCategorias.calcularResumen()
        self.resumenBrokers.calcularResumen()
        self.resumen.calcularResumen()
        self.resumen.calcularComposiciones()

    def calcularColores( self , pUsuario ):
        self.resumenActivos.calcularColores("Activo" , pUsuario )
        self.resumenEstrategias.calcularColores("Estrategia" , pUsuario )
        self.resumenCategorias.calcularColores("Categoria" , pUsuario)
        self.resumenBrokers.calcularColores("Broker" , pUsuario ) 

    def main( self ):
        self.ImportarDatos( ); 
        self.calcularResumenes( );
        self.calcularColores( self.usuario );
        
    def clear( self ):
        # listas
        self.listaInversiones = [];
        # resumen
        self.resumenActivos = ListaResumen();
        self.resumenEstrategias = ListaResumen();
        self.resumenCategorias = ListaResumen();
        self.resumenBrokers = ListaResumen();
        self.resumen = Resumen( "global" )
        
# --------------------------------------- #
# -------------- INVERSION -------------- #
# --------------------------------------- #

class Inversion:
        
    def __init__( self , pIsin , pLink , pProducto , pCategoria , pEstrategia , pDescripcion , pCotizacion ):
        # datos
        self.isin = pIsin;
        self.link = pLink;
        self.producto = pProducto;
        self.categoria = pCategoria;
        self.estrategia = pEstrategia;
        self.descripcion = pDescripcion;
        self.cotizacion = pCotizacion;
        # listas
        self.listaAportaciones = [];
        self.listaComisiones = [];
        # Composiciones
        self.composiciones = Composiciones();  

    def anadirAportacion( self , aportacion ):
        self.listaAportaciones.append( aportacion );

    def anadirComision( self , comision ):
        self.listaComisiones.append( comision );    
    
    def anadirAllocation( self , pAllocation , pPorcentaje ):
        self.composiciones.anadirAllocation( pAllocation , pPorcentaje )
        
    def anadirRegion( self , pRegion , pPorcentaje ):
        self.composiciones.anadirRegion( pRegion , pPorcentaje )
        
    def anadirSector( self , pRegion , pPorcentaje ):
        self.composiciones.anadirSector( pRegion , pPorcentaje )
    
    def anadirCapitalizacion( self , pRegion , pPorcentaje ):
        self.composiciones.anadirCapitalizacion( pRegion , pPorcentaje )
        
    def anadirVencimiento( self , pRegion , pPorcentaje ):
        self.composiciones.anadirVencimiento( pRegion , pPorcentaje )
            
    def anadirCalidad( self , pRegion , pPorcentaje ):
        self.composiciones.anadirCalidad( pRegion , pPorcentaje )
                
    def anadirEntidad( self , pRegion , pPorcentaje ):
        self.composiciones.anadirEntidad( pRegion , pPorcentaje )

# --------------------------------------- #
# -------------- APORTACION ------------- #
# --------------------------------------- #

class Aportacion:
        
    def __init__( self , pDate , pTitulos , pPrecio , pBroker , pOperacion ):       
        # datos
        self.date = pDate;
        self.titulos = pTitulos;
        self.precio = pPrecio; 
        self.broker = pBroker;
        self.operacion = pOperacion;
        
    def print( self ):
        print( "   - " , self.date , self.precio , self.titulos , self.broker , self.operacion );

# --------------------------------------- #
# -------------- COMISION --------------- #
# --------------------------------------- #

class Comision:
    
    def __init__( self , pDate , pPrecio , pBroker , pComision ): 
        # datos
        self.date = pDate;
        self.precio = pPrecio; 
        self.broker = pBroker;
        self.comision = pComision;
    
    def anadirComision( self , comision ):
        self.listaComisiones.append( comision );    
    
    def print( self ):
        print( "   - " , self.date , self.precio , self.broker , self.comision );

# --------------------------------------- #
# ----------- COMPOSICIONES ------------- #
# --------------------------------------- #

class Composiciones:
    
    def __init__( self ): 
        self.allocations = ListaComposiciones()
        self.regiones = ListaComposiciones()
        self.sectores = ListaComposiciones()
        self.capitalizaciones = ListaComposiciones()
        self.vencimientos = ListaComposiciones()
        self.calidadesCrediticias = ListaComposiciones()
        self.entidadesEmisoras = ListaComposiciones()
    
    # ------------ SETTERS ------------- #
    
    def anadirAllocation( self , pAllocation , pPorcentaje ):
        self.allocations.anadirComposicion( pAllocation , pPorcentaje )
        
    def anadirRegion( self , pRegion , pPorcentaje ):
        self.regiones.anadirComposicion( pRegion , pPorcentaje )
    
    def anadirSector( self , pSector , pPorcentaje ):
        self.sectores.anadirComposicion( pSector , pPorcentaje )
    
    def anadirCapitalizacion( self , pCapitalizacion , pPorcentaje ):
        self.capitalizaciones.anadirComposicion( pCapitalizacion , pPorcentaje )        

    def anadirVencimiento( self , pVencimiento , pPorcentaje ):
        self.vencimientos.anadirComposicion( pVencimiento , pPorcentaje )  
    
    def anadirCalidad( self , pCalidad , pPorcentaje ):
        self.calidadesCrediticias.anadirComposicion( pCalidad , pPorcentaje ) 
                
    def anadirEntidad( self , pEntidad , pPorcentaje ):
        self.entidadesEmisoras.anadirComposicion( pEntidad , pPorcentaje )
    
    # ------------ CALCULOS ------------- #
    
    def ponderarComposiciones( self , pAportacion , pComposiciones ):
        self.allocations.ponderarComposiciones( pAportacion , pComposiciones.allocations )
        self.regiones.ponderarComposiciones( pAportacion , pComposiciones.regiones )
        self.sectores.ponderarComposiciones( pAportacion , pComposiciones.sectores )
        self.capitalizaciones.ponderarComposiciones( pAportacion , pComposiciones.capitalizaciones )
        self.vencimientos.ponderarComposiciones( pAportacion , pComposiciones.vencimientos )
        self.calidadesCrediticias.ponderarComposiciones( pAportacion , pComposiciones.calidadesCrediticias )
        self.entidadesEmisoras.ponderarComposiciones( pAportacion , pComposiciones.entidadesEmisoras )
          
    def calcularComposiciones( self ):
        self.allocations.calcularComposiciones( )
        self.regiones.calcularComposiciones( )
        self.sectores.calcularComposiciones( )
        self.capitalizaciones.calcularComposiciones( )
        self.vencimientos.calcularComposiciones( )
        self.calidadesCrediticias.calcularComposiciones( )
        self.entidadesEmisoras.calcularComposiciones( )
    
    # ------------ GRAFICOS ------------- #
    
    def graficoComposiciones( self , pTitulo , pUsuario ):
        informacion = ""        
        tipo = "allocation"
        informacion += self.allocations.graficoComposicion( pTitulo + "_" + tipo , tipo , pUsuario )       
        tipo = "region"
        informacion += self.regiones.graficoComposicion( pTitulo + "_" + tipo , tipo , pUsuario )        
        tipo = "sector"
        informacion += self.sectores.graficoComposicion( pTitulo + "_" + tipo , tipo , pUsuario )        
        tipo = "capitalizacion"
        informacion += self.capitalizaciones.graficoComposicion( pTitulo + "_" + tipo , tipo , pUsuario )        
        tipo = "vencimiento"
        informacion += self.vencimientos.graficoComposicion( pTitulo + "_" + tipo , tipo , pUsuario )       
        tipo = "calidad"
        informacion += self.calidadesCrediticias.graficoComposicion( pTitulo + "_" + tipo , tipo , pUsuario )     
        tipo = "entidad"
        informacion += self.entidadesEmisoras.graficoComposicion( pTitulo + "_" + tipo , tipo , pUsuario )    
        return informacion;
    
    # ------------ PRINT ------------- #
        
    def print( self ):
        print( "* allocations" )
        self.allocations.print( ) 
        print( "* Regiones" )
        self.regiones.print( )       
        print( "* Sectores" )
        self.sectores.print( )      
        print( "* Capitalizaciones" )
        self.capitalizaciones.print( )  
        print( "* Vencimientos" )
        self.vencimientos.print( )
        print( "* Calidades Crediticias" )
        self.calidadesCrediticias.print( )
        print( "* Entidades Emisoras" )
        self.entidadesEmisoras.print( )

# --------------------------------------- #
# -------- LISTA COMPOSICIONES ---------- #
# --------------------------------------- #

class ListaComposiciones:
    
    def __init__( self ): 
        self.listaComposiciones = {}
    
    # ------------ SETTERS ------------- #
     
    def anadirComposicion( self , pComposicion , pPorcentaje ):
        self.listaComposiciones[ pComposicion ] = pPorcentaje;
        
    # ------------ CALCULOS ------------- #
    
    def ponderarComposiciones( self , pAportacion , pComposiciones ):      
        for pComposicion in pComposiciones.listaComposiciones:
            porcentaje = pComposiciones.listaComposiciones[ pComposicion ] * pAportacion
            if pComposicion in self.listaComposiciones:
               self.listaComposiciones[ pComposicion ] += porcentaje
            else: self.listaComposiciones[ pComposicion ] = porcentaje;
      
    def calcularComposiciones( self ):
        total = 0
        for composicion in self.listaComposiciones:
            total += self.listaComposiciones[ composicion ]
        for composicion in self.listaComposiciones:
            valor = self.listaComposiciones[ composicion ] * 100 / total
            self.listaComposiciones[ composicion ] = valor
    
    # ------------ GRAFICOS ------------- #
        
    def graficoComposicion( self , pTitulo , pTipo , pUsuario ):
        informacion = ""; cabeceras = [];  datos = [];   colores = []; 
        informacion += html.subTitulo( "Reparto de " + pTipo + "es" )    
        for composicion in self.listaComposiciones:
            cabeceras.append( composicion )
            datos.append( self.listaComposiciones[ composicion ] )
            color = sql.getColorInversion( composicion , pTipo , pUsuario )
            colores.append( color )        
        informacion += html.graficoTarta( pTitulo + "_representacion" , str(cabeceras) , str(datos) , str(colores) , str(colores) )
        return informacion;

    # ------------ PRINT ------------- #
        
    def print( self ):
        for composicion in self.listaComposiciones:
            print( "   - " + composicion , self.listaComposiciones[ composicion ] )
            
# --------------------------------------- #
# ------------ LISTA RESUMEN ------------ #
# --------------------------------------- #

class ListaResumen:
    
    def __init__( self ):
        self.listaResumen = {}

    # ------------ SETTERS ------------- #
    def anadirAportacion( self , pResumen , pAportacion , pCotizacion ):        
        if pResumen in self.listaResumen:
            self.listaResumen[ pResumen ].anadirAportacion( pAportacion , pCotizacion )
        else:
            resumen = Resumen( pResumen )
            resumen.anadirAportacion( pAportacion , pCotizacion )
            self.listaResumen[ pResumen ] = resumen;
    
    def anadirComision( self , pResumen , pComision ):        
        if pResumen in self.listaResumen:
            self.listaResumen[ pResumen ].anadirComision( pComision )
        else:
            resumen = Resumen( pResumen )
            resumen.anadirComision( pComision )
            self.listaResumen[ pResumen ] = resumen;
      
    # ------------ CALCULOS ------------- #
    def calcularResumen( self ):
        for resumen in self.listaResumen:
            self.listaResumen[ resumen ].calcularResumen()
            self.listaResumen[ resumen ].calcularComposiciones()
                    
    def ponderarComposiciones( self , pResumen , pAportacion , pComposiciones ):        
        if pResumen in self.listaResumen:
            self.listaResumen[ pResumen ].ponderarComposiciones( pAportacion , pComposiciones )
        else:
            resumen = Resumen( pResumen )
            resumen.ponderarComposiciones( pAportacion , pComposiciones )
            self.listaResumen[ pResumen ] = resumen;   
            
    def calcularColores( self , pTipo , pUsuario ):         
        for resumen in self.listaResumen:
            color = sql.getColorInversion( resumen , pTipo , pUsuario );
            self.listaResumen[ resumen ].anadirColor( color )
              
    # ------------ GETTERS ------------- #
    def getCabeceras( self ):
        cabeceras = []
        for resumen in self.listaResumen:
            cabeceras.append( resumen )
        return cabeceras

    def getAtributo( self , pAtributo ):
        atributos = []
        for resumen in self.listaResumen:
            if pAtributo == "aportaciones": atributos.append( self.listaResumen[resumen].aportaciones )
            elif pAtributo == "titulos": atributos.append( self.listaResumen[resumen].titulos )
            elif pAtributo == "valorMedio": atributos.append( self.listaResumen[resumen].valorMedio )
            elif pAtributo == "beneficioBruto": atributos.append( self.listaResumen[resumen].beneficioBruto )
            elif pAtributo == "beneficioNeto": atributos.append( self.listaResumen[resumen].beneficioNeto )
            elif pAtributo == "comisiones": atributos.append( self.listaResumen[resumen].comisiones )
            elif pAtributo == "dividendos": atributos.append( self.listaResumen[resumen].dividendos )
            elif pAtributo == "rentabilidad": atributos.append( self.listaResumen[resumen].rentabilidad )
            elif pAtributo == "color": atributos.append( self.listaResumen[resumen].color )
            else: atributos.append( self.listaResumen[resumen].aportaciones )
                
        return atributos;

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
        self.isin = "";
        # resumen
        self.aportaciones = 0;
        self.titulos = 0;
        self.valorActual = 0;
        self.valorMedio = 0;
        self.beneficioBruto = 0;
        self.beneficioNeto = 0;
        self.comisiones = 0;
        self.dividendos = 0;
        self.rentabilidad = 0;
        self.color = ""
        # Composiciones
        self.composiciones = Composiciones();  
      
    # ------------ SETTERS ------------- #
    def anadirAportacion( self , pAportacion , pCotizacion ):
        titulos = pAportacion.titulos;
        if pAportacion.operacion == "venta": titulos = -titulos;        
        self.titulos += titulos;
        self.aportaciones += titulos * pAportacion.precio;
        self.valorActual  += titulos * pCotizacion;
        self.beneficioBruto += self.valorActual - self.aportaciones;
    
    def anadirComision( self , pComision ):
        if pComision.comision == 'comision': self.comisiones += pComision.precio;
        else: self.dividendos += pComision.precio;            
     
    def anadirColor( self , pcolor ):
        self.color = pcolor;
        
    # ------------ CALCULOS ------------- #
    def calcularResumen( self ):
        if self.titulos > 0: self.valorMedio = self.aportaciones/self.titulos;
        else: self.valorMedio = 0; 
        
        self.beneficioNeto = self.beneficioBruto - self.comisiones + self.dividendos;
        
        if self.aportaciones > 0:
           self.rentabilidad = 100 * self.beneficioNeto / self.aportaciones;
        else: self.rentabilidad = 0;
             
    def ponderarComposiciones( self , pAportacion , pComposiciones ):
        self.composiciones.ponderarComposiciones( pAportacion , pComposiciones )
   
    def calcularComposiciones( self ):
        self.composiciones.calcularComposiciones( );
    
    # ------------ GRAFICOS ------------- #      
    
    def graficoComposiciones( self , pTitulo , pUsuario ):
        return self.composiciones.graficoComposiciones( pTitulo , pUsuario )
        
    # ------------ PRINT ------------- #      
    def print( self ):
        print("################ " + self.descripcion + " ################");
        print( "Aportaciones: " , self.aportaciones );
        print( "Titulos: " , self.titulos );
        print( "Valor Actual: " , self.valorActual );
        print( "Valor Medio: " , self.valorMedio );
        print( "Beneficio Bruto: " , self.beneficioBruto );
        print( "Beneficio Neto: " , self.beneficioNeto );
        print( "Comisiones: " , self.comisiones );
        print( "Dividendos: " , self.dividendos );
        print( "Rentabilidad: " , self.rentabilidad );
        self.composiciones.print();
        
####################################################################    
#------------------------------- MAIN -----------------------------#
####################################################################

def main_1(): 
    usuario = 'davidcuesta'; 
    listaInversiones = ListaInversiones( usuario )
    listaInversiones.main();
    
    for inversion in listaInversiones.listaInversiones:      
        print( "################ " + inversion.descripcion + " ################" );
        print( "COMISIONES" );
        for aportacion in inversion.listaAportaciones:
            aportacion.print();
        
        print( "APORTACIOENS" );
        for comision in inversion.listaComisiones:
            comision.print();
        print( " " );
        
def main_2( ):
    usuario = 'davidcuesta';  
    listaInversiones = ListaInversiones( usuario )
    listaInversiones.main();
    
    print("--------------- ACTIVOS ----------------")
    listaInversiones.resumenActivos.print();
    print("--------------- ESTRATEGIAS ----------------")
    listaInversiones.resumenEstrategias.print();
    print("--------------- CATEGORIAS ----------------")
    listaInversiones.resumenCategorias.print();
    print("--------------- BROKERS ----------------")
    listaInversiones.resumenBrokers.print();
    print("--------------- RESUMEN ----------------")
    listaInversiones.resumen.print();
    
def main_3():
    usuario = 'davidcuesta';  
    listaInversiones = ListaInversiones( usuario )
    listaInversiones.main();
    
    for inversion in listaInversiones.listaInversiones:
        print( inversion.descripcion )
        inversion.composiciones.print()
    
#main_2( );

