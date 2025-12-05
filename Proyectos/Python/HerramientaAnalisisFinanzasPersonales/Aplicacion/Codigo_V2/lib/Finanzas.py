from datetime import datetime
from datetime import timedelta

from lib import Utils as utils
from lib import Scraper as scraper

from app import Sesion as sesion

MARGEN = 0.01

####################################################################    
#-------------------------- AGRUPACIONES --------------------------#
####################################################################

#------------------------- Transacciones --------------------------#

def transaccionesAgrupadasPorSubclasificacion( pFechaInicio , pFechaFin ): 
    transaccionesAgrupadas = {}
    transacciones = sesion.Sesion().getTransaccionesBy( pFechaInicio , pFechaFin , '' , '' , '' )
    for cuenta , subClasificacion , fecha , gasto , ingreso , faborita , descripcion in transacciones:
        gastoTotal = 0
        ingresoTotal = 0
        if subClasificacion in transaccionesAgrupadas: gastoTotal , ingresoTotal = transaccionesAgrupadas[ subClasificacion ]  
        gastoTotal += gasto
        ingresoTotal += ingreso
        transaccionesAgrupadas[ subClasificacion ] = ( gastoTotal , ingresoTotal )
    return transaccionesAgrupadas

#-------------------------- Aportaciones --------------------------#

def aportacionesAgrupadasPorActivo( pFechaInicio , pFechaFin , vCuenta ):
    aportacionesAgrupadas = {}
    aportaciones = sesion.Sesion().getAportacionesBy( pFechaInicio , pFechaFin , '' , '' , '' , 'ISIN ASC' )
    for isin , cuenta , fecha , precio , titulos , cambio , tipo , faborita , descripcion in aportaciones:
        if cuenta == vCuenta or vCuenta == '':
            titulosTotal = 0
            valorTotal = 0
            precioMedio = 0
            if isin in aportacionesAgrupadas: precioMedio , titulosTotal , valorTotal = aportacionesAgrupadas[ isin ]
            if tipo == 'Venta' or tipo == 'venta': titulos = -1*titulos
            titulosTotal += titulos
            valorTotal += titulos * precio * cambio
            if titulosTotal > MARGEN: precioMedio = valorTotal / titulosTotal
            else: titulosTotal = 0; precioMedio = 0;
            aportacionesAgrupadas[isin] = ( precioMedio , titulosTotal , valorTotal )
    return aportacionesAgrupadas

#--------------------------- Comisiones ---------------------------#

def comisionesAgrupadasPorActivo( pFechaInicio , pFechaFin , vCuenta ):
    comisionesAgrupadas = {}      
    comisiones = sesion.Sesion().getComisionesBy( pFechaInicio , pFechaFin , '' , '' , '' , '' )
    for isin , cuenta , fecha , gasto , ingreso , tipo , faborita , descripcion in comisiones:
        if cuenta == vCuenta or vCuenta == '':
            if isin == '*': isin = cuenta 
            gastoTotal = 0
            ingresoTotal = 0
            if isin in comisionesAgrupadas: gastoTotal , ingresoTotal = comisionesAgrupadas[ isin ]  
            gastoTotal += gasto
            ingresoTotal += ingreso
            comisionesAgrupadas[ isin ] = ( gastoTotal , ingresoTotal )
    return comisionesAgrupadas        

####################################################################    
#-------------------------- RENTABILIDAD --------------------------#
####################################################################

def actualizarCotizaciones():
    activos = sesion.Sesion().getActivos()
    for isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia in activos:
        cotizacion = scraper.cotizacionFecha_YahooFinance( link , datetime.now() )
        sesion.Sesion().actualizarCotizacionActivo( isin , cotizacion )
            
        
def rentabilidadAcumulada( pCuenta , pIsin , pFechaInicio , pFechaFin ):
    coste = 0
    valorFinal = 0
    activos = {}
    aportaciones = sesion.Sesion().getAportacionesBy( pFechaInicio , pFechaFin , pCuenta , pIsin , '' , '' )
    
    for isin , cuenta , fecha , precio , titulos , cambio , tipo , faborita , descripcion in aportaciones:        
        if tipo == 'Venta' or tipo == 'venta': titulos = -1*titulos
        coste += precio*titulos*cambio
        if isin not in activos: activos[ isin ] = titulos
        else: activos[ isin ] += titulos
        #print( "Coste " + isin + ": " + utils.floatStr( precio ) + " * " + utils.floatStr( titulos ) + " * " + utils.floatStr( cambio ) + " = " + utils.floatStr( precio*titulos ) )
    
    for activo in activos:
        isin , tipo_producto , tipo_emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia = sesion.Sesion().getActivo( activo )
        cambio = scraper.tipoCambio_YahooFinance( moneda , pFechaFin )
        pFechaFin = utils.ajustarSoloFecha( pFechaFin )
        if pFechaFin == datetime.now().date() and precio != None: cotizacion = precio
        else: cotizacion = scraper.cotizacionFecha_YahooFinance( link , pFechaFin )
                
        #print( "valorFinal " + isin + ": " + utils.floatStr( cotizacion ) + " * " + utils.floatStr( activos[activo] ) + " * " + utils.floatStr( cambio ) + " = " + utils.floatStr( cotizacion*activos[activo] ) )
        valorFinal += cotizacion*activos[activo]*cambio
        
    return valorFinal - coste

    
        
        
        
        