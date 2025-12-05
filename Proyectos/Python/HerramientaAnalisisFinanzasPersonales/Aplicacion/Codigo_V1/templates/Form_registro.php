
		<form id='registro' name='registro_frm' action='' method='post'>
			<fieldset>
			<label for='nombre_txt'> Nombre: </label>
			<input id='nombre_txt' type='text' name='nombre_txt' pattern='[A-Za-z0-9]*' placeholder='Introduzca su nombre' required />
			<br /> <br />
			<label for='apellido1_txt'> Primer apellido: </label>
			<input id='apellido1_txt' type='text' name='apellido1_txt' pattern='[A-Za-z0-9]*' placeholder='Introduzca su primer apellido' required />
			<br /> <br />
			<label for='apellido2_txt'> Segundo apellido: </label>
			<input id='apellido2_txt' type='text' name='apellido2_txt' pattern='[A-Za-z0-9]*' placeholder='Introduzca su segundo apellido' required />
			<br /> <br />
			<label for='usuario_txt'> Usuario: </label>
			<input id='usuario_txt' type='text' name='usuario_txt' pattern='[A-Za-z0-9]*' placeholder='Introduzca un nombre de usuario' title='El nombre de usuario debe ser unico' required />
			<br /> <br /> <br /> <br />
			
			<label for='dni_txt'> DNI: </label>
			<input id='dni_txt' type='text' name='dni_txt' pattern='[0-9]{8}-[A-Za-z]{1}' placeholder='Introduzca su DNI' required />
			<br /> <br />
			<label for='telefono_tel'> Tel&eacute;fono: </label>
			<input id='telefono_tel' type='tel' name='telefono_tel' placeholder='Introduzca su numero de télefono' required />
			<br /> <br />
			<label for='fecha_date'> Fecha nacimiento: </label>
			<input id='fecha_date' type='date' name='fecha_date' placeholder='Introduzca su fecha de nacimiento' />
			<br /> <br />
			<label for='email_email'> email: </label>
			<input id='email_email' type='email' name='email_email' placeholder='Introduzca su e-mail' required />
			<br /> <br /> <br /> <br />
			
			<label for='password_txt'> Contrase&ntilde;a: </label>
			<input id='password_txt' type='password' name='password_txt' title='Las contraseñas deben coincidir' required />
			<br /> <br />
			<label for='passwordRP_txt'> repite la Contrase&ntilde;a: </label>
			<input id='passwordRP_txt' type='password' name='passwordRP_txt' title='Las contraseñas deben coincidir' required />
			<br /> <br />  <br />
			 
			<input type='submit' name='enviar_btn' value='Registrarse' id='procesar_POST' />
			</fieldset>
		</form>

