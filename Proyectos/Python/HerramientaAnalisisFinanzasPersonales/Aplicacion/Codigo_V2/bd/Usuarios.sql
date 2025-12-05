DROP DATABASE IF EXISTS usuarios;
CREATE DATABASE usuarios;
USE usuarios;

-- ----------------------------------------------
-- ----------------- USUARIOS -------------------
-- ----------------------------------------------

DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario(
	
	nombre VARCHAR(50)NOT NULL,
	apellido1 VARCHAR(50)NOT NULL,
	apellido2 VARCHAR(50)NOT NULL,
	usuario VARCHAR(50) NOT NULL,
	DNI VARCHAR(9) NOT NULL,
	telefono VARCHAR(13)NOT NULL,
	email VARCHAR(50) NOT NULL,
	password VARCHAR(64) NOT NULL,
	sal VARCHAR(64) NOT NULL,
	permisos int NOT NULL,
	
	PRIMARY KEY(usuario)
	
) DEFAULT CHARSET=latin1;

INSERT INTO usuario( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , sal , permisos ) VALUES ( "david" , "cuesta" , "alario" , "david" , "20857516N" , "615755325" , "davidcuestaalario@gmail.com" , "1718c24b10aeb8099e3fc44960ab6949ab76a267352459f203ea1036bec382c2" , "1234" , 3 );
INSERT INTO usuario( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , sal , permisos ) VALUES ( "david" , "cuesta" , "alario" , "davidcuesta" , "20857516N" , "615755325" , "davidcuestaalario@gmail.com" , "1718c24b10aeb8099e3fc44960ab6949ab76a267352459f203ea1036bec382c2" , "1234" , 2 );
INSERT INTO usuario( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , sal , permisos ) VALUES ( "devilvil" , "muy" , "vil" , "devilvil" , "20857516N" , "615755325" , "devilvilmuyvil@gmail.com" , "1718c24b10aeb8099e3fc44960ab6949ab76a267352459f203ea1036bec382c2" , "1234" , 1 );

-- ----------------------------------------------
-- ---------------- ADMISIONES ------------------
-- ----------------------------------------------

DROP TABLE IF EXISTS admision;
CREATE TABLE admision(
	nombre VARCHAR(50) NOT NULL,
	apellido1 VARCHAR(50)NOT NULL,
	apellido2 VARCHAR(50)NOT NULL,
	usuario VARCHAR(50) NOT NULL,
	DNI VARCHAR(9) NOT NULL,
	telefono VARCHAR(13)NOT NULL,
	email VARCHAR(50) NOT NULL,
	password VARCHAR(64) NOT NULL,
	sal VARCHAR(64) NOT NULL,
	
	PRIMARY KEY(usuario)
	
) DEFAULT CHARSET=latin1;

INSERT INTO admision( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , sal ) VALUES ( "pepito" , "perez" , "perruno" , "pepito" , "20857516N" , "615755325" , "pepito@gmail.com" , "1718c24b10aeb8099e3fc44960ab6949ab76a267352459f203ea1036bec382c2" , "1234" );
INSERT INTO admision( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , sal ) VALUES ( "venganito" , "perez" , "perruno" , "venganito"  , "20857516N" , "615755325" , "venganito@gmail.com" , "1718c24b10aeb8099e3fc44960ab6949ab76a267352459f203ea1036bec382c2" , "1234" );

-- ----------------------------------------------
-- ------------------ ACCESOS -------------------
-- ----------------------------------------------

DROP TABLE IF EXISTS accesos;
CREATE TABLE accesos(

	usuario VARCHAR(50) NOT NULL,
	fecha DATE NOT NULL,
	acceso VARCHAR(1) NOT NULL,
	ip VARCHAR(10) NOT NULL,
	
	PRIMARY KEY(usuario)
	
) DEFAULT CHARSET=latin1;

ALTER TABLE accesos
ADD CONSTRAINT accesos_usuario FOREIGN KEY(usuario) REFERENCES usuario(usuario) ON DELETE CASCADE;

-- ----------------------------------------------
-- ----------------- PERMISOS -------------------
-- ----------------------------------------------

-- SUPER USUARIO
DROP USER IF EXISTS 'DAVID'@'localhost';
CREATE USER 'DAVID'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON *.* TO 'DAVID'@'localhost';
GRANT DELETE , INSERT , SELECT , UPDATE ON usuarios.usuario TO 'DAVID'@'localhost';
GRANT DELETE , INSERT , SELECT , UPDATE ON usuarios.admision TO 'DAVID'@'localhost';
GRANT DELETE , INSERT , SELECT , UPDATE ON usuarios.accesos TO 'DAVID'@'localhost';
GRANT CREATE USER ON *.* TO 'DAVID'@'localhost'; 

-- ADMINISTRADOR
DROP USER IF EXISTS 'davidcuesta'@'localhost';
CREATE USER 'davidcuesta'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON *.* TO 'davidcuesta'@'localhost';
GRANT DELETE , INSERT , SELECT , UPDATE ON usuarios.usuario TO 'davidcuesta'@'localhost';
GRANT DELETE , INSERT , SELECT , UPDATE ON usuarios.admision TO 'davidcuesta'@'localhost';
GRANT CREATE USER ON *.* TO 'davidcuesta'@'localhost'; 

-- USUARIO
DROP USER IF EXISTS 'devilvil'@'localhost';
CREATE USER 'devilvil'@'localhost' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON BD_devilvil.* TO 'devilvil'@'localhost';
GRANT SELECT ON usuarios.usuario TO 'devilvil'@'localhost';
GRANT CREATE USER ON *.* TO 'devilvil'@'localhost'; 