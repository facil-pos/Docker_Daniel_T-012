#!/bin/bash

# Detener la ejecución si hay errores
set -e

# Instalar dependencias
echo "Installing NPM dependencies..."
npm install

# Ejecutar la aplicación en modo de desarrollo
echo "Starting development server..."
npm run dev
