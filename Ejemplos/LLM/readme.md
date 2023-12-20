# Aplicacion de llm

Para este ejemplo desplegaremos un contenedor de [Flowise](https://github.com/FlowiseAI/Flowise), Esta es una plataforma no-code de codigo abierto con licencia apache2 y basada en langchain que nos permite crear aplicaciones llm y chatbot sin programa

Podemos crear una imagen por medio del dockerfile como se muestra en su documentacion o compen crear el contendor con docker compose 

## Dockerfile

```dockerfile
FROM node:18-alpine

USER root

RUN apk add --no-cache git
RUN apk add --no-cache python3 py3-pip make g++
# needed for pdfjs-dist
RUN apk add --no-cache build-base cairo-dev pango-dev

# Install Chromium
RUN apk add --no-cache chromium

ENV PUPPETEER_SKIP_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# You can install a specific version like: flowise@1.0.0
RUN npm install -g flowise

WORKDIR /data

CMD "flowise
```
Este `Dockerfile` define cómo se construirá una imagen Docker para un entorno de Node.js con herramientas y dependencias específicas, incluyendo la capacidad de ejecutar Chromium y una biblioteca llamada `flowise`. Aquí te explico cada línea:

1. **`FROM node:18-alpine`**: Esta línea establece la imagen base como `node:18-alpine`. `node:18` se refiere a la versión 18 de Node.js. `alpine` es una distribución ligera de Linux, conocida por su simplicidad y tamaño reducido.

2. **`USER root`**: Cambia el usuario a `root`. Esto es necesario para instalar paquetes y realizar configuraciones que requieren permisos de administrador.

3. **`RUN apk add --no-cache git`**: Instala `git` en la imagen. `apk` es el gestor de paquetes de Alpine Linux. La opción `--no-cache` significa que los archivos temporales usados durante la instalación no se almacenarán, reduciendo el tamaño de la imagen.

4. **`RUN apk add --no-cache python3 py3-pip make g++`**: Instala Python 3, `pip` (gestor de paquetes de Python), `make` y `g++` (un compilador de C++) en la imagen.

5. **`RUN apk add --no-cache build-base cairo-dev pango-dev`**: Instala `build-base` (un grupo de paquetes que incluyen herramientas esenciales para la compilación), `cairo-dev` (una biblioteca para gráficos vectoriales) y `pango-dev` (una biblioteca para el diseño y renderizado de texto), necesarios para `pdfjs-dist`.

6. **`RUN apk add --no-cache chromium`**: Instala Chromium, un navegador web de código abierto, en la imagen. Esto es útil para tareas que requieren un navegador, como pruebas automatizadas o scraping web.

7. **`ENV PUPPETEER_SKIP_DOWNLOAD=true`**: Establece una variable de entorno para evitar que Puppeteer (una biblioteca de Node para controlar navegadores basados en Chromium) descargue su propia versión de Chromium, ya que se está utilizando la versión instalada a través de `apk`.

8. **`ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser`**: Indica a Puppeteer el camino al ejecutable de Chromium que se acaba de instalar.

9. **`RUN npm install -g flowise`**: Instala globalmente `flowise` usando `npm`. `flowise` es probablemente un paquete de npm, aunque no se proporciona detalle sobre su función.

10. **`WORKDIR /data`**: Establece el directorio de trabajo en `/data`. Cualquier comando que se ejecute después de esta línea se ejecutará en este directorio.

11. **`CMD "flowise"`**: Define el comando que se ejecutará cuando se inicie un contenedor basado en esta imagen. En este caso, ejecuta `flowise`.

En resumen, este `Dockerfile` crea una imagen Docker para un entorno de Node.js preparado para tareas de desarrollo y automatización que requieren Chromium, con la capacidad de ejecutar el comando `flowise`.


## docker-compose.yml

```yml
version: '3.1'

services:
    flowise:
        image: flowiseai/flowise
        restart: always
        environment:
            - PORT=${PORT}
            - FLOWISE_USERNAME=${FLOWISE_USERNAME}
            - FLOWISE_PASSWORD=${FLOWISE_PASSWORD}
            - DEBUG=${DEBUG}
            - DATABASE_PATH=${DATABASE_PATH}
            - DATABASE_TYPE=${DATABASE_TYPE}
            - DATABASE_PORT=${DATABASE_PORT}
            - DATABASE_HOST=${DATABASE_HOST}
            - DATABASE_NAME=${DATABASE_NAME}
            - DATABASE_USER=${DATABASE_USER}
            - DATABASE_PASSWORD=${DATABASE_PASSWORD}
            - APIKEY_PATH=${APIKEY_PATH}
            - SECRETKEY_PATH=${SECRETKEY_PATH}
            - FLOWISE_SECRETKEY_OVERWRITE=${FLOWISE_SECRETKEY_OVERWRITE}
            - LOG_LEVEL=${LOG_LEVEL}
            - LOG_PATH=${LOG_PATH}
        ports:
            - '${PORT}:${PORT}'
        volumes:
            - ~/.flowise:/root/.flowise
        command: /bin/sh -c "sleep 3; flowise start"
```

Este `docker-compose.yml` es un archivo de configuración para Docker Compose, una herramienta utilizada para definir y ejecutar aplicaciones Docker multi-contenedor. Vamos a desglosar cada parte del archivo para entender su función:

### Estructura General

- **`version: '3.1'`**: Indica la versión de la sintaxis de Docker Compose utilizada. La versión `3.1` soporta varias características avanzadas y es adecuada para la mayoría de los usos modernos.

### Servicios

- **`services`**: Bajo este elemento, defines los contenedores (servicios) que quieres ejecutar. Aquí, solo se define un servicio llamado `flowise`.

#### Configuración del Servicio `flowise`

- **`image: flowiseai/flowise`**: Indica que el servicio `flowise` utilizará la imagen `flowiseai/flowise`. 

- **`restart: always`**: Configura el servicio para que se reinicie automáticamente si se detiene. Por ejemplo, se reiniciará en caso de fallo o si el servidor Docker se reinicia.

- **`environment`**: Define variables de entorno para el servicio. Estas variables son pasadas al contenedor y pueden ser utilizadas por la aplicación dentro del contenedor. Aquí se utilizan variables de entorno para configurar el puerto, credenciales, configuración de la base de datos, claves de API, niveles de registro (log), etc. Los valores de estas variables parecen ser tomados de variables de entorno del host o un archivo `.env`.

- **`ports`**: Mapea los puertos entre el contenedor y el host. Aquí, el puerto especificado en la variable `${PORT}` del host se mapea al mismo puerto dentro del contenedor, permitiendo el acceso a la aplicación desde fuera del contenedor.

- **`volumes`**: Monta volúmenes para persistencia de datos. En este caso, monta el directorio `.flowise` del usuario actual en el host (`~/.flowise`) al directorio `/root/.flowise` en el contenedor. Esto es útil para mantener datos o configuraciones entre reinicios del contenedor.

- **`command`**: Define un comando personalizado que se ejecutará al iniciar el contenedor. Aquí, espera 3 segundos (`sleep 3`) antes de ejecutar `flowise start`, probablemente para asegurarse de que otros servicios (como bases de datos) estén listos.

### Resumen

Este archivo `docker-compose.yml` está configurado para ejecutar un único servicio (`flowise`) en un contenedor Docker. Utiliza una imagen predefinida, configura el entorno, expone un puerto, persiste datos mediante volúmenes y ejecuta un comando personalizado al iniciar. Este tipo de configuración es típico para aplicaciones que necesitan una configuración específica del entorno y dependen de la persistencia de datos y la exposición de servicios a través de puertos.

## Ejecucion

En este caso ejecutaremos el docker-compese.yml para esto tenemos que ejecuetar el comando `docker compose up`, luego de que termine la ejecucion la aplicacion estara corriendo en el puerto 3000