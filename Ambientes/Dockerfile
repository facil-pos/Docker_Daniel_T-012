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
