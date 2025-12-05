-- CREACION DE LA BD mis_contactos
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
	DNI VARCHAR(10) NOT NULL,
	telefono VARCHAR(13)NOT NULL,
	email VARCHAR(50) NOT NULL,
	password VARCHAR(50) NOT NULL,
	tipo VARCHAR(9) NOT NULL,
	
	PRIMARY KEY(usuario)
	
) DEFAULT CHARSET=latin1;

INSERT INTO usuario( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , tipo ) VALUES ( "david" , "cuesta" , "alario" , "davidcuesta" , "20857516-N" , "615755325" , "davidcuestaalario@gmail.com" , "1234" , "admin");
INSERT INTO usuario( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password , tipo ) VALUES ( "devilvil" , "muy" , "vil" , "devilvil" , "20857516-N" , "615755325" , "devilvilmuyvil@gmail.com" , "1234" , "usuario");

-- ----------------------------------------------
-- ---------------- ADMISIONES ------------------
-- ----------------------------------------------

DROP TABLE IF EXISTS admision;
CREATE TABLE admision(
	nombre VARCHAR(50) NOT NULL,
	apellido1 VARCHAR(50)NOT NULL,
	apellido2 VARCHAR(50)NOT NULL,
	usuario VARCHAR(50) NOT NULL,
	DNI VARCHAR(10) NOT NULL,
	telefono VARCHAR(13)NOT NULL,
	email VARCHAR(50) NOT NULL,
	password VARCHAR(50) NOT NULL,
	
	PRIMARY KEY(usuario)
	
) DEFAULT CHARSET=latin1;

INSERT INTO admision( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password ) VALUES ( "pepito" , "perez" , "perruno" , "pepito" , "20857516-N" , "615755325" , "pepito@gmail.com" , "1234");
INSERT INTO admision( nombre , apellido1 , apellido2 , usuario , DNI , telefono , email , password ) VALUES ( "venganito" , "perez" , "perruno" , "venganito"  , "20857516-N" , "615755325" , "venganito@gmail.com" , "1234");

