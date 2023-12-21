# Ambientes

Con docker podemos manejar ambientes de desarrollo o sea crear un contenedor con nuestro proyecto en desarrollo y poder ir viendo los cambios en tiempo real ejecutado desde el contenedor

Para este ejemplo vamos a crear un ambiente de desarrollo con node y un script sencillo que suma dos numeros, la idea principal es usar nodemon para ver los cambios en tiempo real que realizamos sobre nuestro codigo

## Pasos a seguir

### Dockerfile

En el dockerfile crearemos nuestra imagen de node, con nuestro espacio de otrabajo y ambiente y todas las configuraciones necesaria

```Dockerfile
FROM node

# Crear directorio de trabajo
WORKDIR /home/app

# Copiar archivos de configuración (package.json y package-lock.json, si existe)
COPY package*.json ./

# Instalar dependencias del proyecto
RUN npm install

# Copiar el resto de los archivos de tu proyecto
COPY . .

# Copiar el script de inicio al directorio de trabajo y hacerlo ejecutable
RUN chmod +x ./run.sh

# Exponer el puerto en el que tu app se ejecuta
EXPOSE 3000

# El comando para iniciar tu aplicación (esto puede ser sobrescrito por docker-compose)
CMD ["./run.sh"]
```

### Docker-compese.yml

En este archivo crearemos el contenedor, lo llamaremos `holamundonodemon` 

```yml
version: "3.9"
services:
  holamundonodemon:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: holamundonodemon
    volumes:
      - .:/home/app
    ports:
      - "3000:3000"
    restart: always
    command: ["./run.sh"]
```

* restart: always: Indica que el contenedor siempre debe reiniciarse si se detiene. Si el contenedor se detiene por alguna razón, Docker intentará reiniciarlo automáticamente, esta linea es importante ya que en un ambiente de desarrollo podemos tener multiples errores que lleve a un stop de la aplicacion

* command : ["./run.sh"] : Ejecuta el archivo que previamente le dimos permiso de ejecucion, en este archivo guardaremos los scripts para la instalcion y ejecucion de nuestra aplicacion

### run.sh

```sh
#!/bin/bash

# Detener la ejecución si hay errores
set -e

# Instalar dependencias
echo "Installing NPM dependencies..."
npm install

# Ejecutar la aplicación en modo de desarrollo
echo "Starting development server..."
npm run dev

```