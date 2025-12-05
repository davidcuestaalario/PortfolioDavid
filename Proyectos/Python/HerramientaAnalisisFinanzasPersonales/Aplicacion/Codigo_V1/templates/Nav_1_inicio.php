<section id="contenido">
	<br />
	<nav id="principal" class="principal">
		<ul>
			<li> <a href="balance"> Balance </a> </li>
			<li> <a href="finanzas"> Finanzas </a> </li>
			<li> <a href="inversiones"> Inversiones </a> </li>
			{% if permisos == 'admin' %}
			<li> <a href="admision"> Admisiones </a> </li>
			{% endif %}
			<li> <a href="logout"> Cerrar Sesion </a> </li>
		</ul>
	</nav>
	<br /> <br />	
</section>
