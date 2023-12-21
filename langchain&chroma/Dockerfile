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

# Hacemos ejecutable el script de inicio
RUN chmod +x ./run.sh

# Exponer el puerto en el que tu app se ejecuta
EXPOSE 8501
