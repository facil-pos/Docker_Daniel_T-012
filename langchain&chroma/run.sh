#!/bin/bash

# Detener la ejecución si hay errores
set -e

sleep 3;
# Ejecutar la aplicación en modo de desarrollo
echo "Starting server..."
streamlit run app.py
