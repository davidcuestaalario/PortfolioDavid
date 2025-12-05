import numpy as np

from lib import HTML as html
from lib import Utils as utils
from lib import Ficheros as ficheros
from lib import Scraper as scr
from lib import Finanzas as finanzas
from lib import Scraper as scraper

from app import Sesion as sesion
from app import Seccion as secciones
from app import Filtro as filtro

####################################################################    
#----------------------------- Graficas ---------------------------#
####################################################################

class Grafica:
    
    def __init__( self , pFormulario , pSubFormulario , pTitulo ):
        self.formulario = pFormulario
        self.subFormulario = pSubFormulario
        self.titulo = pTitulo
        self.accion = 'Tabla'
        self.parametros = ''
        self.filtro = None
    
    
    def setAccion( self , pAccion ): self.accion = pAccion
    
    
    def generarFormulario( self ):
        mensaje = "La función generarFormulario() debe ser reescrita por sus clases herederas"
        secciones.Secciones().reportarError( mensaje )
        return "<p> " + mensaje + " </p>"
    
    
    def capturarCampos( self ):
        mensaje = "La función capturarCampos() debe ser reescrita por sus clases herederas"
        secciones.Secciones().reportarError( mensaje )
        return False
    

####################################################################    
#----------------------------- Balance ----------------------------#
####################################################################


class Balance(Grafica):
    
    def __init__( self ):   
        Grafica.__init__( self , 'Balance' , 'Balance' , 'Capital' )
        self.filtro = filtro.Filtro( 'Analisis' , 'Balance' )
        self.filtro.anadirCampo( 'FechaInicio' , 'Fecha Inicio' , 'date' , 'Filtrar por fechas superiores a la seleccionada'  )
        self.filtro.anadirCampo( 'FechaFin' , 'Fecha Fin' , 'date' , 'Filtrar por fechas inferiores a la seleccionada'  )
        
        
    def generarFormulario( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        vFechaInicio = self.filtro.campos[ 'FechaInicio' ].getValor() 
        vFechaFin = self.filtro.campos[ 'FechaFin' ].getValor()
        
        tituloFechaInicio = vFechaInicio
        if vFechaInicio == '': tituloFechaInicio = " Inicio  "
        tituloFechaFin = vFechaFin
        if vFechaFin == '': tituloFechaFin = " Dia actual "
        
        informacion = ''
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        informacion += "   <tr>"
        informacion += "       <td> Fecha de Inicio: </td>"
        informacion += "       <td> " + tituloFechaInicio + " </td>"
        informacion += "   </tr>"       
        informacion += "   <tr>"
        informacion += "       <td> Fecha de Fin: </td>"
        informacion += "       <td> " + tituloFechaFin + " </td>"
        informacion += "   </tr>"
        informacion += "</table>"
        
        informacion += "<br />"
        
        titulo = " Capital Total "
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br />"
        informacion += self.tablaBalancePatrimonial( vFechaInicio , vFechaFin )
        
        informacion += "<br />" + "<br />"
        
        titulo = " Resumen de Activos "
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br />"
        informacion += self.tablaBlanaceActivos( vFechaInicio , vFechaFin )
        
        return informacion

        
    def tablaBalancePatrimonial( self , vFechaInicio , vFechaFin ):
        informacion = ''
        informacion += "<br />"
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + html.refrescar( 'OrdenarCuenta' , 'Analisis' , 'etiqueta' , 'Ordenar' , 'Cuenta' , 'Cuenta' ) + "    </th>"
        informacion += "       <th> Ingresos </th>"
        informacion += "       <th> Gastos </th>"
        informacion += "       <th> Traspasos </th>"
        informacion += "       <th> Comisiones </th>"
        informacion += "       <th> Beneficios </th>"
        informacion += "       <th> Capital </th>"
        informacion += "   </tr>"
        
        transaccionGastoTotal = 0
        transaccionIngresoTotal = 0
        traspasoOrigenTotal = 0
        traspasoDestinoTotal = 0
        comisionGastoTotal = 0
        comisionIngresoTotal = 0
        rentabilidadTotal = 0
        totalTotal = 0
        
        cuentas = sesion.Sesion().getCuentasBy( '' , '' , '' , self.filtro.orden )
        for cuenta , color , descripcion , moneda , pais in cuentas:
            transaccionGasto , transaccionIngreso = sesion.Sesion().calcularTransacciones( cuenta , vFechaInicio , vFechaFin , '' )
            traspasoOrigen , traspasoDestino = sesion.Sesion().calcularTraspasos( cuenta , vFechaInicio , vFechaFin )
            comisionGasto , comisionIngreso = sesion.Sesion().calcularComisiones( cuenta , vFechaInicio , vFechaFin , '' )
            rentabilidad = finanzas.rentabilidadAcumulada( cuenta , '' , vFechaInicio , vFechaFin )
            total = transaccionIngreso - transaccionGasto + traspasoDestino - traspasoOrigen + comisionIngreso - comisionGasto + rentabilidad 

            informacion += "   <tr>"
            informacion += "       <th> " + cuenta + " </th>"
            informacion += "       <td> " + html.representarNumero( transaccionIngreso , True ) + " </td>"
            informacion += "       <td> " + html.representarNumero( - transaccionGasto , True ) + " </td>"
            informacion += "       <td> " + html.representarNumero( traspasoDestino - traspasoOrigen , True ) + " </td>"
            informacion += "       <td> " + html.representarNumero( comisionIngreso - comisionGasto , True ) + " </td>"
            informacion += "       <td> " + html.representarNumero( rentabilidad , True ) + " </td>"
            informacion += "       <td> " + html.representarNumero( total , True ) + " </td>"
            informacion += "   </tr>"
            
            transaccionGastoTotal += transaccionGasto 
            transaccionIngresoTotal += transaccionIngreso
            traspasoOrigenTotal += traspasoOrigen
            traspasoDestinoTotal += traspasoDestino
            comisionGastoTotal += comisionGasto
            comisionIngresoTotal += comisionIngreso
            rentabilidadTotal += rentabilidad
            totalTotal += total
            
        informacion += "   <tr>"
        informacion += "       <th> Capital </th>"
        informacion += "       <th> " + html.representarNumero( transaccionIngresoTotal , True ) + " </th>"
        informacion += "       <th> " + html.representarNumero( - transaccionGastoTotal , True ) + " </th>"
        informacion += "       <th> " + html.representarNumero( traspasoDestinoTotal - traspasoOrigenTotal , True ) + " </th>"
        informacion += "       <th> " + html.representarNumero( comisionIngresoTotal - comisionGastoTotal , True ) + " </th>"
        informacion += "       <th> " + html.representarNumero( rentabilidadTotal , True ) + " </th>"
        informacion += "       <th> " + html.representarNumero( totalTotal , True ) + " </th>"
        informacion += "   </tr>"
            
        informacion += "</table>"    
        return informacion        
       
        
    def tablaBlanaceActivos( self , vFechaInicio , vFechaFin ):
        aportacionesAgrupadas = finanzas.aportacionesAgrupadasPorActivo( vFechaInicio , vFechaFin , '' )
        comisionesAgrupadas = finanzas.comisionesAgrupadasPorActivo( vFechaInicio , vFechaFin , '' )
        periodoInversion = ( utils.daysBetween( vFechaInicio , vFechaFin ) / 365 )
        
        informacion = ''
        informacion += "<br />"
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> ISIN </th>"
        informacion += "       <th> Descripción </th>"
        informacion += "       <th> Títulos </th>"
        informacion += "       <th> Precio Medio </th>"
        informacion += "       <th> Precio Actual </th>"        
        informacion += "       <th> Valor Aportado </th>"
        informacion += "       <th> Valor Actual </th>"
        informacion += "       <th> Comisiones </th>"        
        informacion += "       <th> Beneficio </th>"
        informacion += "       <th> Rentabilidad Total </th>"
        informacion += "       <th> Rentabilidad Anual </th>"
        informacion += "   </tr>"
        
        totalValorTotal = 0
        totalValorActual = 0
        totalComisionIngreso = 0 
        totalComisionGasto = 0
        
        comisionIngresoCerradas = 0
        comisionGastoCerradas = 0
        beneficioCerradas = 0
               
        activos = sesion.Sesion().getActivosBy( '' , '' , '' , 'estrategia ASC' )
        for isin , tipo , emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia in activos:            
            comisionGasto = 0
            comisionIngreso = 0
            if isin in comisionesAgrupadas: comisionGasto , comisionIngreso = comisionesAgrupadas[ isin ]
            
            if isin in aportacionesAgrupadas:                
                precioMedio , titulosTotal , valorTotal = aportacionesAgrupadas[ isin ]
                
                cambioActual = scraper.tipoCambio_YahooFinance( moneda , vFechaFin )
                cotizacion = scraper.cotizacionFecha_YahooFinance( link , vFechaFin )
                valorActual = titulosTotal * cotizacion * cambioActual
                
                rentabilidadAnual = 0
                rentabilidadTotal = 0
                beneficio = valorActual - valorTotal + comisionIngreso - comisionGasto
                if beneficio != 0: rentabilidadTotal = ( beneficio / valorTotal ) * 100
                try: rentabilidadAnual = rentabilidadTotal / periodoInversion
                except: print( "Revisar rentabilidad anual" )
                
                totalValorTotal += valorTotal
                totalValorActual += valorActual
                totalComisionIngreso += comisionIngreso 
                totalComisionGasto += comisionGasto
                
                if titulosTotal == 0:
                    comisionIngresoCerradas += comisionIngreso
                    comisionGastoCerradas += comisionGasto
                    beneficioCerradas += beneficio
                    
                else:              
                    informacion += "   <tr>"
                    informacion += "       <th> " + isin + " </th>"
                    informacion += "       <td> <a rel='" + descripcion + "' href='https://es.finance.yahoo.com/quote/" + link + "?p=" + link + "' target='blank'> " + descripcion + " </a> </td>"
                    informacion += "       <td> " + html.representarNumero( titulosTotal , False ) + " </td>"
                    informacion += "       <td> " + html.representarNumero( precioMedio , False ) + " </td>"
                    informacion += "       <td> " + html.representarNumero( cotizacion * cambioActual , False ) + " </td>"
                    informacion += "       <td> " + html.representarNumero( valorTotal , False ) + " </td>"
                    informacion += "       <td> " + html.representarNumero( valorActual , False ) + " </td>"
                    informacion += "       <td> " + html.representarNumero( comisionIngreso - comisionGasto , True ) + " </td>"        
                    informacion += "       <td> " + html.representarNumero( beneficio , True ) + " </td>"
                    informacion += "       <td> " + html.representarNumero( rentabilidadTotal , True ) + " </td>"
                    informacion += "       <td> " + html.representarNumero( rentabilidadAnual , True ) + " </td>"
                    informacion += "   </tr>"
        
        informacion += "   <tr>"
        informacion += "       <th>  </th>"
        informacion += "       <td> Operaciones Cerradas </td>"
        informacion += "       <td>  </td>"
        informacion += "       <td>  </td>"
        informacion += "       <td>  </td>"
        informacion += "       <td>  </td>"
        informacion += "       <td>  </td>"
        informacion += "       <td> " + html.representarNumero( comisionIngresoCerradas - comisionGastoCerradas , True ) + " </td>"        
        informacion += "       <td> " + html.representarNumero( beneficioCerradas , True ) + " </td>"
        informacion += "       <td>  </td>"
        informacion += "       <td>  </td>"
        informacion += "   </tr>"        
        
        totalRentabilidadTotal = 0
        totalRentabilidadAnual = 0
        totalBeneficio = totalValorActual - totalValorTotal + totalComisionIngreso - totalComisionGasto
        if totalBeneficio != 0: totalRentabilidadTotal = ( totalBeneficio / totalValorTotal ) * 100
        try: totalRentabilidadAnual = totalRentabilidadTotal / periodoInversion
        except: print( "Revisar rentabilidad total anual" )
        
        informacion += "   <tr>"
        informacion += "       <th> Total </th>"
        informacion += "       <th>  </th>"
        informacion += "       <th>  </th>"
        informacion += "       <th>  </th>"
        informacion += "       <th>  </th>"
        informacion += "       <th> " + html.representarNumero( totalValorTotal , False ) + " </th>"
        informacion += "       <th> " + html.representarNumero( totalValorActual , False ) + " </th>"
        informacion += "       <th> " + html.representarNumero( totalComisionIngreso - totalComisionGasto , True ) + " </th>"        
        informacion += "       <th> " + html.representarNumero( totalBeneficio , True ) + " </th>"
        informacion += "       <th> " + html.representarNumero( totalRentabilidadTotal , True ) + " </th>"
        informacion += "       <th> " + html.representarNumero( totalRentabilidadAnual , True ) + " </th>"
        informacion += "   </tr>"
        
        informacion += "</table>"    
        return informacion
    
####################################################################    
#------------------------------ Gastos ----------------------------#
####################################################################


class Gastos(Grafica):
    
    def __init__( self ):   
        Grafica.__init__( self , 'Patrimonio' , 'Gastos' , 'Analisis de Gastos e Ingresos' )
        self.filtro = filtro.Filtro( 'Analisis' , 'Gastos' )
        self.filtro.anadirCampo( 'FechaInicio' , 'Fecha Inicio' , 'date' , 'Filtrar por fechas superiores a la seleccionada'  )
        self.filtro.anadirCampo( 'FechaFin' , 'Fecha Fin' , 'date' , 'Filtrar por fechas inferiores a la seleccionada'  )
        
        opciones = []
        opciones.append( ( '' , ' --------- ' , True ) )
        opciones.append( ( 'Gastos' , 'Analisis de Gastos' , False ) ) 
        opciones.append( ( 'Ingresos' , 'Analisis de Ingresos' , False ) )
        opciones.append( ( 'Comparacion' , 'Comparaciones entre los Gastos e Ingresos' , False ) )
        opciones.append( ( 'Detalles' , 'Desglose de Gastos e Ingresos' , False ) )
        self.filtro.anadirCampo( 'FiltroGrafico' , 'Filtro de Grafico' , opciones , 'Permite quitar algunos de los gráficos para mayor comodidad' )


    def generarFormulario( self ):
        self.filtro.ordenar(  secciones.Secciones().getParametros( 'Ordenar' ) )
        vFechaInicio = self.filtro.campos[ 'FechaInicio' ].getValor() 
        vFechaFin = self.filtro.campos[ 'FechaFin' ].getValor()
        vFiltroGrafico = self.filtro.campos[ 'FiltroGrafico' ].getValor()

        tituloFechaInicio = vFechaInicio
        if vFechaInicio == '': tituloFechaInicio = " Inicio  "
        tituloFechaFin = vFechaFin
        if vFechaFin == '': tituloFechaFin = " dia actual "
        
        informacion = ''
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        informacion += "   <tr>"
        informacion += "       <td> Fecha de Inicio: </td>"
        informacion += "       <td> " + tituloFechaInicio + " </td>"
        informacion += "   </tr>"       
        informacion += "   <tr>"
        informacion += "       <td> Fecha de Fin: </td>"
        informacion += "       <td> " + tituloFechaFin + " </td>"
        informacion += "   </tr>"
        informacion += "</table>"
        
        informacion += "<br />"
        
        titulo = " Distribución de Gastos e Ingresos "
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br />"
        informacion += self.graficaDistribucionGastosIngresos( vFechaInicio , vFechaFin , vFiltroGrafico )
        
        if vFiltroGrafico == 'Detalles' or vFiltroGrafico == '':
            informacion += "<br />" + "<br />"
            titulo = " Desglose de Gastos e Ingresos "
            informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
            informacion += "<br />"
            informacion += self.tablaResumenGastos( vFechaInicio , vFechaFin )

        return informacion


    def graficaDistribucionGastosIngresos( self , vFechaInicio , vFechaFin , vFiltroGrafico ):
        transaccionesAgrupadas = finanzas.transaccionesAgrupadasPorSubclasificacion( vFechaInicio , vFechaFin )
        
        etiquetas = []
        colores = []
        valoresGastos = []
        valoresIngresos = []
        
        colorPositivo = '#00ff6b'
        colorNegativo = '#f00e1c'
        
        cabecerasGastos = []

        cuerpoComparaciones = []
        cuerpoGastos = []
        cuerpoIngresos = []
        i = 0
        
        clasificaciones = sesion.Sesion().getClasificacionesBy( '' , 'CLASIFICACION ASC' )
        for clasificacion , color , descripcion in clasificaciones:
            gastoTotal = 0
            ingresoTotal = 0
            subClasificaciones = sesion.Sesion().getSubClasificacionesBy( clasificacion , '' , 'SUBCLASIFICACION ASC' )
            for subClasificacion , clasificacion in  subClasificaciones:
                if subClasificacion in transaccionesAgrupadas: 
                    gasto , ingreso = transaccionesAgrupadas[ subClasificacion ]
                    gastoTotal += gasto
                    ingresoTotal += ingreso
        
            etiquetas.append( clasificacion )
            colores.append( utils.colorRGBToHexadecimal( color ) )
            valoresGastos.append( gastoTotal )
            valoresIngresos.append( ingresoTotal )
            
            vectorGastos = np.zeros( len( clasificaciones ) )
            vectorGastos[i] = gastoTotal
            
            vectorIngresos = np.zeros( len( clasificaciones ) )
            vectorIngresos[i] = ingresoTotal
            i=i+1
            
            cabecerasGastos.append( clasificacion )
            cuerpoGastos.append( [ clasificacion , color , vectorGastos.tolist() ] )
            cuerpoIngresos.append( [ clasificacion , color , vectorIngresos.tolist() ] )
        
        cuerpoComparaciones.append( ['Gastos' , utils.colorHexadecimalToRGB( colorNegativo ) , valoresGastos] )
        cuerpoComparaciones.append( ['Ingresos' , utils.colorHexadecimalToRGB( colorPositivo ) , valoresIngresos] )
        
        informacion = ''
        if vFiltroGrafico == 'Gastos' or vFiltroGrafico == '':
            titulo = " Distribución de Gastos "
            informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 3 , titulo )
            informacion += "<br />"
            informacion += html.graficoSimple( 'GraficaGastos' , etiquetas , valoresGastos , colores , colores , 'pie' , False )
            informacion += "<br />" + "<br />"
            titulo = " Comparación de Gastos "
            informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 3 , titulo )
            informacion += "<br />"
            #informacion += html.graficoSimple( 'ComparacionGastos' , etiquetas , valoresGastos , colores , colores , 'bar' )
            informacion += html.graficoBarrasAgrupado( 'ComparacionGastos' , cabecerasGastos , cuerpoGastos , False , True )
            informacion += "<br />" + "<br />"
        
        if vFiltroGrafico == 'Ingresos' or vFiltroGrafico == '':
            titulo = " Distribución de Ingresos "
            informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 3 , titulo )
            informacion += "<br />"
            informacion += html.graficoSimple( 'GraficaIngresos' , etiquetas , valoresIngresos , colores , colores , 'pie' , False )
            informacion += "<br />" + "<br />"   
            titulo = " Comparación de Ingresos "
            informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 3 , titulo )
            informacion += "<br />"
            #informacion += html.graficoSimple( 'ComparacionIngresos' , etiquetas , valoresIngresos , colores , colores , 'bar' )
            informacion += html.graficoBarrasAgrupado( 'ComparacionIngresos' , cabecerasGastos , cuerpoIngresos , False , True )
            informacion += "<br />" + "<br />"
       
        if vFiltroGrafico == 'Comparacion' or vFiltroGrafico == '':
            titulo = " Comparación de Gastos con Ingresos "
            informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 3 , titulo )
            informacion += "<br />"
            informacion += html.graficoBarrasAgrupado( 'ComparacionGastosIngresos' , cabecerasGastos , cuerpoComparaciones , False , False )

        return informacion


    def tablaResumenGastos( self , vFechaInicio , vFechaFin ):
        transaccionesAgrupadas = finanzas.transaccionesAgrupadasPorSubclasificacion( vFechaInicio , vFechaFin )
        informacion = ''
        clasificaciones = sesion.Sesion().getClasificacionesBy( '' , 'CLASIFICACION ASC' )
        for clasificacion , color , descripcion in clasificaciones:       
            
            informacion += html.tituloTabla( clasificacion )
            informacion += "<table>"
            informacion += "   <tr>"
            informacion += "       <th> SubClasificación </th>"
            informacion += "       <th> Gasto </th>"
            informacion += "       <th> Ingreso </th>"
            informacion += "   <tr>"
            
            gastoTotal = 0
            ingresoTotal = 0
            
            subClasificaciones = sesion.Sesion().getSubClasificacionesBy( clasificacion , '' , 'SUBCLASIFICACION ASC' )
            for subClasificacion , clasificacion in  subClasificaciones:
                gasto = 0
                ingreso = 0
                if subClasificacion in transaccionesAgrupadas: 
                    gasto , ingreso = transaccionesAgrupadas[ subClasificacion ]
                    gastoTotal += gasto
                    ingresoTotal += ingreso
                
                informacion += "   <tr>"
                informacion += "       <td> " + subClasificacion + " </td>"
                informacion += "       <td> " + html.representarNumero( gasto , False ) + " </td>"
                informacion += "       <td> " + html.representarNumero( ingreso , False ) + " </td>"            
                informacion += "   <tr>"

            informacion += "   <tr>"
            informacion += "       <th> Total </th>"
            informacion += "       <th> " + html.representarNumero( -gastoTotal , True ) + " </th>"
            informacion += "       <th> " + html.representarNumero( ingresoTotal , True ) + " </th>"
            informacion += "   <tr>"
            informacion += "</table>"
            informacion += "<br />" + "<br />"           
            
        return informacion

####################################################################    
#---------------------------- Patrimonio --------------------------#
####################################################################


class Patrimonio(Grafica):
    
    def __init__( self ):   
        Grafica.__init__( self , 'Patrimonio' , 'Patrimonio' , 'Analisis Patrimonial' )
        self.filtro = filtro.Filtro( 'Analisis' , 'Patrimonio' )
        self.filtro.anadirCampo( 'FechaInicio' , 'Fecha Inicio' , 'date' , 'Filtrar por fechas superiores a la seleccionada' )
        self.filtro.anadirCampo( 'FechaFin' , 'Fecha Fin' , 'date' , 'Filtrar por fechas inferiores a la seleccionada' )
        

    def inicializarFiltro( self ):
        opciones = []
        opciones.append( ( '' , ' --------- ' , True ) )
        cuentas = sesion.Sesion().getCuentasBy( '' ,  '' ,  '' , 'cuenta ASC' )
        for cuenta , color , descripcion , moneda , pais in cuentas: 
            if descripcion == None: descripcion = ''
            opciones.append( ( cuenta , cuenta + " - " + descripcion , False ) ) 
        self.filtro.anadirCampo( 'Cuenta' , 'Cuenta' , opciones , 'Seleccionar únicamente los activos de una cuenta' )
        
        opciones = []
        opciones.append( ( '' , ' --------- ' , True ) )
        estrategias = sesion.Sesion().getEstrategiasBy( '' , 'Estrategia ASC' )
        for estrategia , color , descripcion in estrategias: 
            if descripcion == None: descripcion = ''
            opciones.append( ( estrategia , estrategia + " - " + descripcion , False ) )
        self.filtro.anadirCampo( 'Estrategia' , 'Estrategia' , opciones , 'Seleccionar únicamente los activos que siguen una estrategia' )
 
           
    def generarFormulario( self ):
        self.inicializarFiltro()
        self.filtro.ordenar( secciones.Secciones().getParametros( 'Ordenar' ) )       
        vFechaInicio = self.filtro.campos[ 'FechaInicio' ].getValor() 
        vFechaFin = self.filtro.campos[ 'FechaFin' ].getValor()
        
        vCuenta = self.filtro.campos[ 'Cuenta' ].getValor() 
        vEstrategia = self.filtro.campos[ 'Estrategia' ].getValor()
        
        tituloFechaInicio = vFechaInicio
        if vFechaInicio == '': tituloFechaInicio = " Inicio  "
        tituloFechaFin = vFechaFin
        if vFechaFin == '': tituloFechaFin = " Dia actual "
        tituloCuenta = vCuenta
        if vCuenta == '': tituloCuenta = " Todas " 
        tituloEstrategia = vEstrategia
        if vEstrategia == '': tituloEstrategia = " Todas " 
        
        informacion = ''
        informacion += "<table>"
        informacion += "   <tr>"
        informacion += "       <th> " + self.filtro.formularioEditarFiltros() + " </th>"
        informacion += "   </tr>"
        informacion += "   <tr>"
        informacion += "       <td> Fecha de Inicio: </td>"
        informacion += "       <td> " + tituloFechaInicio + " </td>"
        informacion += "   </tr>"       
        informacion += "   <tr>"
        informacion += "       <td> Fecha de Fin: </td>"
        informacion += "       <td> " + tituloFechaFin + " </td>"
        informacion += "   </tr>"
        informacion += "   <tr>"
        informacion += "       <td> Cuenta: </td>"
        informacion += "       <td> " + tituloCuenta + " </td>"
        informacion += "   </tr>"
        informacion += "   <tr>"
        informacion += "       <td> Estrategia: </td>"
        informacion += "       <td> " + tituloEstrategia + " </td>"
        informacion += "   </tr>"
        informacion += "</table>"
        
        informacion += "<br />"
      
        titulo = " Distribución de estrategias "
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br />"
        informacion += self.graficaDistribucionEstrategias( vFechaInicio , vFechaFin )
        
        #titulo = " Distribución de cuentas "
        #informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        #informacion += self.graficaDistribucionCuentas( vFechaInicio , vFechaFin )
        
        titulo = " Distribución de activos "
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br />"
        informacion += self.graficaDistribucionActivos( vFechaInicio , vFechaFin )        
        
        titulo = " Distribución de Allocations "
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        informacion += "<br />"
        allocations = sesion.Sesion().getAllocationsBy( '' , 'Allocation ASC' )
        for allocation , descripcion in allocations:
            if descripcion != None: informacion += html.parrafo( 'Descripcion_' + allocation , 'descripcion' , descripcion )
            informacion += self.graficaDistribucionAllocations( vFechaInicio , vFechaFin , vCuenta , vEstrategia , allocation )
        
        #titulo = " Desglose de Activos "
        #informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 2 , titulo )
        #informacion += "<br />"
        #informacion += self.tablaResumenActivos( vFechaInicio , vFechaFin )
        
        return informacion


    def graficaDistribucionEstrategias( self , vFechaInicio , vFechaFin ):
        aportacionesAgrupadas = finanzas.aportacionesAgrupadasPorActivo( vFechaInicio , vFechaFin , '' )
        
        informacion = ''
        datosGrafica = {}
        
        activos = sesion.Sesion().getActivosBy( '' , '' , '' , 'estrategia ASC' )
        for isin , tipo , emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia in activos:            
            if isin in aportacionesAgrupadas:                
                precioMedio , titulosTotal , valorTotal = aportacionesAgrupadas[ isin ]

                cambioActual = scraper.tipoCambio_YahooFinance( moneda , vFechaFin )
                cotizacion = scraper.cotizacionFecha_YahooFinance( link , vFechaFin )
                valorActual = titulosTotal * cotizacion * cambioActual
                
                valor = 0 
                estrategia , color , descripcion = sesion.Sesion().getEstrategia( estrategia )
                if estrategia in datosGrafica: valor , color = datosGrafica[estrategia]
                valor += valorActual
                datosGrafica[estrategia] = ( valor , color )

        etiquetas = []
        valores = []
        colores = []
        
        for estrategia in datosGrafica:
            valor , color = datosGrafica[estrategia]
            etiquetas.append( estrategia )
            valores.append( valor )
            colores.append( utils.colorRGBToHexadecimal( color ) )
        
        informacion += html.graficoSimple( 'DistribucionEstrategias' , etiquetas , valores , colores , colores , 'pie' , False )
        informacion += "<br />" + "<br />"
        return informacion


    def graficaDistribucionCuentas( self , vFechaInicio , vFechaFin ):
        informacion = ''
        return informacion


    def graficaDistribucionActivos( self , vFechaInicio , vFechaFin ):
        aportacionesAgrupadas = finanzas.aportacionesAgrupadasPorActivo( vFechaInicio , vFechaFin , '' )
        
        informacion = ''
        datosGrafica = {}
        
        activos = sesion.Sesion().getActivosBy( '' , '' , '' , 'estrategia ASC' )
        for isin , tipo , emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia in activos:            
            if isin in aportacionesAgrupadas:                
                precioMedio , titulosTotal , valorTotal = aportacionesAgrupadas[ isin ]

                cambioActual = scraper.tipoCambio_YahooFinance( moneda , vFechaFin )
                cotizacion = scraper.cotizacionFecha_YahooFinance( link , vFechaFin )
                valorActual = titulosTotal * cotizacion * cambioActual
                
                valor = 0
                if isin in datosGrafica: descripcion , valor , color = datosGrafica[isin]
                valor += valorActual 
                datosGrafica[isin] = ( descripcion , valor , color )

        etiquetas = []
        valores = []
        colores = []
        
        for isin in datosGrafica:
            descripcion , valor , color = datosGrafica[isin]
            etiquetas.append( descripcion )
            valores.append( valor )
            colores.append( utils.colorRGBToHexadecimal( color ) )               
        
        informacion += html.graficoSimple( 'DistribucionCuentas' , etiquetas , valores , colores , colores , 'pie' , False )
        informacion += "<br />" + "<br />"
        return informacion


    def graficaDistribucionAllocations( self , vFechaInicio , vFechaFin , vCuenta , vEstrategia , vAllocation ):
        aportacionesAgrupadas = finanzas.aportacionesAgrupadasPorActivo( vFechaInicio , vFechaFin , vCuenta )
 
        informacion = ''
        datosGrafica = {}
        
        activos = sesion.Sesion().getActivosBy( '' , '' , vEstrategia , 'estrategia ASC' )
        for isin , tipo , emisor , fuente , link , moneda , descripcion , color , precio , producto , estrategia in activos:            
            if isin in aportacionesAgrupadas:                
                precioMedio , titulosTotal , valorTotal = aportacionesAgrupadas[ isin ]

                cambioActual = scraper.tipoCambio_YahooFinance( moneda , vFechaFin )
                cotizacion = scraper.cotizacionFecha_YahooFinance( link , vFechaFin )
                valorActual = titulosTotal * cotizacion * cambioActual
                
                subAllocations = sesion.Sesion().getSubAllocationsOf( vAllocation , isin , 'suballocation ASC' )
                for isin , subAllocation , porcentaje in subAllocations:
                    valor = 0
                    subAllocation , color , allocation = sesion.Sesion().getSubAllocation( subAllocation )
                    if subAllocation in datosGrafica: valor , color = datosGrafica[subAllocation]
                    valor += (valorActual * porcentaje)/100
                    datosGrafica[subAllocation] = ( valor , color )
                    
        etiquetas = []
        valores = []
        colores = []
        
        for subAllocation in datosGrafica:
            valor , color = datosGrafica[subAllocation]
            etiquetas.append( subAllocation )
            valores.append( valor )
            colores.append( utils.colorRGBToHexadecimal( color ) )
        
        titulo = " Distribución de " + vAllocation
        informacion += html.titulo( self.formulario + self.subFormulario , "contenido" , 3 , titulo )
        informacion += "<br />"
        informacion += html.graficoSimple( 'DistribuciónAllocation_' + vAllocation , etiquetas , valores , colores , colores , 'pie' , False )
        informacion += "<br />" + "<br />"                   
        return informacion


    def tablaResumenActivos( self , vFechaInicio , vFechaFin ):
        #aportacionesAgrupadas = finanzas.aportacionesAgrupadasPorActivo( vFechaInicio , vFechaFin )
        
        informacion = ''
        informacion += "<br />"
        informacion += "<table>"
        informacion += "   <tr>"
        
        
        informacion += "   </tr>"
            
        informacion += "</table>"    
        return informacion
      
####################################################################    
#---------------------------- Evolucion ---------------------------#
####################################################################


class Evolucion(Grafica):
    
    def __init__( self ):   
        Grafica.__init__( self , 'Evolucion' , 'Evolucion' , 'Evolución Temporal de los Activos' )
        self.filtro = filtro.Filtro( 'Analisis' , 'Evolucion' )
        self.filtro.anadirCampo( 'FechaInicio' , 'Fecha Inicio' , 'date' , 'Filtrar por fechas superiores a la seleccionada'  )
        self.filtro.anadirCampo( 'FechaFin' , 'Fecha Fin' , 'date' , 'Filtrar por fechas inferiores a la seleccionada'  )
        
        opciones = []
        opciones.append( ( 'Gastos' , 'Gastos' , True ) ) 
        opciones.append( ( 'Patrimonio' , 'Patrimonio' , False ) ) 
        self.filtro.anadirCampo( 'Tipo' , 'Tipo de Grafico' , opciones , 'Permite seleccionar el tipo de grafico que va a mostrar' )
    
    #def generarFormulario( self ):
        

####################################################################    
#------------------------------ Flujo -----------------------------#
####################################################################


class Flujo(Grafica):
    
    def __init__( self ):   
        Grafica.__init__( self , 'Evolucion' , 'Flujo' , 'Evolución Temporal de los Gastos e Ingresos' )
        self.filtro = filtro.Filtro( 'Analisis' , 'Flujo' )
        
        
        