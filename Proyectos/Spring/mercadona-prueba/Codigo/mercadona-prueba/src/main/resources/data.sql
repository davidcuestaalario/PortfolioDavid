-- SECCIONES
-- Insertar las Secciones obligatorias
INSERT INTO seccion (nombre, horas_necesarias) VALUES( 'Horno' , 8 );
INSERT INTO seccion (nombre, horas_necesarias) VALUES( 'Cajas' , 16 );
INSERT INTO seccion (nombre, horas_necesarias) VALUES( 'Pescaderia' , 16 );
INSERT INTO seccion (nombre, horas_necesarias) VALUES( 'Verduras' , 16 );
INSERT INTO seccion (nombre, horas_necesarias) VALUES( 'Drogueria' , 16 );

-- TIENDAS
-- Insertar un par de tiendas
INSERT INTO tienda( codigo , nombre ) VALUES ( 1 , 'Mercadona Ruzafa' );
INSERT INTO tienda( codigo , nombre ) VALUES ( 2 , 'Mercadona Campanar' );

-- TRABAJADORES
-- Ana tiene 8h de contrato
INSERT INTO trabajador( dni , nombre , apellidos , horas_contrato , codigo_tienda ) VALUES ( '11111111A' , 'Ana' , 'Garcia' , 8 , 1 );
-- Luis tiene 4h de contrato
INSERT INTO trabajador( dni , nombre , apellidos , horas_contrato , codigo_tienda ) VALUES ('22222222B' , 'Luis' , 'Martinez' , 4 , 2 );

-- ASIGNACIONES
-- Ana gasta sus 8 horas (4 en Horno, 4 en Cajas)
INSERT INTO asignacion ( dni_trabajador , nombre_seccion , horas_asignadas ) VALUES ('11111111A', 'Horno', 4);
INSERT INTO asignacion ( dni_trabajador , nombre_seccion , horas_asignadas ) VALUES ('11111111A', 'Cajas', 4);
-- Luis gasta solo 2 de sus 4 horas
INSERT INTO asignacion ( dni_trabajador , nombre_seccion , horas_asignadas ) VALUES ('22222222B', 'Horno', 2);

-- APTITUDES
INSERT INTO aptitud (nombre) VALUES( 'Hornear Pan' );
INSERT INTO aptitud (nombre) VALUES( 'Reposteria' );
INSERT INTO aptitud (nombre) VALUES( 'Simpatia' );
INSERT INTO aptitud (nombre) VALUES( 'Matematicas' );
INSERT INTO aptitud (nombre) VALUES( 'Manejo de armas blancas' );
INSERT INTO aptitud (nombre) VALUES( 'Limpiar pescado' );
INSERT INTO aptitud (nombre) VALUES( 'Fortaleza fisica' );
INSERT INTO aptitud (nombre) VALUES( 'Alquimia' );

-- Vincular Aptitudes a las Secciones (Tabla intermedia autogenerada)
-- Aptitudes para el Horno
INSERT INTO seccion_aptitud( nombre_seccion , nombre_aptitud ) VALUES ( 'Horno' , 'Hornear Pan' );
INSERT INTO seccion_aptitud( nombre_seccion , nombre_aptitud ) VALUES ( 'Horno' , 'Reposteria' );
-- Aptitudes para la caja
INSERT INTO seccion_aptitud( nombre_seccion , nombre_aptitud ) VALUES ( 'Cajas' , 'Simpatia' );
INSERT INTO seccion_aptitud( nombre_seccion , nombre_aptitud ) VALUES ( 'Cajas' , 'Matematicas' );
-- Aptitudes para la Pescaderia
INSERT INTO seccion_aptitud( nombre_seccion , nombre_aptitud ) VALUES ( 'Pescaderia' , 'Manejo de armas blancas' );
INSERT INTO seccion_aptitud( nombre_seccion , nombre_aptitud ) VALUES ( 'Pescaderia' , 'Limpiar pescado' );
-- Aptitudes para las Verduras
INSERT INTO seccion_aptitud( nombre_seccion , nombre_aptitud ) VALUES ( 'Verduras' , 'Fortaleza fisica' );
-- Aptitudes para la Drogueria
INSERT INTO seccion_aptitud( nombre_seccion , nombre_aptitud ) VALUES ( 'Drogueria' , 'Alquimia'  );

-- Vincular Aptitudes a los trabajadores
-- Ana sabe Hornear Pan y Simpatia
INSERT INTO trabajador_aptitud( dni_trabajador , nombre_aptitud ) VALUES ( '11111111A', 'Hornear Pan');
INSERT INTO trabajador_aptitud( dni_trabajador , nombre_aptitud ) VALUES ( '11111111A', 'Simpatia');
-- Luis sabe Hornear Hornear Pan y Cajas
INSERT INTO trabajador_aptitud( dni_trabajador , nombre_aptitud ) VALUES ( '22222222B' , 'Hornear Pan' );
INSERT INTO trabajador_aptitud( dni_trabajador , nombre_aptitud ) VALUES ( '22222222B' , 'Matematicas' );

