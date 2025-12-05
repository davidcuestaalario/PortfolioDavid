<br />
	<section id='equipos'>
	<article id='equipo'>
		<hgroup id="equipo"> <h1> Solicitudes pendientes </h1> </hgroup>			
	</article>
	</section>
	<br />

<?php
	// abrimos una conexion
	include("z_BD.php");
	$conexion = abrirBD();
	$consulta = "SELECT * FROM  admision ORDER BY usuario";
?>
	
	<table id="equipos">
		<tr>
			<th> Nombre </th>
			<th> Primer apellido </th>
			<th> Segundo apellido </th>
			<th> DNI </th>
			<th> T&eacute;lefono </th>
			<th> e-mail </th>
			<th> Aceptaci&oacute;n </th>
		</tr> 

<?php 
	
	$ejecucion = consultaBD( $conexion , $consulta );
	while( $registro = todasConsultas( $ejecucion ) )
	{
		$nombre = $registro["nombre"];
		$apellido1 = $registro["apellido1"];
		$apellido2 = $registro["apellido2"];
		$usuario = $registro["usuario"];
		$DNI = $registro["DNI"];
		$telefono = $registro["telefono"];
		$email = $registro["email"];

			echo" 
				<tr>
					<td> <h3> $nombre </h3> </td>
					<td> $apellido1 </td>
					<td> $apellido2 </td>
					<td> $DNI </td>
					<td> $telefono </td>
					<td> $email </td>
					<td> 
						<form name='admitir_frm' action='php/admitir_admitir.php' method='post' enctype='application/x-www-form-urlencoded'>
			 
							<input type='hidden' name='usuario_hdn' value='$usuario' />
						
							<select id='admision' class='cambio' name='tipo_select'>
								<option value='lider'> Lider </option>
								<option value='notario'> Notario </option>
							</select>
							&nbsp &nbsp &nbsp &nbsp
							<select id='admision' class='cambio' name='admision_select'>
								<option value='rechazar'> Rechazar </option>
								<option value='aceptar'> Aceptar </option>	
							</select>
							&nbsp &nbsp &nbsp &nbsp
							<input type='submit' id='editar' class='editar' name='editar_btn' value=' Confirmar '/>
						</form>
					</td>
				</tr>
				
			";
		}
?>
	</table>
	
	<br /> <br />
	
	<section id='equipos'>
	<article id='equipo'>
		<hgroup id="equipo"> <h1> Usuarios Registrados </h1> </hgroup>			
	</article>
	</section>
	<br />
	
	<table id="equipos">
		<tr>
			<th> Nombre </th>
			<th> Primer apellido </th>
			<th> Segundo apellido </th>
			<th> DNI </th>
			<th> T&eacute;lefono </th>
			<th> e-mail </th>
			<th> Categor&iacute;a actual  </th>
			<th> Cambiar Categor&iacute;a </th>
			<th> Eliminar </th>
		</tr> 

<?php 
	
	$consulta = "SELECT * FROM  usuario WHERE tipo != 'admin' ORDER BY usuario";
	$ejecucion = consultaBD( $conexion , $consulta );
	while( $registro = todasConsultas( $ejecucion ) )
	{
		$nombre = $registro["nombre"];
		$apellido1 = $registro["apellido1"];
		$apellido2 = $registro["apellido2"];
		$usuario = $registro["usuario"];
		$DNI = $registro["DNI"];
		$telefono = $registro["telefono"];
		$email = $registro["email"];
		$tipo = $registro["tipo"];
		
		echo" 
				<tr>
					<td> <h3> $nombre </h3> </td>
					<td> $apellido1 </td>
					<td> $apellido2 </td>
					<td> $DNI </td>
					<td> $telefono </td>
					<td> $email </td>
					<td> $tipo </td>
					<td> 
						<form name='registro_recategorizar_frm' action='php/registro_recategorizar.php' method='post' enctype='application/x-www-form-urlencoded'>
			 
							<input type='hidden' name='usuario_hdn' value='$usuario' />
						
							<select id='admision' class='cambio' name='tipo_select'>
								<option value='lider'> Lider </option>
								<option value='notario'> Notario </option>
							</select>
							&nbsp &nbsp &nbsp &nbsp
							<input type='submit' id='aceptar' class='editar' name='editar_btn' value=' Confirmar '/>
						</form>
					</td>
					<td> 
						<form name='registro_eliminar_frm' action='php/registro_eliminar.php' method='post' enctype='application/x-www-form-urlencoded'>
							<input type='hidden' name='usuario_hdn' value='$usuario' />
							<input type='submit' id='eliminar' class='editar' name='editar_btn' value=' Eliminar '/>
						</form>
					</td>
				</tr>
			";		
	}
?>
	</table>
	
<?php 	
	// Cerramos laonexionan
	cerrarBD( $conexion );	
?>