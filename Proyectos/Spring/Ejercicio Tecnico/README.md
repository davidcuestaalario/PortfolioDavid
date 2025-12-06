# Ejercicio Técnico - vBote API

API RESTful desarrollada con Spring Boot para la gestión de usuarios y sesiones activas. Este proyecto ha sido diseñado priorizando la calidad del código, la seguridad y la escalabilidad, cumpliendo con todos los requerimientos funcionales y técnicos propuestos.

## 🚀 Tecnologías Utilizadas

* **Java 17**: Lenguaje principal (LTS).
* **Spring Boot 3**: Framework para el desarrollo ágil de la API.
* **Spring Data JPA (Hibernate)**: Para la persistencia y ORM.
* **H2 Database**: Base de datos en memoria para desarrollo y pruebas rápidas.
* **Lombok**: Para reducir el código repetitivo (Boilerplate) y mejorar la legibilidad.
* **Gradle**: Gestor de dependencias y automatización de construcción.
* **JUnit 5 & Mockito**: Stack de pruebas unitarias.
* **Docker**: Contenerización de la aplicación y base de datos.

---

## 🛠️ Arquitectura y Decisiones de Diseño

Se ha implementado una **Arquitectura en Capas** estricta para garantizar la separación de responsabilidades:

1.  **Controladores (REST Layer)**: Manejan las peticiones HTTP y respuestas. No contienen lógica de negocio.
2.  **DTOs (Data Transfer Objects)**: Desacoplan la API del modelo de base de datos, ocultando datos sensibles (passwords) y permitiendo contratos de API limpios.
3.  **Mappers**: Componentes dedicados a la transformación bidireccional `Entidad <-> DTO`.
4.  **Servicios (Business Layer)**: Contienen toda la lógica de negocio y gestión de transacciones (`@Transactional`).
5.  **Repositorios (Data Access)**: Interfaces de Spring Data JPA para la persistencia.

### 🛡️ Seguridad y Filtros (Requerimientos Técnicos)
Se han implementado filtros nativos (`OncePerRequestFilter`) para gestionar la seguridad y auditoría sin depender de frameworks externos pesados:

* **AuthenticationFilter**: Intercepta endpoints protegidos y valida el token `Bearer` contra la base de datos y el estado de la sesión activa.
* **RequestLogFilter**: Auditoría de cada petición entrante (Timestamp, Método, Endpoint) y su tiempo de ejecución.
* **RateLimitFilter (Punto Extra)**: Protección contra ataques de denegación de servicio (DoS) limitando a **10 peticiones por minuto por IP** utilizando almacenamiento en memoria (`ConcurrentHashMap`).

---

## 📊 Calidad y Testing

Se ha priorizado la robustez del código mediante una estrategia de pruebas unitarias sólidas.

* **Herramientas**: JUnit 5, Mockito y EclEmma.
* **Cobertura de Código**:
    * **Servicios Core (`UserService`, `SessionService`)**: **>90%** de cobertura, verificando "Happy Paths", casos de error y cobertura de ramas (Branch Coverage).
    * **Cobertura Global**: **~70%** del proyecto.
* **Estrategia**: Tests aislados que simulan (Mock) las dependencias de repositorio y mappers para verificar puramente la lógica de negocio.

---

## ⚙️ Configuración y Ejecución

### Prerrequisitos
* Java JDK 17 instalado.
* Gradle (o usar el wrapper incluido `./gradlew`).

### Opción A: Ejecución Local (H2)

1.  **Clonar** el repositorio.
2.  **Ejecutar** desde la terminal en la raíz del proyecto:
    * **Windows**:
        ```bash
        ./gradlew bootRun
        ```
    * **Linux/Mac**:
        ```bash
        ./gradlew bootRun
        ```
3.  **Acceso**: La API estará disponible en `http://localhost:8080`.

### Opción B: Despliegue con Docker (Punto Extra)

El proyecto incluye configuración para desplegar la API conectada automáticamente a una base de datos **PostgreSQL**.

* **Dockerfile**: Imagen basada en OpenJDK 17 Alpine.
* **docker-compose.yml**: Orquestación de servicios (`app` + `db`).

**Pasos para desplegar:**

1.  Generar el artefacto JAR:
    ```bash
    ./gradlew bootJar
    ```
2.  Construir y levantar los contenedores:
    ```bash
    docker-compose up --build
    ```

---

## 📚 Documentación de la API

### 1. Autenticación (Público)
* **Login**: `POST /api/sessions/login`
    * Body: `{ "username": "admin", "password": "admin123" }`
    * Retorna: `{ "token": "uuid-token...", ... }`

### 2. Operaciones de Usuarios
🔒 *Requiere Header:* `Authorization: Bearer <TOKEN>`

* **Listar Usuarios**: `GET /api/users`
    * Filtros opcionales: `?role=ADMIN` o `?username=texto`
* **Crear Usuario**: `POST /api/users`
* **Obtener por ID**: `GET /api/users/{id}`
* **Actualizar Usuario**: `PUT /api/users/{id}`
* **Bloquear Usuario**: `PATCH /api/users/{id}/block`

### 3. Operaciones de Sesión
🔒 *Requiere Header:* `Authorization: Bearer <TOKEN>`

* **Listar mis sesiones**: `GET /api/sessions`
* **Logout (Actual)**: `POST /api/sessions/logout?token=<TOKEN>`
* **Logout (Masivo)**: `POST /api/sessions/logout-all?userId=<ID>`

---

## 🧪 Datos de Prueba

Al iniciar la aplicación (modo local H2), se precargan los siguientes usuarios para facilitar las pruebas:

| Usuario | Contraseña | Rol | Estado |
| :--- | :--- | :--- | :--- |
| **admin** | `admin123` | ADMIN | ✅ Activo |
| **usuario1** | `user123` | USER | ✅ Activo |
| **noEsAdmin** | `admin123` | USER | ✅ Activo |
| **adminBloqueado**| `admin123` | ADMIN | ❌ Bloqueado |
| **usuarioBloqueado**| `user123` | USER | ❌ Bloqueado |

---
*Entregable para Ejercicio Técnico - vBote*