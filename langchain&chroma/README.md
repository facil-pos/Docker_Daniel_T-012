# 🧮🗨️  ChromaDB y ChatGPT 

En este ejemplo dockerizamos una aplicacion de langchain y chromadb

## Pasos

### Prerequisite
1. Descarga e instala Docker y Git Clona el repositorio de Chroma con tu terminal

```bash
git clone https://github.com/chroma-core/chroma.git
```

2. Cambiamos al directorio de chroma

```bash
cd chroma
```

3. Ejecutamos docker compose 
```bash
docker-compose up -d --build
```

Este paso es necesario para correr el conteneder de docker y obtener su red

### Dockerfile

En este archivo creamos nuestra imagen basandonos en la imagen de [python:3.11.7-bullseye](https://hub.docker.com/layers/library/python/3.11.7-bullseye/images/sha256-e29978a317906ae8a88dd463b9cecbac7db92fa8e501525989d19fce23167217?context=explore)

```dockerfile
FROM python:3.11.7-bullseye

# Crear directorio de trabajo
WORKDIR /home/app

# Instalar las dependencias necesarias para compilar sqlite3
RUN apt-get update && \
    apt-get install -y wget gcc make libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Descargar y compilar sqlite3 desde el código fuente
ENV SQLITE_VERSION 3440200
RUN wget https://www.sqlite.org/2023/sqlite-autoconf-$SQLITE_VERSION.tar.gz && \
    tar xvfz sqlite-autoconf-$SQLITE_VERSION.tar.gz && \
    cd sqlite-autoconf-$SQLITE_VERSION && \
    ./configure && \
    make && \
    make install && \
    ldconfig && \
    cd .. && \
    rm -rf sqlite-autoconf-$SQLITE_VERSION* && \
    sqlite3 --version

# Copiar el resto de los archivos de tu proyecto
COPY . .

# Actualizar pip e instalar dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install pysqlite3-binary

# Exponer el puerto en el que tu app se ejecuta
EXPOSE 8501
```

#### Configuracion

A la hora de crear una imagen debemos de asegurarnos de instalar todos los paquetes y programas necesarios para el funcionamiento de nuestr aplicacion, la imagen base de [python:3.11.7-bullseye](https://hub.docker.com/layers/library/python/3.11.7-bullseye/images/sha256-e29978a317906ae8a88dd463b9cecbac7db92fa8e501525989d19fce23167217?context=explore) es una imagen de python que corre sobre linux teniendo esto en cuenta podemos instalar paquetes de linux de la misma forma que se haria desde una terminal.

* Cremos un espacio de trabajo
* Actualizamos paquetes e instalamos SQLite para el funcionamiento de chroma
* Copiamos todos nuestos archivos a nuestro espacio de trabajo
* Actualizamo pip e instalamos todas nuestras dependencias del proyecto
* Hacemos ejecutable el script de inicio

Ya tenemos nuestra imagen bien configurada

### Compose

```yml
version: "3.9"
services:
  langchainchroma:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: langchainchroma
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - .:/home/app
    ports:
      - "8501:8501"
    restart: always
    networks:
      - flowise_net
    command: ["./run.sh"]
  
networks:
    flowise_net:
        name: chroma_net
        external: true
```

Teniendo el contenedor de chromadb corriendo asosiamos su red a la de nuestro contenedor y ejecutamos nuestro archivo de inicializacion en este caso es el run.sh