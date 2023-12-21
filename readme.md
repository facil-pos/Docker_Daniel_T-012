# Docker

sistema de contenedores que corre sobre un kernel (En linux este kernel es el mismo, en windows tenemos que usar un sistema operativo de contenedor para usar el kernel del host)

## Sistema de imagen apilable

Los sistemas de archivos en docker se basan en imagenes apilables, por ejemplo tenemos una imagen base y sobre esta otras imagenes que dependen de la base (estas imagenes son inmutables), al final tenemos una base grabable donde sus datos seran destruidos al destruir el contenedor

### Recuros

  * [Introduccion](./Introduccion/readme.md) 
  * [Aprende Docker ahora! curso completo gratis desde cero! (youtube.com)](https://www.youtube.com/watch?v=4Dko5W96WHg)
  * [Ejemplos](./Ejemplos/)
  * [Introducción a los contenedores de Docker - Training | Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/intro-to-docker-containers/)
  * [Compilación de una aplicación web en contenedores con Docker - Training | Microsoft Learn](https://learn.microsoft.com/es-es/training/modules/intro-to-containers/)


## ¿Qué es un Dockerfile?

Un Dockerfile es un archivo de texto que contiene las instrucciones que se usan para compilar y ejecutar una imagen de Docker. Define los siguientes aspectos de la imagen:

- La imagen base o primaria que usamos para crear la nueva imagen.
- Los comandos para actualizar el sistema operativo base e instalar software adicional.
- Los artefactos de compilación que se incluirán, como una aplicación desarrollada.
- Los servicios que se van a exponer, como la configuración de red y del almacenamiento.
- El comando que se ejecutará cuando se inicie el contenedor.

### Recuros

  * [Introduccion](./Ejemplos/Imagen_Python/readme.md) 

# Contenedores

## Ciclos de vida

![Diagrama en el que se muestra el ciclo de vida de un contenedor y la transición entre las fases del ciclo de vida.](https://learn.microsoft.com/es-es/training/modules/intro-to-docker-containers/media/4-docker-container-lifecycle-2.png)


## Configuracion de almacenamiento

El almacenamiento en los contenedores es temporal, por esto se debe trabajar en la configuracion del mismo.

Los contenedores pueden usar dos opciones para conservar los datos. La primera consiste en hacer uso de *volúmenes* y la segunda es mediante *montajes de enlace*.

### Que es un volumen?

Un volumen se almacena en el sistema de archivos del host en una carpeta específica. Elija una carpeta donde sepa que los procesos que no son de Docker no van a modificar los datos.

Los volúmenes se almacenan en directorios en el sistema de archivos del host. Docker montará y administrará los volúmenes en el contenedor. Una vez montados, estos volúmenes están aislados de la máquina host.

Varios contenedores pueden usar simultáneamente los mismos volúmenes. Además, los volúmenes no se eliminan automáticamente cuando los contenedores dejan de usarlos.

### ¿Qué es un montaje de enlace?

Un montaje de enlace es conceptualmente lo mismo que un volumen; pero, en lugar de usar una carpeta específica, puede montar cualquier archivo o carpeta en el host. También espera que el host pueda cambiar el contenido de estos montajes. Igual que sucede con los volúmenes, un montaje de enlace se crea si lo monta y aún no existe en el host.

Los montajes de enlace tienen una funcionalidad limitada en comparación con los volúmenes y, aunque ofrecen más rendimiento, dependen de que el host tenga una estructura de carpetas específica.



## Configuracion de red

La configuración de red predeterminada de Docker hace que sea posible aislar los contenedores en el host de Docker. Esta característica permite crear y configurar aplicaciones que pueden comunicarse de forma segura entre sí.

La red en Docker es un componente crucial que define cómo los contenedores dentro de un mismo host Docker interactúan entre sí y con redes externas.

## Recursos

* [Aprende Docker ahora | conectandose a los contenedores](https://youtu.be/4Dko5W96WHg?t=2770&si=Q8LArChOHfbnkn4n)

### 1. Tipos de Redes en Docker

Docker proporciona varios controladores de red:

- **Bridge**: El controlador predeterminado, usado para crear una red privada interna dentro del host.
- **Host**: Para eliminar el aislamiento de red entre el contenedor y el host de Docker.
- **Overlay**: Usado para conectar múltiples contenedores de Docker en hosts diferentes.
- **Macvlan**: Permite asignar una dirección MAC a un contenedor para que parezca un dispositivo físico en la red.

### 2. Crear y Gestionar Redes

Para crear una red, usas el comando `docker network create`. Por ejemplo, para crear una red:

```bash
docker network create bridge mi_red_bridge
```

Para listar redes disponibles:

```bash
docker network ls
```

### 3. Conectar Contenedores a Redes

Al crear un contenedor, puedes conectarlo a una red específica usando el flag `--network`. Por ejemplo:

```bash
docker run -d --name mi_contenedor --network mi_red_bridge mi_imagen
```

### 4. Comunicación entre Contenedores

Los contenedores en la misma red pueden comunicarse entre sí usando sus nombres como hostnames. Por ejemplo, si tienes dos contenedores en la misma red `mi_red_bridge`, pueden comunicarse entre sí usando sus respectivos nombres.

### 5. Ejemplo Práctico

Imagina que quieres que dos contenedores, uno con una aplicación web y otro con una base de datos, se comuniquen:

1. **Crear la Red**: `docker network create --driver bridge mi_red_app`.

2. **Ejecutar Contenedores**: 
   - Contenedor de la Aplicación: `docker run -d --name app_container --network mi_red_app mi_imagen_app`.
   - Contenedor de la Base de Datos: `docker run -d --name db_container --network mi_red_app mi_imagen_db`.

3. **Comunicación**: El contenedor `app_container` puede conectarse a `db_container` usando el hostname `db_container`.

### 6. Exponiendo Puertos

Si necesitas que tu contenedor sea accesible desde fuera de tu host Docker, debes exponer puertos usando el flag `-p`. Por ejemplo:

```bash
docker run -d -p 80:80 --name mi_web_container mi_imagen_web
```

Esto mapea el puerto 80 del contenedor al puerto 80 del host.

### 7. Redes y Compose de Docker

En `docker-compose.yml`, puedes definir redes y especificar a qué red se conectará cada servicio. Docker Compose automáticamente establece una red por defecto donde todos los servicios pueden interactuar.

Vamos a crear un ejemplo práctico usando Docker Compose para configurar una imagen de MySQL que se comunique con una imagen de phpMyAdmin.

* [Ejemplos\MysqlPhpMyAdmin\readme.md](./Ejemplos/MysqlPhpMyAdmin/readme.md)

### Conclusiones

- **Aislamiento y Seguridad**: Las redes en Docker proporcionan aislamiento y seguridad entre contenedores.
- **Facilidad de Comunicación**: Facilitan la comunicación entre contenedores, tanto en el mismo host como en diferentes hosts.
- **Flexibilidad**: Ofrecen diversas opciones para diferentes escenarios, desde aplicaciones simples hasta despliegues complejos en múltiples hosts.

