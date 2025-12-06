# Ejercicio Técnico - vBote API

API RESTful desarrollada con Spring Boot para la gestión de usuarios y sesiones activas. Este proyecto implementa persistencia de datos, seguridad basada en tokens y filtros de auditoría.

## 🚀 Tecnologías Utilizadas

* **Java 17**: Lenguaje principal (Requisito Java 8+).
* **Spring Boot 3**: Framework para el desarrollo ágil de la API.
* **Spring Data JPA (Hibernate)**: Para la persistencia y ORM.
* **H2 Database**: Base de datos en memoria para desarrollo y pruebas.
* **Lombok**: Para reducir el código repetitivo (Boilerplate) y mejorar la legibilidad.
* **Gradle**: Gestor de dependencias y automatización de construcción.
* **Mockito**: Simulador de componentes para las pruebas unitarias

## 🛠️ Decisiones de Diseño

Para garantizar la calidad del código, escalabilidad y mantenimiento, se ha optado por una **Arquitectura en Capas**:

1.  **Modelo de Dominio (Entity)**: Clases `User` y `Session` que reflejan fielmente las tablas de base de datos.
2.  **DTOs (Data Transfer Objects)**: Se han separado los objetos de transferencia (`UserRequestDTO`, `UserResponseDTO`) de las entidades para:
    * Ocultar datos sensibles (como passwords y IDs internos).
    * Desacoplar la API de la estructura de base de datos.
3.  **Mappers**: Componentes dedicados a la transformación Entidad <-> DTO.
4.  **Servicios**: Capa transaccional (`@Transactional`) donde reside toda la lógica de negocio.
5.  **Controladores**: Capa REST encargada solo de recibir peticiones y devolver respuestas HTTP adecuadas.

### Seguridad y Requerimientos Técnicos
* **Filtros (Filters)**: Se han implementado filtros nativos (`OncePerRequestFilter`) en lugar de interceptores para cumplir con los requisitos técnicos:
    * `RequestLogFilter`: Auditoría de cada petición (Timestamp, Método, Endpoint).
    * `AuthenticationFilter`: Validación de seguridad. Intercepta las peticiones y verifica la validez del token `Bearer` contra la base de datos.
* **Base de Datos Volátil**: Se utiliza H2 con un script `data.sql` que precarga usuarios de prueba al iniciar la aplicación.

## ⚙️ Configuración y Ejecución

### Prerrequisitos
* JDK 17 instalado.
* Maven (o usar el wrapper incluido `mvnw`).

### Pasos para correr el proyecto

1.  **Clonar/Descargar** el repositorio.
2.  **Compilar y Ejecutar**:
    Desde la raíz del proyecto, ejecutar:
	* En Windows:
        ```bash
        ./gradlew bootRun
        ```
    * En Linux/Mac:
        ```bash
        ./gradlew bootRun
        ```
    O importar como proyecto Maven en **Spring Tool Suite (STS)** / Eclipse y ejecutar como *Spring Boot App*.

3.  **Acceso**: La API arrancará en `http://localhost:8080`.

### Dockerización

El proyecto incluye configuración para desplegar la API junto con una base de datos PostgreSQL contenerizada.

**Archivos incluidos**
* **Dockerfile**: Empaqueta la aplicación Spring Boot en una imagen OpenJDK 17 Alpine.
* **docker-compose.yml**: Orquesta dos servicios:
    1. `app`: La API REST (Puerto 8080).
    2. `db`: Base de datos PostgreSQL 15 (Puerto 5432).

**Comandos de despliegue**

* Generar el artefacto JAR:
   ```bash
   ./gradlew bootJar
   
   
   
   
   
      
## 📚 Documentación de la API

### Autenticación
Para acceder a los endpoints protegidos, primero debe obtener un token.

* **Login**: `POST /api/sessions/login`
    * Body: `{ "username": "admin", "password": "admin123" }`
    * Retorna: `{ "token": "uuid-token-...", ... }`

### Usuarios (Requiere Header: `Authorization: Bearer <TOKEN>`)

* **Listar Usuarios**: `GET /api/users`
    * Filtros opcionales: `?role=ADMIN` o `?username=text`
* **Crear Usuario**: `POST /api/users`
* **Obtener por ID**: `GET /api/users/{id}`
* **Actualizar Usuario**: `PUT /api/users/{id}`
* **Bloquear Usuario**: `PATCH /api/users/{id}/block`

### Sesiones (Requiere Header: `Authorization: Bearer <TOKEN>`)

* **Listar activas**: `GET /api/sessions`
* **Logout (Actual)**: `POST /api/sessions/logout?token=<TOKEN>`
* **Logout (Masivo)**: `POST /api/sessions/logout-all?userId=<ID>`

## 📚 Características Adicionales (Puntos Extra)

Además de los requerimientos funcionales, se han implementado mejoras técnicas para robustecer la aplicación:

### Seguridad Avanzada (Autenticación/Autorización)
Se ha implementado un sistema de seguridad personalizado mediante Tokens, superando el requisito de un mock simple.
* **AuthenticationFilter**: Intercepta todas las peticiones a endpoints protegidos.
* **Validación**: Verifica la presencia y validez del token `Bearer` contra la base de datos y el estado de la sesión.
* **Protección**: Impide el acceso a operaciones sensibles (CRUD de usuarios, Logout) sin credenciales válidas.

### Protección contra DoS (Rate Limiting)
Implementación de un `RateLimitFilter` en memoria para proteger la API de abusos.
* **Límite**: 10 peticiones por minuto por dirección IP.
* **Respuesta**: Devuelve `429 Too Many Requests` si se excede el límite.
* **Tecnología**: Uso de `ConcurrentHashMap` para gestión eficiente en entornos concurrentes.

### Calidad y Testing
Se han incluido pruebas unitarias para garantizar la fiabilidad de la lógica de negocio.
* **Stack**: JUnit 5 + Mockito.
* **Cobertura**: Tests aislados para `UserService` simulando el comportamiento del repositorio y mappers, verificando casos de éxito y mapeo de datos.


## 🧪 Datos de Prueba (H2)

La aplicación inicia con los siguientes usuarios precargados:

# Usuarios de ejemplo en `T_USER`

 👑 ADMINS

| Usuario          | Contraseña | Rol   | Bloqueado | Fecha de creación   |
|------------------|------------|-------|-----------|---------------------|
| admin            | admin123   | ADMIN | false     | CURRENT_TIMESTAMP   |
| adminBloqueado   | admin123   | ADMIN | true      | CURRENT_TIMESTAMP   |

 👤 NO ADMINS

| Usuario          | Contraseña | Rol   | Bloqueado | Fecha de creación   |
|------------------|------------|-------|-----------|---------------------|
| usuario1         | user123    | USER  | false     | CURRENT_TIMESTAMP   |
| noEsAdmin        | admin123   | USER  | false     | CURRENT_TIMESTAMP   |
| usuarioBloqueado | user123    | USER  | false     | CURRENT_TIMESTAMP   |

---
*Entregable para Ejercicio Técnico - vBote*