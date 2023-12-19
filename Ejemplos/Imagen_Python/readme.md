# Dockerfile

Un Dockerfile es un archivo de texto que contiene una serie de instrucciones utilizadas para crear una imagen Docker. Cada instrucción en el Dockerfile agrega una capa a la imagen, y cada capa representa una parte de la imagen Docker que se está construyendo. Esta imagen final puede ser utilizada para ejecutar contenedores.

## Componentes Clave de un Dockerfile

* FROM: Define la imagen base desde la cual se construirá la imagen. Por ejemplo, FROM ubuntu:20.04.

* RUN: Ejecuta comandos en la capa superior de la imagen actual. Por ejemplo, RUN apt-get update.

* CMD: Proporciona un comando y argumentos para ejecutar cuando el contenedor inicia. Sólo puede haber una instrucción CMD; si hay más de una, solo la última tendrá efecto.

* EXPOSE: Informa a Docker que el contenedor escucha en los puertos especificados en tiempo de ejecución. Por ejemplo, EXPOSE 80.

* ENV: Establece variables de entorno. Por ejemplo, ENV MY_VARIABLE value.

* ADD y COPY: Agregan archivos desde tu directorio local al sistema de archivos del contenedor.

* ENTRYPOINT: Configura el contenedor para que se ejecute como un ejecutable.

* WORKDIR: Establece el directorio de trabajo para las instrucciones RUN, CMD, ENTRYPOINT, COPY y ADD que siguen en el Dockerfile.

## Ejemplo Práctico de un Dockerfile

Supongamos que queremos crear una imagen Docker que ejecute una aplicación web básica escrita en Python. La aplicación requiere un entorno con Python y algunas dependencias.

Explicación:

* FROM python: Comienza con una imagen Python completa.

* WORKDIR /app: Establece /app como directorio de trabajo.

* COPY: Copia requirements.txt y app.py (archivo de la aplicación) al contenedor.

* RUN pip install: Instala las dependencias definidas en requirements.txt.

* EXPOSE 5000: Informa que el contenedor estará escuchando en el puerto 5000.

* CMD ["python", "app.py"]: Define el comando para ejecutar la aplicación.

## Construir y Ejecutar la Imagen:

* Construir la imagen: docker build -t mi-flask-app .

* Ejecutar un contenedor de la imagen: docker run -p 5000:5000 mi-flask-app

Este Dockerfile es un ejemplo de cómo puedes empacar una aplicación Python en una imagen Docker. Puedes modificarlo según las necesidades específicas de tu aplicación.