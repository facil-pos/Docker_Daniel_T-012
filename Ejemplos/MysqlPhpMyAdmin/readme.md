# Mysql y PhpMyAdmin

En este ejemplo usaremos dos imagenes, una de mysql y otra de phpmyadmin, se podran comunicar entre ellos

Primero, crea un archivo [`docker-compose.yml`](docker-compose.yml) con el siguiente contenido:

```yaml
version: '3'

services:
  db:
    image: mysql:5.7
    volumes:
      - db_data:/var/lib/mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: userpassword
    networks:
      - backend

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    depends_on:
      - db
    environment:
      PMA_HOST: db
      PMA_PORT: 3306
      MYSQL_ROOT_PASSWORD: rootpassword
    ports:
      - "8080:80"
    networks:
      - backend
    restart: always

volumes:
  db_data:

networks:
  backend:
```

#### Explicación del Compose File

- **Servicios**: Define dos servicios: `db` (MySQL) y `phpmyadmin`.
- **Imagen de MySQL**: Usa `mysql:5.7`. Configura variables de entorno para la contraseña de root, la base de datos, el usuario y su contraseña.
- **Imagen de phpMyAdmin**: Usa `phpmyadmin/phpmyadmin`. Establece `PMA_HOST` como `db` para conectar con el servicio de MySQL. El puerto 8080 del host se mapea al puerto 80 del contenedor de phpMyAdmin.
- **Dependencias**: `phpmyadmin` usa `depends_on` para esperar a que el servicio `db` esté disponible.
- **Volúmenes**: `db_data` se utiliza para persistir los datos de MySQL.
- **Redes**: Se crea una red `backend` para la comunicación entre los contenedores.

#### Cómo Usarlo

1. **Ejecutar Docker Compose**: 
   En la misma carpeta donde está tu archivo `docker-compose.yml`, ejecuta:
   ```bash
   docker-compose up -d
   ```
   Esto iniciará los contenedores en el fondo (detached mode).

2. **Acceder a phpMyAdmin**: 
   Abre tu navegador y ve a `http://localhost:8080`. Deberías ver la interfaz de phpMyAdmin. Usa el usuario `root` y la contraseña `rootpassword` (o el usuario y contraseña que definiste) para ingresar.

3. **Gestionar Base de Datos**: 
   Dentro de phpMyAdmin, podrás gestionar la base de datos MySQL que se está ejecutando en el contenedor `db`.

#### Conclusiones

- **Separación de Servicios**: Cada servicio (MySQL y phpMyAdmin) se ejecuta en su propio contenedor, pero pueden comunicarse entre sí.
- **Persistencia de Datos**: Los datos de MySQL se almacenan en un volumen, lo que significa que no se perderán aunque el contenedor se detenga o elimine.
- **Facilidad de Uso**: Docker Compose simplifica la gestión de múltiples contenedores que necesitan trabajar juntos.
