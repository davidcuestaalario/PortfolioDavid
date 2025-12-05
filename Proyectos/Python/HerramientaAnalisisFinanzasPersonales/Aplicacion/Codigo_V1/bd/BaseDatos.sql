DROP DATABASE IF EXISTS FINANZAS_;
CREATE DATABASE FINANZAS_;
USE FINANZAS_;

-- ----------------------------------------------
-- --------------- DESCRIPCION ------------------
-- ----------------------------------------------

CREATE TABLE DESCRIPCION(
DESCRIPCION VARCHAR(100) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(DESCRIPCION));

-- ----------------------------------------------
-- ---------------- CATEGORIA -------------------
-- ----------------------------------------------

CREATE TABLE CATEGORIA(
CATEGORIA VARCHAR(30) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(CATEGORIA));

-- ----------------------------------------------
-- ---------------- ESTRATEGIA ------------------
-- ----------------------------------------------

CREATE TABLE ESTRATEGIA(
ESTRATEGIA VARCHAR(30) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(ESTRATEGIA));

-- ----------------------------------------------
-- ------------------ BROKER --------------------
-- ----------------------------------------------

CREATE TABLE BROKER(
BROKER VARCHAR(30) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(BROKER));

-- ----------------------------------------------
-- ----------------- INDICES --------------------
-- ----------------------------------------------

CREATE TABLE INDICES(
ISIN VARCHAR(30) NOT NULL,
PRODUCTO VARCHAR(30) NOT NULL,
CATEGORIA VARCHAR(30) NOT NULL,
ESTRATEGIA VARCHAR(30) NOT NULL,
DESCRIPCION VARCHAR(100) NOT NULL,
LINK VARCHAR(100) NOT NULL,
PRIMARY KEY(ISIN));

ALTER TABLE INDICES
ADD CONSTRAINT indice_categoria FOREIGN KEY(CATEGORIA) REFERENCES CATEGORIA(CATEGORIA)  ON DELETE CASCADE,
ADD CONSTRAINT indice_descripcion FOREIGN KEY(DESCRIPCION) REFERENCES DESCRIPCION(DESCRIPCION) ON DELETE CASCADE;

-- ----------------------------------------------
-- --------------- APORTACIONES -----------------
-- ----------------------------------------------

CREATE TABLE APORTACIONES(
FECHA DATE NOT NULL,
ISIN VARCHAR(30) NOT NULL, 
TITULOS FLOAT NOT NULL,
PRECIO FLOAT NOT NULL,
BROKER VARCHAR(100) NOT NULL,
OPERACION VARCHAR(30) NOT NULL,
PRIMARY KEY(FECHA,ISIN));

ALTER TABLE APORTACIONES
ADD CONSTRAINT aportacion_broker FOREIGN KEY(BROKER) REFERENCES BROKER(BROKER) ON DELETE CASCADE,
ADD CONSTRAINT apotacion_indice FOREIGN KEY(ISIN) REFERENCES INDICES(ISIN) ON DELETE CASCADE;

-- ----------------------------------------------
-- ---------------- COMISIONES ------------------
-- ----------------------------------------------

CREATE TABLE COMISIONES(
FECHA DATE NOT NULL,
ISIN VARCHAR(30) NOT NULL, 
BROKER VARCHAR(100) NOT NULL,
COMISION VARCHAR(30) NOT NULL,
PRECIO FLOAT NOT NULL,
PRIMARY KEY(FECHA,ISIN));

ALTER TABLE COMISIONES
ADD CONSTRAINT comision_broker FOREIGN KEY(BROKER) REFERENCES BROKER(BROKER) ON DELETE CASCADE,
ADD CONSTRAINT comision_indice FOREIGN KEY(ISIN) REFERENCES INDICES(ISIN) ON DELETE CASCADE;

-- ----------------------------------------------
-- ---------------- ALLOCATION ------------------
-- ----------------------------------------------

CREATE TABLE ALLOCATION(
ALLOCATION VARCHAR(30) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(ALLOCATION));

INSERT INTO ALLOCATION( ALLOCATION , COLOR ) VALUES( 'Efectivo' , 'rgba( 7 , 181 , 42 , 1 )' );     -- VerdeEsmeralda
INSERT INTO ALLOCATION( ALLOCATION , COLOR ) VALUES( 'Renta Fija' , 'rgba( 0 , 148 , 20 , 1 )' );     -- VerdeOscuro
INSERT INTO ALLOCATION( ALLOCATION , COLOR ) VALUES( 'Renta Variable' , 'rgba( 19 , 6 , 120 , 1 )' );       -- AzulMarino
INSERT INTO ALLOCATION( ALLOCATION , COLOR ) VALUES( 'Commodities' , 'rgba( 138 , 122 , 3 , 1 )' );       -- Dorado
INSERT INTO ALLOCATION( ALLOCATION , COLOR ) VALUES( 'Real State' , 'rgba( 120 , 3 , 138 , 1 )' );        -- Violeta

CREATE TABLE ALLOCATIONS(
ISIN VARCHAR(30) NOT NULL,
ALLOCATION VARCHAR(30) NOT NULL,
PORCENTAJE FLOAT NOT NULL,
PRIMARY KEY( ISIN , ALLOCATION ));

ALTER TABLE ALLOCATIONS
ADD CONSTRAINT allocation_indice FOREIGN KEY(ISIN) REFERENCES INDICES(ISIN) ON DELETE CASCADE,
ADD CONSTRAINT allocation_allocation FOREIGN KEY(ALLOCATION) REFERENCES ALLOCATION(ALLOCATION) ON DELETE CASCADE;

-- ----------------------------------------------
-- ------------------ REGION --------------------
-- ----------------------------------------------

CREATE TABLE REGION(
REGION VARCHAR(30) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(REGION));

INSERT INTO REGION( REGION , COLOR ) VALUES( 'Estados Unidos' , 'rgba( 19 , 6 , 120 , 1 )' );       -- AzulMarino
INSERT INTO REGION( REGION , COLOR ) VALUES( 'Canada' , 'rgba( 230 , 0 , 0 , 1 )' );        -- Rojo
INSERT INTO REGION( REGION , COLOR ) VALUES( 'Latino America' , 'rgba( 0 , 148 , 20 , 1 )' );     -- VerdeOscuro
INSERT INTO REGION( REGION , COLOR ) VALUES( 'Reino Unido' , 'rgba( 120 , 3 , 138 , 1 )' );        -- Violeta
INSERT INTO REGION( REGION , COLOR ) VALUES( 'Europa' , 'rgba( 52 , 215 , 247 , 1 )' );       -- AzulCeleste
INSERT INTO REGION( REGION , COLOR ) VALUES( 'Africa' , 'rgba( 230 , 174 , 44 , 1 )' );        -- Naranja
INSERT INTO REGION( REGION , COLOR ) VALUES( 'Oriente Medio' , 'rgba( 230 , 227 , 44 , 1 )' );     -- Amarillo
INSERT INTO REGION( REGION , COLOR ) VALUES( 'Japon' , 'rgba( 148 , 142 , 132 , 1 )' );        -- Plateado
INSERT INTO REGION( REGION , COLOR ) VALUES( 'Australia' , 'rgba( 138 , 122 , 3 , 1 )' );       -- Dorado
INSERT INTO REGION( REGION , COLOR ) VALUES( 'Asia' , 'rgba( 252 , 251 , 247 , 1 )' );        -- Blanco

CREATE TABLE REGIONES(
ISIN VARCHAR(30) NOT NULL,
REGION VARCHAR(30) NOT NULL,
PORCENTAJE FLOAT NOT NULL,
PRIMARY KEY( ISIN , REGION ));

ALTER TABLE REGIONES
ADD CONSTRAINT region_indice FOREIGN KEY(ISIN) REFERENCES INDICES(ISIN) ON DELETE CASCADE,
ADD CONSTRAINT region_region FOREIGN KEY(REGION) REFERENCES REGION(REGION) ON DELETE CASCADE;

-- ----------------------------------------------
-- ------------------ SECTOR --------------------
-- ----------------------------------------------

CREATE TABLE SECTOR(
SECTOR VARCHAR(30) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(SECTOR));

INSERT INTO SECTOR( SECTOR , COLOR ) VALUES( 'Materiales Primas' , 'rgba( 19 , 6 , 120 , 1 )' );       -- AzulMarino
INSERT INTO SECTOR( SECTOR , COLOR ) VALUES( 'Consumo Ciclico' , 'rgba( 230 , 0 , 0 , 1 )' );        -- Rojo
INSERT INTO SECTOR( SECTOR , COLOR ) VALUES( 'Financiero y Asegurador' , 'rgba( 0 , 148 , 20 , 1 )' );     -- VerdeOscuro
INSERT INTO SECTOR( SECTOR , COLOR ) VALUES( 'Inmoviliario' , 'rgba( 120 , 3 , 138 , 1 )' );        -- Violeta
INSERT INTO SECTOR( SECTOR , COLOR ) VALUES( 'Consumo Defensivo' , 'rgba( 52 , 215 , 247 , 1 )' );       -- AzulCeleste
INSERT INTO SECTOR( SECTOR , COLOR ) VALUES( 'Salud' , 'rgba( 230 , 174 , 44 , 1 )' );        -- Naranja
INSERT INTO SECTOR( SECTOR , COLOR ) VALUES( 'Servivicios Publicos' , 'rgba( 230 , 227 , 44 , 1 )' );     -- Amarillo
INSERT INTO SECTOR( SECTOR , COLOR ) VALUES( 'Servivicios Comunicacion' , 'rgba( 148 , 142 , 132 , 1 )' );        -- Plateado
INSERT INTO SECTOR( SECTOR , COLOR ) VALUES( 'Energia' , 'rgba( 138 , 122 , 3 , 1 )' );       -- Dorado
INSERT INTO SECTOR( SECTOR , COLOR ) VALUES( 'Industria' , 'rgba( 252 , 251 , 247 , 1 )' );        -- Blanco
INSERT INTO SECTOR( SECTOR , COLOR ) VALUES( 'Tecnologia' , 'rgba( 79 , 179 , 155 , 1 )' );        -- VerdeAzulado

CREATE TABLE SECTORES(
ISIN VARCHAR(30) NOT NULL,
SECTOR VARCHAR(30) NOT NULL,
PORCENTAJE FLOAT NOT NULL,
PRIMARY KEY( ISIN , SECTOR ));

ALTER TABLE SECTORES
ADD CONSTRAINT sector_indice FOREIGN KEY(ISIN) REFERENCES INDICES(ISIN) ON DELETE CASCADE,
ADD CONSTRAINT sector_sector FOREIGN KEY(SECTOR) REFERENCES SECTOR(SECTOR) ON DELETE CASCADE;
   
-- ----------------------------------------------
-- -------------- CAPITALIZACION ----------------
-- ----------------------------------------------

CREATE TABLE CAPITALIZACION(
CAPITALIZACION VARCHAR(30) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(CAPITALIZACION));

INSERT INTO CAPITALIZACION( CAPITALIZACION , COLOR ) VALUES( 'Gigante' , 'rgba( 19 , 6 , 120 , 1 )' );       -- AzulMarino
INSERT INTO CAPITALIZACION( CAPITALIZACION , COLOR ) VALUES( 'Grande' , 'rgba( 230 , 0 , 0 , 1 )' );        -- Rojo
INSERT INTO CAPITALIZACION( CAPITALIZACION , COLOR ) VALUES( 'Mediano' , 'rgba( 0 , 148 , 20 , 1 )' );     -- VerdeOscuro
INSERT INTO CAPITALIZACION( CAPITALIZACION , COLOR ) VALUES( 'Pequeño' , 'rgba( 120 , 3 , 138 , 1 )' );        -- Violeta
INSERT INTO CAPITALIZACION( CAPITALIZACION , COLOR ) VALUES( 'Micro' , 'rgba( 52 , 215 , 247 , 1 )' );       -- AzulCeleste

CREATE TABLE CAPITALIZACIONES(
ISIN VARCHAR(30) NOT NULL,
CAPITALIZACION VARCHAR(30) NOT NULL,
PORCENTAJE FLOAT NOT NULL,
PRIMARY KEY( ISIN , CAPITALIZACION ));

ALTER TABLE CAPITALIZACIONES
ADD CONSTRAINT capitalizacion_indice FOREIGN KEY(ISIN) REFERENCES INDICES(ISIN) ON DELETE CASCADE,
ADD CONSTRAINT capitalizacion_capitalizacion FOREIGN KEY(CAPITALIZACION) REFERENCES CAPITALIZACION(CAPITALIZACION) ON DELETE CASCADE;

-- ----------------------------------------------
-- --------------- VENCIMIENTO ------------------
-- ----------------------------------------------

CREATE TABLE VENCIMIENTO(
VENCIMIENTO VARCHAR(30) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(VENCIMIENTO));

INSERT INTO VENCIMIENTO( VENCIMIENTO , COLOR ) VALUES( '1 a 3' , 'rgba( 19 , 6 , 120 , 1 )' );       -- AzulMarino
INSERT INTO VENCIMIENTO( VENCIMIENTO , COLOR ) VALUES( '3 a 5' , 'rgba( 230 , 0 , 0 , 1 )' );        -- Rojo
INSERT INTO VENCIMIENTO( VENCIMIENTO , COLOR ) VALUES( '5 a 7' , 'rgba( 0 , 148 , 20 , 1 )' );     -- VerdeOscuro
INSERT INTO VENCIMIENTO( VENCIMIENTO , COLOR ) VALUES( '7 a 10' , 'rgba( 120 , 3 , 138 , 1 )' );        -- Violeta
INSERT INTO VENCIMIENTO( VENCIMIENTO , COLOR ) VALUES( '10 a 15' , 'rgba( 52 , 215 , 247 , 1 )' );       -- AzulCeleste
INSERT INTO VENCIMIENTO( VENCIMIENTO , COLOR ) VALUES( '15 a 20' , 'rgba( 230 , 174 , 44 , 1 )' );        -- Naranja
INSERT INTO VENCIMIENTO( VENCIMIENTO , COLOR ) VALUES( '20 a 30' , 'rgba( 230 , 227 , 44 , 1 )' );     -- Amarillo
INSERT INTO VENCIMIENTO( VENCIMIENTO , COLOR ) VALUES( 'mas de 30' , 'rgba( 148 , 142 , 132 , 1 )' );        -- Plateado

CREATE TABLE VENCIMIENTOS(
ISIN VARCHAR(30) NOT NULL,
VENCIMIENTO VARCHAR(30) NOT NULL,
PORCENTAJE FLOAT NOT NULL,
PRIMARY KEY( ISIN , VENCIMIENTO ));

ALTER TABLE VENCIMIENTOS
ADD CONSTRAINT vencimiento_indice FOREIGN KEY(ISIN) REFERENCES INDICES(ISIN) ON DELETE CASCADE,
ADD CONSTRAINT vencimiento_vencimiento FOREIGN KEY(VENCIMIENTO) REFERENCES VENCIMIENTO(VENCIMIENTO) ON DELETE CASCADE;

-- ----------------------------------------------
-- ------------ CALIDAD CREDITICIA --------------
-- ----------------------------------------------

CREATE TABLE CALIDAD(
CALIDAD VARCHAR(30) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(CALIDAD));

INSERT INTO CALIDAD( CALIDAD , COLOR ) VALUES( 'AAA' , 'rgba( 19 , 6 , 120 , 1 )' );       -- AzulMarino
INSERT INTO CALIDAD( CALIDAD , COLOR ) VALUES( 'AA' , 'rgba( 230 , 0 , 0 , 1 )' );        -- Rojo
INSERT INTO CALIDAD( CALIDAD , COLOR ) VALUES( 'A' , 'rgba( 0 , 148 , 20 , 1 )' );     -- VerdeOscuro
INSERT INTO CALIDAD( CALIDAD , COLOR ) VALUES( 'B' , 'rgba( 120 , 3 , 138 , 1 )' );        -- Violeta
INSERT INTO CALIDAD( CALIDAD , COLOR ) VALUES( 'BB' , 'rgba( 52 , 215 , 247 , 1 )' );       -- AzulCeleste
INSERT INTO CALIDAD( CALIDAD , COLOR ) VALUES( 'BBB' , 'rgba( 230 , 174 , 44 , 1 )' );        -- Naranja
INSERT INTO CALIDAD( CALIDAD , COLOR ) VALUES( 'Ninguna' , 'rgba( 230 , 227 , 44 , 1 )' );     -- Amarillo

CREATE TABLE CALIDADES(
ISIN VARCHAR(30) NOT NULL,
CALIDAD VARCHAR(30) NOT NULL,
PORCENTAJE FLOAT NOT NULL,
PRIMARY KEY( ISIN , CALIDAD ));

ALTER TABLE CALIDADES
ADD CONSTRAINT calidad_indice FOREIGN KEY(ISIN) REFERENCES INDICES(ISIN) ON DELETE CASCADE,
ADD CONSTRAINT calidad_calidad FOREIGN KEY(CALIDAD) REFERENCES CALIDAD(CALIDAD) ON DELETE CASCADE;

-- ----------------------------------------------
-- -------------- ENTIDAD EMISORA ---------------
-- ----------------------------------------------

CREATE TABLE ENTIDAD(
ENTIDAD VARCHAR(30) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(ENTIDAD));

INSERT INTO ENTIDAD( ENTIDAD , COLOR ) VALUES( 'Institucional' , 'rgba( 19 , 6 , 120 , 1 )' );       -- AzulMarino
INSERT INTO ENTIDAD( ENTIDAD , COLOR ) VALUES( 'Gurnamental' , 'rgba( 230 , 0 , 0 , 1 )' );        -- Rojo

CREATE TABLE ENTIDADES(
ISIN VARCHAR(30) NOT NULL,
ENTIDAD VARCHAR(30) NOT NULL,
PORCENTAJE FLOAT NOT NULL,
PRIMARY KEY( ISIN , ENTIDAD ));

ALTER TABLE ENTIDADES
ADD CONSTRAINT entidad_indice FOREIGN KEY(ISIN) REFERENCES INDICES(ISIN) ON DELETE CASCADE,
ADD CONSTRAINT entidad_entidad FOREIGN KEY(ENTIDAD) REFERENCES ENTIDAD(ENTIDAD) ON DELETE CASCADE;

-- ----------------------------------------------
-- --------------- CLASIFICACION ----------------
-- ----------------------------------------------

CREATE TABLE CLASIFICACION(
CLASIFICACION VARCHAR(100) NOT NULL,
COLOR VARCHAR(50) NOT NULL,
PRIMARY KEY(CLASIFICACION));

INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Salario' , 'rgba( 255 , 255 , 255 , 1 )' ); -- Blanco
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Vivienda' , 'rgba( 0 , 12 , 173 , 1 )' ); -- Azulmarino
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Facturas' , 'rgba( 0 , 98 , 173 , 1 )' );  -- Azul
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Gastos' , 'rgba( 2 , 186 , 199 , 1 )' );   -- AzulCeleste
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Compras' , 'rgba( 2 , 199 , 166 , 1 )' ); -- AzulVerdoso
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Transporte' , 'rgba( 2 , 199 , 94 , 1 )' ); -- VerdeAzulado
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Viajes' , 'rgba( 7 , 181 , 42 , 1 )' );  -- VerdeEsmeralda
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Ocio' , 'rgba( 150 , 224 , 0  , 1 )' );   -- VerdeLima
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Caprichos' , 'rgba( 217 , 237 , 0 , 1 )' ); -- Amarillo
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Regalos' , 'rgba( 138 , 122 , 3 , 1 )' ); -- Dorado
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Banco' , 'rgba( 97 , 23 , 2 , 1 )' );  -- Marron
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Multas' , 'rgba( 179 , 116 , 0 , 1 )' );   -- Naranja
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Apuestas' , 'rgba( 179 , 36 , 0 , 1 )' ); -- Rojo
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Inversion' , 'rgba( 173 , 3 , 88 , 1 )' ); -- Fuxia
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Estudios' , 'rgba( 120 , 3 , 138 , 1 )' );   -- Violeta
INSERT INTO CLASIFICACION( CLASIFICACION , COLOR ) VALUES( 'Salud' , 'rgba( 119 , 0 , 237 , 1 )' ); -- VioletaOscuro

-- ----------------------------------------------
-- ------------ FINANZAS PERSONALES -------------
-- ----------------------------------------------

CREATE TABLE FINANZAS_PERSONALES(
FECHA DATE NOT NULL,
CLASIFICACION VARCHAR(30) NOT NULL, 
ASUNTO VARCHAR(30) NOT NULL,
DESCRIPCION VARCHAR(100) NOT NULL,
GASTO FLOAT NOT NULL,
INGRESO FLOAT NOT NULL,
PRIMARY KEY(FECHA,CLASIFICACION,ASUNTO,DESCRIPCION,GASTO,INGRESO));

ALTER TABLE FINANZAS_PERSONALES
ADD CONSTRAINT aportacion_finanzas FOREIGN KEY(CLASIFICACION) REFERENCES CLASIFICACION(CLASIFICACION) ON DELETE CASCADE;
