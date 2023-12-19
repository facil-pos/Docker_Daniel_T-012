### ¿Qué es Docker?

Docker es una plataforma de contenedores que permite empaquetar aplicaciones y sus dependencias en un formato de contenedor. Estos contenedores son ligeros, portátiles, y proporcionan un entorno consistente para la aplicación, independientemente del entorno en el que se ejecuten. Docker facilita el desarrollo, despliegue y ejecución de aplicaciones usando contenedores.

### Comandos Más Usados en Docker

1. **docker run**: Crea y ejecuta un contenedor a partir de una imagen.
   - Ejemplo: `docker run -d -p 8080:80 nginx` ejecuta un contenedor de nginx en modo desacoplado y mapea el puerto 8080 del host al puerto 80 del contenedor.

2. **docker build**: Construye una imagen a partir de un Dockerfile.
   - Ejemplo: `docker build -t mi-imagen .` construye una imagen con el tag `mi-imagen` usando el Dockerfile en el directorio actual.

3. **docker ps**: Lista los contenedores en ejecución.
   - `docker ps -a` muestra todos los contenedores, incluso los detenidos.

4. **docker stop**: Detiene uno o más contenedores en ejecución.
   - Ejemplo: `docker stop mi_contenedor` detiene el contenedor llamado `mi_contenedor`.

5. **docker rm**: Elimina uno o más contenedores.
   - Ejemplo: `docker rm mi_contenedor` elimina el contenedor llamado `mi_contenedor`.

6. **docker images**: Muestra las imágenes disponibles en tu máquina.
   - Ejemplo: `docker images` lista todas las imágenes descargadas.

7. **docker rmi**: Elimina una o más imágenes.
   - Ejemplo: `docker rmi nginx` elimina la imagen de nginx.

8. **docker pull**: Descarga una imagen del registro de Docker.
   - Ejemplo: `docker pull ubuntu` descarga la última imagen de Ubuntu.

9. **docker push**: Sube una imagen a un registro de Docker.
   - Ejemplo: `docker push mi_usuario/mi-imagen` sube la imagen `mi-imagen` al registro con el nombre de usuario `mi_usuario`.

10. **docker logs**: Obtiene los logs de un contenedor.
    - Ejemplo: `docker logs mi_contenedor` muestra los logs del contenedor `mi_contenedor`.

11. **docker exec**: Ejecuta un comando en un contenedor en ejecución.
    - Ejemplo: `docker exec -it mi_contenedor bash` abre una sesión bash en el contenedor `mi_contenedor`.

12. **docker network**: Gestiona las redes de Docker.
    - Ejemplo: `docker network create mi_red` crea una nueva red llamada `mi_red`.

13. **docker volume**: Gestiona los volúmenes de Docker.
    - Ejemplo: `docker volume create mi_volumen` crea un nuevo volumen llamado `mi_volumen`.

Estos comandos son esenciales para el trabajo diario con Docker, desde la gestión de contenedores e imágenes hasta la configuración de redes y volúmenes para el almacenamiento persistente y la comunicación entre contenedores.