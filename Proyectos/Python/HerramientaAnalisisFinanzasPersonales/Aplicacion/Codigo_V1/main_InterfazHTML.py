# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

import Z_html as html
import Z_SQLReader as sql
import Z_Utils as utilidades

import Inversiones
import Finanzas

####################################################################    
#----------------------------- CALCULOS ---------------------------#
####################################################################

fuente = 'bd'; # 'csv'
rutaEscritorio = 'C:/Users/Devilvil/Desktop/Scraper/BaseDatos';
rutaDrobox = 'C:/Users/david/Dropbox (Personal)/Finanzas/Scraper/BaseDatos';
ruta = rutaDrobox;

activos_csv = '/Inversiones_Activos.csv';
comisiones_csv = '/Inversiones_Comisiones.csv';
posiciones_csv = '/Inversiones_Posiciones.csv';
finanzas_csv = '/FinanzasPersonales.csv';
composiciones_csv = '/Inversiones_Composicion.csv';

registrado = False;
usuario = "";
permisos = "";
mensaje = "";

listaInversiones = Inversiones.ListaInversiones( usuario )
listaOperaciones = Finanzas.ListaOperaciones( usuario )

variablesGobales = {}

####################################################################    
#----------------------- INICIAR SERVIDOR WEB ---------------------#
####################################################################

aplicacion = Flask(__name__)

####################################################################    
#------------------------- PAGINA PRINCIPAL -----------------------#
####################################################################    

@aplicacion.route('/')
def home():
    informacion = render_template('0_index.php')
    if registrado: informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    else:          informacion += render_template('Nav_1_registro.php')
    
    informacion += render_template('Page_Principal.php')
    
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/principal')
def principal():
    informacion = render_template('0_index.php')
    if registrado: informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    else:          informacion += render_template('Nav_1_registro.php')
    
    informacion += render_template('Page_Principal.php')
    
    informacion += render_template('0_footer.php')
    return informacion

####################################################################    
#------------------------ PAGINAS DE SESION -----------------------#
#################################################################### 

# ---------------------------------------- #
# ------------ Iniciar Sesion ------------ #
# ---------------------------------------- #

@aplicacion.route('/login' , methods=["GET", "POST"] )
def login():
    global registrado; global permisos; global usuario; global mensaje;
    global listaInversiones;
    global listaOperaciones;
    if registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_registro.php')
    informacion += html.mensaje( mensaje ); mensaje = "";
    informacion += "<section id='contenido'>"
    
    informacion += "<br />"
    informacion += html.titulo( "Iniciar Sesion" )
    
    informacion += "<form id='resumenAno' name='resumenAno' action='' method='post'>"
    informacion += "<br />"
    informacion += "<fieldset>"
    informacion += "    <label for='usuario'> Usuario: </label>"
    informacion += "    <input type='text' id='usuario' class='login' name='usuario_txt' placeholder='Nombre de usuario' title='Escriba su nombre de usuario' />"
    informacion += "<br /> <br />"
    informacion += "    <label for='contrasena'> Contraseña: </label>"			
    informacion += "    <input type='password' id='contrasena' class='login' name='contrasena_txt' placeholder='********' title='Escriba su contraseña' />"
    informacion += "<br /> <br />"
    informacion += "<input type='submit' id='aceptar' name='logIn_btn' value='Iniciar Sesion'/>"
    informacion += "</fieldset>" + "</form>"
    
    if request.method == 'POST': 
        usuario = request.form['usuario_txt'];
        contrasena = request.form['contrasena_txt'];
        
        if sql.existeUsuario( usuario ):
            mensaje = usuario + " no esta registrado"
            print(mensaje)
            return redirect( "/login" )
        elif sql.existeAdmision( usuario ):
            mensaje = "Ese usuario esta pendiente de admision"
            print(mensaje)
            return redirect( "/login" )
        elif not sql.contrasenaCorrecta( usuario , contrasena ):
            mensaje = "La constraseña no es correcta"
            print(mensaje)
            return redirect( "/login" )
        else:
            registrado = True;
            permisos = sql.getPermiso( usuario );
        
        print( "usuario" , usuario )
        listaInversiones.setUsuario( usuario )
        listaInversiones.main(); 
        
        listaOperaciones.setUsuario( usuario )
        listaOperaciones.main(); 
        
        return redirect( '/principal' )
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion

# ---------------------------------------- #
# ------------- Cerrar Sesion ------------ #
# ---------------------------------------- #

@aplicacion.route('/logout' )
def logout():
    global registrado; registrado = False;
    global permisos; permisos = '';
    global usuario; 
    global mensaje; mensaje = "Sesion de " + usuario + " Cerrada";
    usuario = "";
    global variablesGobales; variablesGobales = {}
    
    listaInversiones.clear();
    listaOperaciones.clear(); 
    return redirect( '/principal' )

# ---------------------------------------- #
# ---------------- Registro -------------- #
# ---------------------------------------- #

@aplicacion.route('/registro' , methods=["GET", "POST"] )
def registro( ):
    global mensaje; global variablesGobales; global usuario;
    if registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_registro.php')
    informacion += html.mensaje( mensaje ); mensaje = "";
    informacion += "<section id='contenido'>"
    
    informacion += "<br />"
    informacion += html.titulo( "Registro" )
    informacion += "<br />"
    
    if "registro_nombre" not in variablesGobales: variablesGobales["registro_nombre"] = ""
    if "registro_apellido1" not in variablesGobales: variablesGobales["registro_apellido1"] = ""
    if "registro_apellido2" not in variablesGobales: variablesGobales["registro_apellido2"] = ""
    if "registro_DNI" not in variablesGobales: variablesGobales["registro_DNI"] = ""
    if "registro_telefono" not in variablesGobales: variablesGobales["registro_telefono"] = ""
    if "registro_email" not in variablesGobales: variablesGobales["registro_email"] = ""
    if "registro_contra" not in variablesGobales: variablesGobales["registro_contra"] = ""
    if "registro_contraRPT" not in variablesGobales: variablesGobales["registro_contraRPT"] = ""
     
    if request.method == 'POST': 
        variablesGobales["registro_nombre"] = request.form['nombre_txt'];
        variablesGobales["registro_apellido1"] = request.form['apellido1_txt'];
        variablesGobales["registro_apellido2"] = request.form['apellido2_txt'];
        usuario = request.form['usuario_txt'];
        variablesGobales["registro_DNI"] = request.form['dni_txt'];
        variablesGobales["registro_telefono"] = request.form['telefono_tel'];
        variablesGobales["registro_email"] = request.form['email_email'];
        variablesGobales["registro_contra"] = request.form['password_txt'];
        variablesGobales["registro_contraRPT"] = request.form['passwordRP_txt'];
        
        if not sql.existeUsuario( usuario ):
            mensaje = "Ese usuario ya esta registrado"
            return redirect( "/registro" )
        elif sql.existeAdmision( usuario ):
            mensaje = "Ese usuario esta pendiente de admision"
            return redirect( "/registro" )
        elif variablesGobales["registro_contra"] != variablesGobales["registro_contraRPT"]:
            mensaje = "Las constraseñas no coinciden"
            return redirect( "/registro" )
        else: 
            sql.anadirAdmision( variablesGobales["registro_nombre"] , variablesGobales["registro_apellido1"] , variablesGobales["registro_apellido2"] , usuario , variablesGobales["registro_DNI"] , variablesGobales["registro_telefono"] , variablesGobales["registro_email"] , variablesGobales["registro_contra"] )
            mensaje = "El usuario " + usuario + " ha sido añadido correctamente a la lista de admisiones"
            print(mensaje)
            return redirect( "/login" )
    
    informacion += html.formularioRegistro( "registro" , variablesGobales["registro_nombre"] , variablesGobales["registro_apellido1"] , variablesGobales["registro_apellido2"] , usuario , variablesGobales["registro_DNI"] , variablesGobales["registro_telefono"] , variablesGobales["registro_email"] , variablesGobales["registro_contra"] , variablesGobales["registro_contraRPT"] )
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion

# ---------------------------------------- #
# ---------------- Admision -------------- #
# ---------------------------------------- #

@aplicacion.route('/admision' , methods=["GET", "POST"] )
def admision():
    global mensaje; global registrado; global usuario;
    if not registrado: return redirect( '/principal' )
    if permisos != 'admin': return redirect( '/principal' )
    
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )    
    informacion += html.mensaje( mensaje ); mensaje = "";  
    informacion += "<section id='contenido'>" 
    
    informacion += "<br />"
    informacion += html.titulo( "Usuarios Activos" )
    informacion += "<br />"    
    informacion += html.tablaUsuariosActivos(  )

    informacion += "<br />"
    informacion += html.titulo( "Solicitudes Pendientes" )
    informacion += "<br />"    
    informacion += html.tablasolicitudesPendientes(  )
    
    informacion += "</section>"    
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/anadir_usuario' , methods=["GET", "POST"] )
def anadir_usuario():
    if not registrado: return redirect( '/principal' )
    if permisos != 'admin': return redirect( '/principal' )
    
    if request.method == 'POST': 
        usuario = request.form['usuario_hdn'];
        tipo = request.form['tipo_select'];
        
        nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , contra = sql.getAdmision( usuario )
        sql.anadirUsuario( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , contra , tipo )
        sql.crearBaseDatosFinanzas( usuario )
        
        sql.eliminarAdmision( usuario )
        return redirect( '/admision' )
    
    
@aplicacion.route('/eliminar_registro' , methods=["GET", "POST"] )
def eliminar_registro():
    if not registrado: return redirect( '/principal' )
    if permisos != 'admin': return redirect( '/principal' )
    
    if request.method == 'POST': 
        usuario = request.form['usuario_hdn'];
        sql.eliminarAdmision( usuario )
        return redirect( '/admision' )


@aplicacion.route('/cambiar_permisos_usuario' , methods=["GET", "POST"] )
def cambiar_permisos_usuario():
    if not registrado: return redirect( '/principal' )
    if permisos != 'admin': return redirect( '/principal' )
    
    if request.method == 'POST': 
        usuario = request.form['usuario_hdn'];
        tipo = request.form['tipo_select'];
        sql.cambiarPermisosUsuario( usuario , tipo )
    
    return redirect( '/admision' ) 
 
# ---------------------------------------- #
# ------------ Eliminar Usuario ---------- #
# ---------------------------------------- #    

@aplicacion.route('/eliminar_usuario' , methods=["GET", "POST"] )
def eliminar_usuario():
    if not registrado: return redirect( '/principal' )
    
    if request.method == 'POST': 
        usuario = request.form['usuario_hdn'];
        sql.eliminarUsuario( usuario )
        sql.eliminarBaseDatosFinanzas( usuario )
        
    if permisos == 'admin': return redirect( '/admision' )
    else: return redirect( '/principal' ) 

####################################################################    
#------------------------- PAGINA RESUMEN -------------------------#
####################################################################

@aplicacion.route('/balance')
def balance():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += "<section id='contenido'>"
    
    informacion += html.titulo( "Balance" )
    informacion += "<br />"
    # TODO
    
    informacion += "</section>" 
    informacion += render_template('0_footer.php')
    return informacion

####################################################################    
#------------------------- PAGINA FINANZAS ------------------------#
####################################################################

# ---------------------------------------- #
# ------------- Tabla Resumen ------------ #
# ---------------------------------------- #
    
@aplicacion.route('/finanzas')
def finanzas():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_finanzas.php')
    informacion += "<section id='contenido'>"
    
    cabeceras = listaOperaciones.resumenAnos.getCabeceras()
    cuerpoGastos , cuerpoIngresos = listaOperaciones.resumenAnos.getCuerpo();
    
    informacion += "<br />"
    informacion += html.titulo( "Resumen" )
    informacion += "<br />"
    informacion += html.subTitulo( "Gastos" )
    informacion += "<br />"
    informacion += html.tablaResumenFinanzas( "General_Gastos" , listaOperaciones.resumen , cabeceras , cuerpoGastos );
    informacion += "<br />"
    informacion += html.subTitulo( "Ingresos" )
    informacion += "<br />"
    informacion += html.tablaResumenFinanzas( "General_Ingresos" , listaOperaciones.resumen , cabeceras , cuerpoIngresos );
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion

# ---------------------------------------- #
# --------------- Sectores --------------- #
# ---------------------------------------- #

@aplicacion.route('/finanzas_sectores' , methods=["GET", "POST"] )
def finanzas_sectores():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_finanzas.php')
    informacion += "<section id='contenido'>"
    
    resumenes = listaOperaciones.resumenAnos.getResumenes()
        
    informacion += "<br />"
    informacion += html.titulo( "Graficos" )
    informacion += "<br />"
    
    informacion += "<form id='resumenAno' name='resumenAno' action='' method='post'>"
    informacion += "<fieldset>"
    informacion += "<select id='resumenAnos_select' name='resumenAnos_select' onchange='this.form.submit()'>"
    informacion += "    <option selected value='Todos'> Seleccione un año </option>"
    informacion += "    <option value='Todos'> Todo </option>"
    informacion += "    <option value='Global'> Global </option>"
    for resumen in resumenes:
        informacion += "<option value='" + resumen + "'> Año " + resumen + " </option>"
    informacion += "</select>"
    informacion += "</fieldset>"	
    informacion += "</form>"	
    
    resumenAno = "Todos"
    if request.method == 'POST': resumenAno = request.form['resumenAnos_select'];
        
    informacion += "<br />"
    if resumenAno == "Global":
        informacion += html.subTitulo( "Global" )
        informacion += html.graficoSectoresFinanzas( "General" , listaOperaciones.resumen )
    elif resumenAno == "Todos":
        informacion += html.subTitulo( "Global" )
        informacion += html.graficoSectoresFinanzas( "General" , listaOperaciones.resumen )
        informacion += "<br />"
        for resumen in resumenes:                        
            informacion += html.subTitulo( "Año " + resumen )
            informacion += "<br />"
            informacion += html.graficoSectoresFinanzas( resumen , resumenes[resumen] )
            informacion += "<br />"    
    else:
        informacion += html.subTitulo( "Año " + resumenAno )
        informacion += html.graficoSectoresFinanzas( resumenAno , resumenes[resumenAno] )
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion

# ---------------------------------------- #
# -------------- Categorias -------------- #
# ---------------------------------------- #

@aplicacion.route('/finanzas_categorias' , methods=["GET", "POST"] )
def finanzas_categorias():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_finanzas.php')
    informacion += "<section id='contenido'>"
    
    cabeceras = listaOperaciones.resumenAnos.getCabeceras()
    resumenes = listaOperaciones.resumenAnos.getResumenes()
        
    informacion += "<br />"
    informacion += html.titulo( "Categorias" )
    informacion += "<br />"
    
    informacion += "<form id='resumenCategorias' name='resumenCategorias' action='' method='post'>"
    informacion += "<fieldset>"
    informacion += "<select id='resumenCategorias_select' name='resumenCategorias_select' >"
    informacion += "    <option selected value='Gastos'> Seleccione un Valor </option>"
    informacion += "    <option value='Gastos'> Gastos </option>"
    informacion += "    <option value='Ingresos'> Ingresos </option>"
    informacion += "</select> &nbsp &nbsp &nbsp"
    informacion += "<select id='vistaCategorias_select' name='vistaCategorias_select' >"
    informacion += "    <option selected value='Categorias'> Seleccione una Vista </option>"
    informacion += "    <option value='Categorias'> Categorias </option>"
    informacion += "    <option value='Anual'> Anual </option>"
    informacion += "</select> <br />"
    informacion += "<input type='submit' id='aceptar' name='vistaCategorias_btn' value='Aceptar'/>"
    informacion += "</fieldset>" + "</form>"
    
    tipo = "Gastos"
    vista = "Anual"
    if request.method == 'POST': 
        tipo = request.form['resumenCategorias_select'];
        vista = request.form['vistaCategorias_select'];
    
    if vista == "Categorias":
        informacion += html.graficoBarrasAgrupadoCategoriasFinanzas( "Categorias" , cabeceras , resumenes , tipo )
    else:
        informacion += html.graficoBarrasAgrupadoAnosFinanzas( "Categorias" , cabeceras , resumenes , tipo )

    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion

####################################################################    
#----------------------- PAGINA INVERSIONES -----------------------#
####################################################################

# ---------------------------------------- #
# -------------- HISTORICO --------------- #
# ---------------------------------------- #

@aplicacion.route('/inversiones')
def inversiones():
    if not registrado: return redirect( '/principal' )   
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    
    # TODO
    
    informacion += render_template('0_footer.php')
    return informacion
    
# ---------------------------------------- #
# -------------- RESUMENES --------------- #
# ---------------------------------------- #
    
@aplicacion.route('/inversiones_resumenes')
def inversiones_resumenes():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_resumenes.php')
    informacion += "<section id='contenido'>"
    
    informacion += html.titulo( "Resumen" )
    informacion += "<br />"
    informacion += html.tablaResumenInversiones( listaInversiones.resumen , listaInversiones.resumenActivos );
    
    informacion += html.titulo( "Graficas" )
    informacion += "<br />"
    informacion += html.graficoSectoresInversiones( "AssetAllocation" , listaInversiones.resumenActivos )
    informacion += "<br />"
    informacion += html.graficoRentabilidadesInversiones( "Rentabilidades" , listaInversiones.resumenActivos )

    informacion += "</section>" 
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/inversiones_resumenes_categorias')
def inversiones_resumenes_categorias():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_resumenes.php')
    informacion += "<section id='contenido'>"
    
    informacion += html.titulo( "Resumen" )
    informacion += "<br />"
    informacion += html.tablaResumenInversiones( listaInversiones.resumen , listaInversiones.resumenCategorias );
    
    informacion += html.titulo( "Graficas" )
    informacion += "<br />"
    informacion += html.graficoSectoresInversiones( "AssetAllocation" , listaInversiones.resumenCategorias )
    informacion += "<br />"
    informacion += html.graficoRentabilidadesInversiones( "Rentabilidades" , listaInversiones.resumenCategorias )

    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion

    
@aplicacion.route('/inversiones_resumenes_estrategias')
def inversiones_resumenes_estrategias():    
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_resumenes.php')    
    informacion += "<section id='contenido'>"
    
    informacion += html.titulo( "Resumen" )
    informacion += "<br />"
    informacion += html.tablaResumenInversiones( listaInversiones.resumen , listaInversiones.resumenEstrategias );
    
    informacion += html.titulo( "Graficas" )
    informacion += "<br />"
    informacion += html.graficoSectoresInversiones( "AssetAllocation" , listaInversiones.resumenEstrategias )
    informacion += "<br />"
    informacion += html.graficoRentabilidadesInversiones( "Rentabilidades" , listaInversiones.resumenEstrategias )

    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/inversiones_resumenes_brokers')
def inversiones_resumenes_brokers():
    if not registrado: return redirect( '/principal' )    
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_resumenes.php')    
    informacion += "<section id='contenido'>"
    
    informacion += html.titulo( "Resumen" )
    informacion += "<br />"
    informacion += html.tablaResumenInversiones( listaInversiones.resumen , listaInversiones.resumenBrokers );
    
    informacion += html.titulo( "Graficas" )
    informacion += "<br />"
    informacion += html.graficoSectoresInversiones( "AssetAllocation" , listaInversiones.resumenBrokers )
    informacion += "<br />"
    informacion += html.graficoRentabilidadesInversiones( "Rentabilidades" , listaInversiones.resumenBrokers )
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion

# ---------------------------------------- #
# ------------ DISTRIBUCIONES ------------ #
# ---------------------------------------- #

@aplicacion.route('/inversiones_distribuciones')
def inversiones_distribuciones():
    if not registrado: return redirect( '/principal' )    
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_distribuciones.php')    
    informacion += "<section id='contenido'>"
    
    informacion += html.titulo( "Distribuciones" )
    informacion += "<br />"
       
    informacion += listaInversiones.resumen.graficoComposiciones( "Composiciones" , usuario )
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/inversiones_distribuciones_activos' , methods=["GET", "POST"] )
def inversiones_distribuciones_activos():    
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_distribuciones.php')    
    informacion += "<section id='contenido'>"
    
    resumenes = listaInversiones.resumenActivos.listaResumen
    
    informacion += "<form id='resumenComposiciones' name='resumenComposiciones' action='' method='post'>"
    informacion += "<fieldset>"
    informacion += "<select id='resumenComposiciones_select' name='resumenComposiciones_select' onchange='this.form.submit()' >"
    informacion += "    <option selected disabled> Seleccione un Resumen </option>"

    for resumen in resumenes:
        informacion += "    <option value='" + resumen + "'> " + resumen + " </option>"
    informacion += "</select> &nbsp &nbsp &nbsp"
    informacion += "</fieldset>" + "</form>"
    
    if request.method == 'POST': 
        resumen = request.form['resumenComposiciones_select'];
        informacion += html.titulo( "Distribuciones para " + resumen )
    else: informacion += html.titulo( "Distribuciones para " + resumen )
    
    informacion += "<br />"
    informacion += resumenes[ resumen ].graficoComposiciones( "Composiciones" , usuario )
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/inversiones_distribuciones_categorias' , methods=["GET", "POST"] )
def inversiones_distribuciones_categorias():    
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_distribuciones.php')    
    informacion += "<section id='contenido'>"
    
    resumenes = listaInversiones.resumenCategorias.listaResumen
    
    informacion += "<form id='resumenComposiciones' name='resumenComposiciones' action='' method='post'>"
    informacion += "<fieldset>"
    informacion += "<select id='resumenComposiciones_select' name='resumenComposiciones_select' onchange='this.form.submit()' >"
    informacion += "    <option selected disabled> Seleccione un Resumen </option>"
    
    for resumen in resumenes:
        informacion += "    <option value='" + resumen + "'> " + resumen + " </option>"
    informacion += "</select> &nbsp &nbsp &nbsp"
    informacion += "</fieldset>" + "</form>"

    if request.method == 'POST': 
        resumen = request.form['resumenComposiciones_select'];
        informacion += html.titulo( "Distribuciones para " + resumen )
    else: informacion += html.titulo( "Distribuciones para " + resumen )
    
    informacion += "<br />"
    informacion += resumenes[ resumen ].graficoComposiciones( "Composiciones" , usuario )
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/inversiones_distribuciones_estrategias' , methods=["GET", "POST"] )
def inversiones_distribuciones_estrategias():   
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_distribuciones.php')    
    informacion += "<section id='contenido'>"
    
    resumenes = listaInversiones.resumenEstrategias.listaResumen
    
    informacion += "<form id='resumenComposiciones' name='resumenComposiciones' action='' method='post'>"
    informacion += "<fieldset>"
    informacion += "<select id='resumenComposiciones_select' name='resumenComposiciones_select' onchange='this.form.submit()' >"
    informacion += "    <option selected disabled> Seleccione un Resumen </option>"
    
    for resumen in resumenes:
        informacion += "    <option value='" + resumen + "'> " + resumen + " </option>"
    informacion += "</select> &nbsp &nbsp &nbsp"
    informacion += "</fieldset>" + "</form>"

    if request.method == 'POST': 
        resumen = request.form['resumenComposiciones_select'];
        informacion += html.titulo( "Distribuciones para " + resumen )
    else: informacion += html.titulo( "Distribuciones para " + resumen )
    
    informacion += "<br />"
    informacion += resumenes[ resumen ].graficoComposiciones( "Composiciones" , usuario )
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/inversiones_distribuciones_brokers' , methods=["GET", "POST"] )
def inversiones_distribuciones_brokers():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_distribuciones.php')    
    informacion += "<section id='contenido'>"    
    
    resumenes = listaInversiones.resumenBrokers.listaResumen
    
    informacion += "<form id='resumenComposiciones' name='resumenComposiciones' action='' method='post'>"
    informacion += "<fieldset>"
    informacion += "<select id='resumenComposiciones_select' name='resumenComposiciones_select' onchange='this.form.submit()' >"
    informacion += "    <option selected disabled> Seleccione un Resumen </option>"
    
    for resumen in resumenes:
        informacion += "    <option value='" + resumen + "'> " + resumen + " </option>"
    informacion += "</select> &nbsp &nbsp &nbsp"
    informacion += "</fieldset>" + "</form>"
    resumen = ""
    if request.method == 'POST': 
        resumen = request.form['resumenComposiciones_select'];
        informacion += html.titulo( "Distribuciones para " + resumen )
    else: informacion += html.titulo( "Distribuciones para " + resumen )
    
    informacion += "<br />"
    informacion += resumenes[ resumen ].graficoComposiciones( "Composiciones" , usuario )
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion

####################################################################    
#---------------------------- GESTIONES ---------------------------#
####################################################################

# ---------------------------------------- #
# --------------- FINANZAS --------------- #
# ---------------------------------------- #

@aplicacion.route('/finanzas_gestionar' , methods=["GET", "POST"] )
def finanzas_gestionar():
    global variablesGobales;
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_finanzas.php')
    informacion += render_template('Nav_3_finanzas_gestion.php')
    informacion += "<section id='contenido'>" 
    
    resumenes = listaOperaciones.resumenAnos.getResumenes()
    
    informacion += "<table id='equipos'>"
    informacion += "<tr>"
    informacion += "    <form name='ordenar_frm' action='finanzas_gestionar' method='post' enctype='application/x-www-form-urlencoded'> "	
    informacion += "    <th>"
    informacion += "        	<select id='fecha_select' class='cambio' name='fecha_select' > "
    informacion += "                <option selected value='' > FECHA </option> "   
    for resumen in resumenes:
        informacion += "            <option value='" + resumen + "'> Año " + resumen + " </option>"
    informacion += "        	</select>   				 "    
    informacion += "    </th>"
    informacion += "    <th>"
    informacion += "        	<select id='clasificacion_select' class='cambio' name='clasificacion_select' > "
    informacion += "                <option selected value='' > CLASE </option> "   
    for resumen in sql.getClases( usuario ):
        informacion += "            <option value='" + resumen + "'> " + resumen + " </option>"
    informacion += "        	</select>   				 "    
    informacion += "    </th>"
    
    informacion += "    <th> ASUNTO </th>"
    informacion += "	<th> DESCRIPCION </th>"
    informacion += "	<th> GASTO </th>"
    informacion += "	<th> INGRESO </th>"
    informacion += "	<th>"
    informacion += "         <input type='submit' id='aceptar' class='editar' name='filtar_btn' value='Filtar'/>	 "
    informacion += "    </th>"
    informacion += "    </form> "
    informacion += "</tr>"
    
    if "finanzas_gestionar_fecha" not in variablesGobales: variablesGobales["finanzas_gestionar_fecha"] = "";
    if "finanzas_gestionar_clasificacion" not in variablesGobales: variablesGobales["finanzas_gestionar_clasificacion"] = "";  
    if request.method == 'POST': 
        variablesGobales["finanzas_gestionar_fecha"] = request.form['fecha_select'];
        variablesGobales["finanzas_gestionar_clasificacion"] = request.form['clasificacion_select'];
      
    informacion += "    <tr>"
    informacion += "        <form name='ordenar_frm' action='finanzas_anadir' method='post' enctype='application/x-www-form-urlencoded'> "	
    informacion += "            <td>"
    informacion += "                 <input id='fecha_date' type='date' name='fecha_date' required />"        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "        	    <select id='admision' class='cambio' name='valor_select' required> "
    informacion += "                        <option selected disabled > CLASE </option> "   
    for resumen in sql.getClases( usuario ):
        informacion += "                    <option value='" + resumen + "'> " + resumen + " </option>"
    informacion += "        	     </select>   				 "           		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                 <input id='asunto_txt' type='text' name='asunto_txt' pattern='[A-Za-z0-9]*' placeholder='Asunto' required />"		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                 <input id='descripcion_txt' type='text' name='descripcion_txt' pattern='[A-Za-z0-9]*' placeholder='Descripcion' required />"		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                 <input id='gasto_txt' type='number' name='gasto_txt' placeholder='Gasto' required />"		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                 <input id='ingreso_txt' type='number' name='ingreso_txt' placeholder='Ingreso' required />"		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                    <input type='submit' id='aceptar' class='editar' name='anadir_btn' value='Añadir'/>	 "			     		        		
    informacion += "            </td>"
    informacion += "        </form> " 
    informacion += "    <tr>"
    
    resultado = sql.getFinanzasBy( usuario , variablesGobales["finanzas_gestionar_fecha"] , variablesGobales["finanzas_gestionar_clasificacion"] )
    for date , clase , asunto , descripcion , gasto , ingreso in resultado:
        informacion += "    <tr>"
        informacion += "        <td> <h3> " + str(date) + " </h3> </td>"
        informacion += "        <td> " + clase + " </td>"
        informacion += "        <td> " + asunto + " </td>"
        informacion += "        <td> " + descripcion + " </td>"
        informacion += "        <td> " + str( "{:.2f}".format(gasto) ) + " </td>"
        informacion += "        <td> " + str( "{:.2f}".format(ingreso) ) + " </td>"
        informacion += "            <td>"
        informacion += "                <form name='ordenar_frm' action='finanzas_eliminar' method='post' enctype='application/x-www-form-urlencoded'> "	   
        informacion += "                    <input type='hidden' name='fecha_hdn' value='" + str(date) + "' />"
        informacion += "                    <input type='hidden' name='valor_hdn' value='" + clase + "' />"
        informacion += "                    <input type='hidden' name='asunto_hdn' value='" + asunto + "' />"
        informacion += "                    <input type='hidden' name='descripcion_hdn' value='" + descripcion + "' />"
        informacion += "                    <input type='submit' id='eliminar' class='editar' name='eliminar_btn' value='Eliminar'/>	 "			     		        		
        informacion += "                </form> "
        informacion += "            </td>"
        informacion += "    <tr>"
        
    informacion += "</table>"
    informacion += "<br />"
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion

# -------- Anadir -------- #

@aplicacion.route('/finanzas_anadir' , methods=["GET", "POST"] )
def finanzas_anadir():
    if not registrado: return redirect( '/principal' )
    if request.method == 'POST': 
       fecha = request.form['fecha_date'];
       clasificacion = request.form['valor_select'];
       asunto = request.form['asunto_txt'];
       descripcion = request.form['descripcion_txt'];
       gasto = request.form['gasto_txt'];
       ingreso = request.form['ingreso_txt'];    
       sql.anadirFinanzas( usuario , fecha , clasificacion , asunto , descripcion , gasto , ingreso ) 
    return redirect( '/finanzas_gestionar' );

# ------- Eliminar ------- #

@aplicacion.route('/finanzas_eliminar' , methods=["GET", "POST"] )
def finanzas_eliminar():
    if not registrado: return redirect( '/principal' )   
    if request.method == 'POST': 
       fecha = request.form['fecha_hdn'];
       clasificacion = request.form['valor_hdn'];
       asunto = request.form['asunto_hdn'];
       descripcion = request.form['descripcion_hdn'];       
       sql.eliminarFinanzas( usuario , fecha , clasificacion , asunto , descripcion )      
    return redirect( '/finanzas_gestionar' );

# ---------------------------------------- #
# ------------- INVERSIONES -------------- #
# ---------------------------------------- #

@aplicacion.route('/inversiones_gestionar' , methods=["GET", "POST"] )
def inversiones_gestionar():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_gestion.php')
    informacion += "<section id='contenido'>"
    
    informacion += "<table id='equipos'>"
    informacion += "<tr>"
    informacion += "    <form name='ordenar_frm' action='inversiones_gestionar' method='post' enctype='application/x-www-form-urlencoded'> "	
    informacion += "    <th> ISIN </th>"
    informacion += "    <th> TIPO </th>"
    informacion += "    <th>"
    informacion += "        	<select id='categoria_select' class='cambio' name='categoria_select' > "
    informacion += "                <option selected value='' > CATEGORIA </option> "   
    for categoria , color in sql.getCategoriaDistribucion( usuario , "categoria" ):
        informacion += "            <option value='" + categoria + "'> " + categoria + " </option>"
    informacion += "        	</select>  "    
    informacion += "    </th>"
    informacion += "    <th>"
    informacion += "        	<select id='estrategia_select' class='cambio' name='estrategia_select' > "
    informacion += "                <option selected value='' > ESTRATEGIA </option> "   
    for estrategia , color in sql.getCategoriaDistribucion( usuario , "estrategia" ):
        informacion += "            <option value='" + estrategia + "'> " + estrategia + " </option>"
    informacion += "        	</select>   				 "    
    informacion += "    </th>"
    informacion += "    <th>"
    informacion += "        	<select id='producto_select' class='cambio' name='producto_select' > "
    informacion += "                <option selected value='' > PRODUCTO </option> "   
    for producto , color in sql.getCategoriaDistribucion( usuario , "descripcion" ):
        informacion += "            <option value='" + producto + "'> " + producto + " </option>"
    informacion += "        	</select>   				 "    
    informacion += "    </th>"
    informacion += "    <th> LINK </th>"
    informacion += "	<th>"
    informacion += "         <input type='submit' id='aceptar' class='editar' name='filtar_btn' value='Filtar'/>	 "
    informacion += "    </th>"
    informacion += "    </form> "
    informacion += "</tr>"
    
    if "inversiones_gestionar_categoria" not in variablesGobales: variablesGobales["inversiones_gestionar_categoria"] = "";
    if "inversiones_gestionar_estrategia" not in variablesGobales: variablesGobales["inversiones_gestionar_estrategia"] = "";
    if "inversiones_gestionar_producto" not in variablesGobales: variablesGobales["inversiones_gestionar_producto"] = "";
    if request.method == 'POST': 
        variablesGobales["inversiones_gestionar_categoria"] = request.form['categoria_select'];
        variablesGobales["inversiones_gestionar_estrategia"] = request.form['estrategia_select'];
        variablesGobales["inversiones_gestionar_producto"] = request.form['producto_select'];
    
    informacion += "    <tr>"
    informacion += "        <form name='ordenar_frm' action='inversiones_gestionar_anadir_activos' method='post' enctype='application/x-www-form-urlencoded'> "	
    informacion += "            <td>"
    informacion += "                 <input id='isin_txt' type='text' name='isin_txt' pattern='[A-Z0-9]*' placeholder='ISIN del producto' required />"        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "        	<select id='tipo_txt' class='cambio' name='tipo_txt' required > "
    informacion += "                <option selected disabled > Tipo de producto </option> "   
    informacion += "                <option value='ETF'>  ETF  </option>"
    informacion += "                <option value='Fondo'>  Fondo  </option>"
    informacion += "                <option value='Accion'>  Accion  </option>"
    informacion += "        	</select>"		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "        	    <select id='categoria_select' class='cambio' name='categoria_select' required > "
    informacion += "                    <option selected value='' > CATEGORIA </option> "   
    for categoria , color in sql.getCategoriaDistribucion( usuario , "categoria" ):
        informacion += "                <option value='" + categoria + "'> " + categoria + " </option>"
    informacion += "        	     </select>  " 
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "        	    <select id='estrategia_select' class='cambio' name='estrategia_select' required > "
    informacion += "                     <option selected value='' > ESTRATEGIA </option> "   
    for estrategia , color in sql.getCategoriaDistribucion( usuario , "estrategia" ):
        informacion += "                 <option value='" + estrategia + "'> " + estrategia + " </option>"
    informacion += "        	     </select>  	 "        			     		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "        	    <select id='producto_select' class='cambio' name='producto_select' required > "
    informacion += "                     <option selected value='' > PRODUCTO </option> "   
    for producto , color in sql.getCategoriaDistribucion( usuario , "descripcion" ):
        informacion += "                 <option value='" + producto + "'> " + producto + " </option>"
    informacion += "        	    </select>   "                			     		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                 <input id='link_txt' type='text' name='link_txt' pattern='[A-Za-z0-9]*' placeholder='Enlace al producto' required />"		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                    <input type='submit' id='aceptar' class='editar' name='anadir_btn' value='Añadir'/>	 "			     		        		
    informacion += "            </td>"
    informacion += "        </form> " 
    informacion += "    <tr>"
    
    resultado = sql.getActivosBy( usuario , variablesGobales["inversiones_gestionar_categoria"] , variablesGobales["inversiones_gestionar_estrategia"] , variablesGobales["inversiones_gestionar_producto"] )
    for isin , tipo , categoria , estrategia , producto , link in resultado:
        informacion += "    <tr>"
        informacion += "        <td> <h3> " + isin + " </h3> </td>"
        informacion += "        <td> " + tipo + " </td>"
        informacion += "        <td> " + categoria + " </td>"
        informacion += "        <td> " + estrategia + " </td>"
        informacion += "        <td> " + producto + " </td>"
        informacion += "        <td> " + link + " </td>"
        informacion += "            <td>"
        informacion += "                <form name='ordenar_frm' action='inversiones_gestionar_eliminar_activos' method='post' enctype='application/x-www-form-urlencoded'> "	   
        informacion += "                    <input type='hidden' name='isin_hdn' value='" + isin + "' />"
        informacion += "                    <input type='submit' id='eliminar' class='editar' name='eliminar_btn' value='Eliminar'/>	 "			     		        		
        informacion += "                </form> "
        informacion += "            </td>"
        informacion += "    <tr>"
      
    informacion += "</table>"
    informacion += "<br />"
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/inversiones_gestionar_aportaciones' , methods=["GET", "POST"] )
def inversiones_gestionar_aportaciones():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_gestion.php')
    informacion += "<section id='contenido'>"
    
    informacion += "<table id='equipos'>"
    informacion += "<tr>"
    informacion += "    <form name='ordenar_frm' action='inversiones_gestionar_aportaciones' method='post' enctype='application/x-www-form-urlencoded'> "	
    informacion += "    <th> "
    informacion += "           <input id='fecha_date' type='date' name='fecha_date' placeholder='FECHA' />"
    informacion += "    </th>"
    informacion += "    <th> "
    informacion += "           <input id='isin_txt' type='text' name='isin_txt' placeholder='ISIN' />"		        		
    informacion += "    </th>"
    informacion += "    <th> TITULOS </th>"
    informacion += "    <th> PRECIO </th>"
    informacion += "    <th>"
    informacion += "        	<select id='broker_select' class='cambio' name='broker_select' > "
    informacion += "                <option selected value='' > PRODUCTO </option> "   
    for broker , color in sql.getCategoriaDistribucion( usuario , "broker" ):
        informacion += "            <option value='" + broker + "'> " + broker + " </option>"
    informacion += "        	</select>   				 "    
    informacion += "    </th>"
    informacion += "    <th> LINK </th>"
    informacion += "	<th>"
    informacion += "         <input type='submit' id='aceptar' class='editar' name='filtar_btn' value='Filtar'/>	 "
    informacion += "    </th>"
    informacion += "    </form> "
    informacion += "</tr>"
    
    if "inversiones_gestionar_date" not in variablesGobales: variablesGobales["inversiones_gestionar_date"] = "";
    if "inversiones_gestionar_isin" not in variablesGobales: variablesGobales["inversiones_gestionar_isin"] = "";
    if "inversiones_gestionar_broker" not in variablesGobales: variablesGobales["inversiones_gestionar_broker"] = "";
    if request.method == 'POST': 
        variablesGobales["inversiones_gestionar_date"] = utilidades.getYear(request.form['fecha_date']);
        variablesGobales["inversiones_gestionar_isin"] = request.form['isin_txt'];
        variablesGobales["inversiones_gestionar_broker"] = request.form['broker_select'];
    
    informacion += "    <tr>"
    informacion += "        <form name='ordenar_frm' action='inversiones_gestionar_anadir_aportaciones' method='post' enctype='application/x-www-form-urlencoded'> "	
    informacion += "            <td>"
    informacion += "                 <input id='fecha_date' type='date' name='fecha_date' required />"        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                 <input id='isin_txt' type='text' name='isin_txt' pattern='[A-Z0-9]*' placeholder='ISIN del producto' required />"        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                 <input id='titulos_txt' type='number' name='titulos_txt' placeholder='Titulos' required />"		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                 <input id='precio_txt' type='number' name='precio_txt' placeholder='Precio de compra/venta' required />"		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "        	    <select id='broker_select' class='cambio' name='broker_select' > "
    informacion += "                     <option selected value='' > PRODUCTO </option> "   
    for broker , color in sql.getCategoriaDistribucion( usuario , "broker" ):
        informacion += "                 <option value='" + broker + "'> " + broker + " </option>"
    informacion += "        	    </select>"
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "        	    <select id='operacion_select' class='cambio' name='operacion_select' required > "
    informacion += "                     <option selected value='' > OPERACION </option> "   
    informacion += "                     <option value='compra'> Compra </option>"
    informacion += "                     <option value='venta'> Venta </option>"
    informacion += "        	    </select>  	 "        			     		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                    <input type='submit' id='aceptar' class='editar' name='anadir_btn' value='Añadir'/>	 "			     		        		
    informacion += "            </td>"
    informacion += "        </form> " 
    informacion += "    <tr>"
    
    resultado = sql.getAportacionesBy( usuario , variablesGobales["inversiones_gestionar_date"] , variablesGobales["inversiones_gestionar_isin"] , variablesGobales["inversiones_gestionar_broker"] )
    for fecha , isin , titulos , precio , broker , operacion in resultado:
        informacion += "    <tr>"
        informacion += "        <td> <h3> " + str(fecha) + " </h3> </td>"
        informacion += "        <td> " + isin + " </td>"
        informacion += "        <td> " + str( "{:.2f}".format(titulos) ) + " </td>"
        informacion += "        <td> " + str( "{:.2f}".format(precio) ) + " </td>"
        informacion += "        <td> " + broker + " </td>"
        informacion += "        <td> " + operacion + " </td>"
        informacion += "            <td>"
        informacion += "                <form name='ordenar_frm' action='inversiones_gestionar_eliminar_aportaciones' method='post' enctype='application/x-www-form-urlencoded'> "	   
        informacion += "                    <input type='hidden' name='isin_hdn' value='" + isin + "' />"
        informacion += "                    <input type='hidden' name='fecha_hdn' value='" + str(fecha) + "' />"
        informacion += "                    <input type='submit' id='eliminar' class='editar' name='eliminar_btn' value='Eliminar'/>	 "			     		        		
        informacion += "                </form> "
        informacion += "            </td>"
        informacion += "    <tr>"
        
    informacion += "</table>"
    informacion += "<br />"
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/inversiones_gestionar_comisiones' , methods=["GET", "POST"] )
def inversiones_gestionar_comisiones():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_gestion.php')
    informacion += "<section id='contenido'>"
    
    informacion += "<table id='equipos'>"
    informacion += "<tr>"
    informacion += "    <form name='ordenar_frm' action='inversiones_gestionar_comisiones' method='post' enctype='application/x-www-form-urlencoded'> "	
    informacion += "    <th> "
    informacion += "           <input id='fecha_date' type='date' name='fecha_date' placeholder='FECHA' />"		        		
    informacion += "    </th>"
    informacion += "    <th> "
    informacion += "           <input id='isin_txt' type='text' name='isin_txt' placeholder='ISIN' />"		        		
    informacion += "    </th>"
    informacion += "    <th>"
    informacion += "        	<select id='broker_select' class='cambio' name='broker_select' > "
    informacion += "                <option selected value='' > PRODUCTO </option> "   
    for broker , color in sql.getCategoriaDistribucion( usuario , "broker" ):
        informacion += "            <option value='" + broker + "'> Año " + broker + " </option>"
    informacion += "        	</select>   				 "    
    informacion += "    </th>"
    informacion += "    <th> TIPO </th>"
    informacion += "    <th> PRECIO </th>"
    informacion += "	<th>"
    informacion += "         <input type='submit' id='aceptar' class='editar' name='filtar_btn' value='Filtar'/>	 "
    informacion += "    </th>"
    informacion += "    </form> "
    informacion += "</tr>"
    
    if "inversiones_gestionar_date" not in variablesGobales: variablesGobales["inversiones_gestionar_date"] = "";
    if "inversiones_gestionar_isin" not in variablesGobales: variablesGobales["inversiones_gestionar_isin"] = "";
    if "inversiones_gestionar_broker" not in variablesGobales: variablesGobales["inversiones_gestionar_broker"] = "";
    if request.method == 'POST': 
        variablesGobales["inversiones_gestionar_date"] = utilidades.getYear(request.form['fecha_date']);
        variablesGobales["inversiones_gestionar_isin"] = request.form['isin_txt'];
        variablesGobales["inversiones_gestionar_broker"] = request.form['broker_select'];
     
    informacion += "    <tr>"
    informacion += "        <form name='ordenar_frm' action='inversiones_gestionar_anadir_comisiones' method='post' enctype='application/x-www-form-urlencoded'> "	
    informacion += "            <td>"
    informacion += "                 <input id='fecha_date' type='date' name='fecha_date' required />"        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                 <input id='isin_txt' type='text' name='isin_txt' pattern='[A-Z0-9]*' placeholder='ISIN del producto' required />"        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "        	    <select id='broker_select' class='cambio' name='broker_select' > "
    informacion += "                     <option selected value='' > PRODUCTO </option> "   
    for broker , color in sql.getCategoriaDistribucion( usuario , "broker" ):
        informacion += "                 <option value='" + broker + "'> " + broker + " </option>"
    informacion += "        	    </select>"
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "        	    <select id='comision_select' class='cambio' name='comision_select' required > "
    informacion += "                     <option selected value='' > OPERACION </option> "   
    informacion += "                     <option value='comision'> Comision </option>"
    informacion += "                     <option value='dividendo'> Dividendo </option>"
    informacion += "        	    </select>  	 "
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                 <input id='precio_txt' type='number' name='precio_txt' placeholder='Precio de compra/venta' required />"		        		  			     		        		
    informacion += "            </td>"
    informacion += "            <td>"
    informacion += "                    <input type='submit' id='aceptar' class='editar' name='anadir_btn' value='Añadir'/>	 "			     		        		
    informacion += "            </td>"
    informacion += "        </form> " 
    informacion += "    <tr>" 
    
    resultado = sql.getComisionesBy( usuario , variablesGobales["inversiones_gestionar_date"] , variablesGobales["inversiones_gestionar_isin"] , variablesGobales["inversiones_gestionar_broker"] )
    for fecha , isin , broker , comision , precio in resultado:
        informacion += "    <tr>"
        informacion += "        <td> <h3> " + str(fecha) + " </h3> </td>"
        informacion += "        <td> " + isin + " </td>"
        informacion += "        <td> " + broker + " </td>"
        informacion += "        <td> " + comision + " </td>"
        informacion += "        <td> " + str( "{:.2f}".format(precio) ) + " </td>"
        informacion += "            <td>"
        informacion += "                <form name='ordenar_frm' action='inversiones_gestionar_eliminar_comisiones' method='post' enctype='application/x-www-form-urlencoded'> "	   
        informacion += "                    <input type='hidden' name='isin_hdn' value='" + isin + "' />"
        informacion += "                    <input type='hidden' name='fecha_hdn' value='" + str(fecha) + "' />"
        informacion += "                    <input type='submit' id='eliminar' class='editar' name='eliminar_btn' value='Eliminar'/>	 "			     		        		
        informacion += "                </form> "
        informacion += "            </td>"
        informacion += "    <tr>"

    informacion += "</table>"
    informacion += "<br />"

    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion

# -------- Anadir -------- #

@aplicacion.route('/inversiones_gestionar_anadir_activos' , methods=["GET", "POST"] )
def inversiones_gestionar_anadir_activos():
    global variablesGobales;
    if not registrado: return redirect( '/principal' )
    if request.method == 'POST': 
        isin = request.form['isin_txt'];
        tipo = request.form['tipo_txt'];
        categoria = request.form['categoria_select'];
        estrategia = request.form['estrategia_select'];
        producto = request.form['producto_select'];
        link = request.form['link_txt'];
        sql.anadirActivo( usuario , isin , tipo , categoria , estrategia , producto , link )    
    return redirect( "/inversiones_gestionar" )

@aplicacion.route('/inversiones_gestionar_anadir_aportaciones' , methods=["GET", "POST"] )
def inversiones_gestionar_anadir_aportaciones():
    global variablesGobales;
    if not registrado: return redirect( '/principal' )
    if request.method == 'POST': 
        fecha = request.form['fecha_date'];
        isin = request.form['isin_txt'];
        titulos = request.form['titulos_txt'];
        precio = request.form['precio_txt'];
        broker = request.form['broker_select'];
        operacion = request.form['operacion_select'];
        sql.anadirAportacion( usuario , fecha , isin , titulos , precio , broker , operacion )    
    return redirect( "/inversiones_gestionar_aportaciones" )

@aplicacion.route('/inversiones_gestionar_anadir_comisiones' , methods=["GET", "POST"] )
def inversiones_gestionar_anadir_comisiones():
    global variablesGobales;
    if not registrado: return redirect( '/principal' )
    if request.method == 'POST': 
        fecha = request.form['fecha_date'];
        isin = request.form['isin_txt'];
        broker = request.form['broker_select'];
        comision = request.form['comision_select'];
        precio = request.form['precio_txt'];
        sql.anadirComision( usuario , fecha , isin , broker , comision , precio )    
    return redirect( "/inversiones_gestionar_comisiones" )

# ------- Eliminar ------- #

@aplicacion.route('/inversiones_gestionar_eliminar_activos' , methods=["GET", "POST"] )
def inversiones_gestionar_eliminar_activos():
    global variablesGobales;
    if not registrado: return redirect( '/principal' )
    if request.method == 'POST': 
        isin = request.form['isin_hdn'];
        sql.eliminarActivo( usuario , isin )    
    return redirect( "/inversiones_gestionar" )

@aplicacion.route('/inversiones_gestionar_eliminar_aportaciones' , methods=["GET", "POST"] )
def inversiones_gestionar_eliminar_aportaciones():
    global variablesGobales;
    if not registrado: return redirect( '/principal' )
    if request.method == 'POST': 
        isin = request.form['isin_hdn'];
        fecha = request.form['fecha_hdn'];
        sql.eliminarAportacion( usuario , isin , fecha )    
    return redirect( "/inversiones_gestionar_aportaciones" )

@aplicacion.route('/inversiones_gestionar_eliminar_comisiones' , methods=["GET", "POST"] )
def inversiones_gestionar_eliminar_comisiones():
    global variablesGobales;
    if not registrado: return redirect( '/principal' )
    if request.method == 'POST': 
        isin = request.form['isin_hdn'];
        fecha = request.form['fecha_hdn'];
        sql.eliminarComision( usuario , isin , fecha )    
    return redirect( "/inversiones_gestionar_comisiones" )

# ---------------------------------------- #
# ------ CATEGORIAS DISTRIBUCIONES ------- #
# ---------------------------------------- #

@aplicacion.route('/categorias_distribuciones_gestionar_clasificacion' , methods=["GET", "POST"] )
def categorias_distribuciones_gestionar_clasificacion():
    global variablesGobales;
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_finanzas.php')
    informacion += render_template('Nav_3_finanzas_gestion.php')
    informacion += "<section id='contenido'>" 
    
    informacion += html.gestionarCategoriaDistribucion( usuario , "clasificacion"  )
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/categorias_distribuciones_gestionar_categorias' , methods=["GET", "POST"] )
def categorias_distribuciones_gestionar_categorias():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_gestion.php')
    informacion += "<section id='contenido'>" 
    
    informacion += "<form id='resumenComposiciones' name='resumenComposiciones' action='' method='post'>"
    informacion += "<fieldset>"
    informacion += "<select id='categorias_distribuciones_select' name='categorias_distribuciones_select' onchange='this.form.submit()' >"
    informacion += "    <option selected disabled> Seleccione una categoria </option>"
    informacion += "    <option value='descripcion'> Productos </option>"
    informacion += "    <option value='categoria'> Categorias </option>"
    informacion += "    <option value='estrategia'> Estrategias </option>"
    informacion += "    <option value='broker'> Brokers </option>"
    informacion += "</select> &nbsp &nbsp &nbsp"
    informacion += "</fieldset>" + "</form>"
    
    if "gestionar_categorias" not in variablesGobales: variablesGobales["gestionar_categorias"] = "descripcion";  
    if request.method == 'POST': 
        variablesGobales["gestionar_categorias"] = request.form['categorias_distribuciones_select'];
    
    informacion += html.titulo( variablesGobales["gestionar_categorias"] )
    informacion += "<br />"
    informacion += html.gestionarCategoriaDistribucion( usuario , variablesGobales["gestionar_categorias"]  )
    
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion


@aplicacion.route('/categorias_distribuciones_gestionar_distribuciones' , methods=["GET", "POST"])
def categorias_distribuciones_gestionar_distribuciones():
    if not registrado: return redirect( '/principal' )
    informacion = render_template('0_index.php')
    informacion += render_template('Nav_1_inicio.php' , permisos = permisos )
    informacion += render_template('Nav_2_inversiones.php')
    informacion += render_template('Nav_3_inversiones_gestion.php')
    informacion += "<section id='contenido'>" 
    
    informacion += "<form id='resumenComposiciones' name='resumenComposiciones' action='' method='post'>"
    informacion += "<fieldset>"
    informacion += "<select id='categorias_distribuciones_select' name='categorias_distribuciones_select' onchange='this.form.submit()' >"
    informacion += "    <option selected disabled> Seleccione una distribucion </option>"
    informacion += "    <option value='allocation'> Composiciones </option>"
    informacion += "    <option value='region'> Regiones </option>"
    informacion += "    <option value='sector'> Sectores </option>" 
    informacion += "    <option value='capitalizacion'> Capitalizaciones </option>"
    informacion += "    <option value='vencimiento'> Vencimientos </option>"
    informacion += "    <option value='calidad'> Calidades Crediticias </option>"
    informacion += "    <option value='entidad'> Entidades Emisoras </option>"                  
    informacion += "</select> &nbsp &nbsp &nbsp"
    informacion += "</fieldset>" + "</form>"
    
    if "gestionar_distribuciones" not in variablesGobales: variablesGobales["gestionar_distribuciones"] = "allocation";  
    if request.method == 'POST': 
        variablesGobales["gestionar_distribuciones"] = request.form['categorias_distribuciones_select'];
    
    informacion += html.titulo( variablesGobales["gestionar_distribuciones"] )
    informacion += "<br />"
    informacion += html.gestionarCategoriaDistribucion( usuario , variablesGobales["gestionar_distribuciones"]  )
 
    informacion += "</section>"
    informacion += render_template('0_footer.php')
    return informacion

# -------- Anadir -------- #

@aplicacion.route('/anadir_clasificacion_distribucion' , methods=["GET", "POST"] )
def anadir_clasificacion_distribucion():
    global variablesGobales;
    direccion = '/principal';
    if not registrado: return redirect( direccion )

    if request.method == 'POST': 
        categoria_distribucion = request.form['categoria_distribucion'];
        clasificacion = request.form['clase_txt'];
        color = request.form['color_color'];
        color = utilidades.colorHexadecimalToRGB( color )
        sql.anadirCategoriaDistribucion( usuario , categoria_distribucion , clasificacion , color )
    
    if categoria_distribucion == "clasificacion": direccion = 'categorias_distribuciones_gestionar_clasificacion'
    elif categoria_distribucion == "descripcion" or categoria_distribucion == "categoria" or categoria_distribucion == "estrategia" or categoria_distribucion == "broker":
        direccion = 'categorias_distribuciones_gestionar_categorias'
    else: direccion = 'categorias_distribuciones_gestionar_distribuciones'
    
    return redirect( direccion )

# ------- Eliminar ------- #

@aplicacion.route('/eliminar_clasificacion_distribucion' , methods=["GET", "POST"] )
def eliminar_clasificacion_distribucion():
    global variablesGobales;
    direccion = '/principal';
    if not registrado: return redirect( direccion )
    
    if request.method == 'POST': 
        categoria_distribucion = request.form['categoria_distribucion'];
        clasificacion = request.form['clase_hdn'];
        sql.eliminarCategoriaDistribucion( usuario , categoria_distribucion , clasificacion )
        
    if categoria_distribucion == "clasificacion": direccion = 'categorias_distribuciones_gestionar_clasificacion'
    elif categoria_distribucion == "descripcion" or categoria_distribucion == "categoria" or categoria_distribucion == "estrategia" or categoria_distribucion == "broker":
        direccion = 'categorias_distribuciones_gestionar_categorias'
    else: direccion = 'categorias_distribuciones_gestionar_distribuciones'
    
    return redirect( direccion )

# -------- Editar -------- #

@aplicacion.route('/modificar_clasificacion_distribucion' , methods=["GET", "POST"] )
def modificar_clasificacion_distribucion():
    global variablesGobales;
    direccion = '/principal';
    if not registrado: return redirect( direccion )
    
    if request.method == 'POST': 
        categoria_distribucion = request.form['categoria_distribucion'];
        clasificacion = request.form['clase_hdn'];
        color = request.form['color_color'];
        color = utilidades.colorHexadecimalToRGB( color )
        sql.cambiarColor( usuario , categoria_distribucion , clasificacion , color )
        
    if categoria_distribucion == "clasificacion": direccion = 'categorias_distribuciones_gestionar_clasificacion'
    elif categoria_distribucion == "descripcion" or categoria_distribucion == "categoria" or categoria_distribucion == "estrategia" or categoria_distribucion == "broker":
        direccion = 'categorias_distribuciones_gestionar_categorias'
    else: direccion = 'categorias_distribuciones_gestionar_distribuciones'
    
    return redirect( direccion )

####################################################################    
#-------------------- EJECUTAR PAGINA PRINCIPAL -------------------#
#################################################################### 
    
if __name__ == '__main__':
    aplicacion.run( )
