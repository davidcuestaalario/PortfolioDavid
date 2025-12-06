# Usamos una imagen base que ya tiene Java 17 instalado (una versión ligera llamada Alpine)
FROM eclipse-temurin:17-jdk-alpine

# Creamos una carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo ejecutable (JAR) al contenedor
# NOTA: Esto asume que antes has ejecutado 'gradle build' para crear el jar.
# El asterisco * ayuda a no tener que saber el nombre exacto de la versión.
COPY build/libs/*.jar app.jar

# Le decimos al contenedor que, cuando arranque, ejecute este comando
ENTRYPOINT ["java", "-jar", "app.jar"]