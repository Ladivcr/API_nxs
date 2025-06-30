# Nexus API - Prueba Técnica

# Vista General
Proyecto realizado para llevar a cabo la prueba técnica de Nexus. Aquí encontrará el proceso para llevar a cabo el levantamiento del proyecto para validar su función. Así como observaciones, mejoras y decisiones técnicas tomadas durante el desarrollo.

# ¿Cómo correr este proyecto?
Para poder llevar a cabo los siguientes pasos, es necesario contar con las siguientes herramientas instaladas en el sistema:
- Docker
- Python >= 3.11, <4.0

## Modo Dockerizado y recomendado
1. **Lo primero que se debe de realizar es la clonación de este proyecto.**

> Por favor ejecuta los comandos en orden.

```Bash
# Creacion de una carpeta para trabajo
mkdir Work
cd Work
# Descarga del proyecto
git clone <URL DEL PROYECTO>
cd API_nxs
```
Una vez realizado lo anterior y posicionados en la carpeta del proyecto, procedemos con la preparación de docker.

2. **Preparación de Docker y levantamiento.**

**!** Antes de levantar el contenedor. Por favor revisa el archivo .env.txt en la ruta **src/config**.

Ya que es un archivo que se usa internamente en los contenedores. Lee lo que dice. Básicamente, eliminar la extensión. Notese que la variable de entorno no es crítica. Se ha añadido para facilitar la revisión a la persona que revise este proyecto. Pero en un entorno de producción, añadir las variables en el repositorio es una mala práctica.


```bash
# creación de la red útilizada en los contenedores
docker network create nexus-network

# levantar los contenedores
docker compose up --build
```
Si todo salio bien. Deberíamos de ver algo como lo siguiente:
![Ejecución de docker build docker build.](img_docs/docker_build.png)


3. **Creación de la base de datos.**

Lo anterior nos realizará el levantamiento de los tres contenedores.
- Nuestra API (local_fast_api).
- Nuestra base de datos en PostgreSQL (local_pgdb_admin)
- Nuestra interfaz para administrar postgresql (local_pgadmin4_container)
![Servicios levantados.](img_docs/docker_ps.png)


Ahora nos dirigimos a nuestro navegador y accedemos a la ruta: http://localhost:8888/ para acceder al panel de administración con pgadmin.
Las credenciales que hemos puesto en nuestro archivo docker:
![Login de pgadmin.](img_docs/pgadmin_1_login.png)

**username:** nexus@email
**password:** nexus

Una vez que hemos logrado acceder a PGAdmin, procedemos a crear la base de datos de la siguiente manera. Nos dirigimos a **register server** (click derecho sobre Servers -> Register -> Server) y registramos un nuevo servidor llamado: **_LOCAL_nexus_db_**

![Registro de nuevo server.](img_docs/pgadmin_2_creaciondb.jpg)

Posteriormente, en la pestaña de **Connection**, llenamos los datos con los que hemos especificado en el **docker compose** para realizar la conexión.
> **Host name/address = local_pgdb_admin** (que es el container name de nuestra bd en el archivo docker-compose)

> **Username y Password = toor** (que son los valores POSTGRES_USER y POSTGRES_PASSWORD en el archivo docmer-compose)

![Registro de conexión.](img_docs/pgadmin_3_registerdb.jpg)

Si todo ha salidos bien, debemos de ser capaces de de ver la base de datos **toor** entre las bases de datos.
![base de datos creada.](img_docs/pgadmin_4_db.jpg)

> La URL de las bases de datos en PostgreSQL se compone de la siguiente manera:
> **"postgresql://USERNAME:PASSWORD@localhost:5432/NAME_DB"**

> Sin embargo, como estamos utilizando contenedores, en lugar de localhost, debe ir el nombre del contenedor de la base de datos, quedando de la siguiente forma de acuerdo a nuestro contenedor: **"postgresql://toor:toor@db:5432/toor"**

Ahora, procedemos a crear las tablas en la base de datos.

4. **Creación de tablas y populación de la base de datos.**

Con los servicios corriendo. En otra terminal entraremos en el contenedor de fast api para ejecutar el script: **populate_script.py**

El script nos ayudará a crear las tablas y a insertar los datos del archivo **models.json**
para acceder ejecutamos el siguiente comando:
```bash
# Acceder al contenedor
docker exec -it local_fast_api /bin/bash

# NOTA local_fast_api hace referencia al nombre del contenedor. Podemos notarlo en la columna NAMES al ejecutar docker ps que nos muestra los contenedores corriendo.

# ejecutar script
python3 populate_script.py
```
Si todo salio bien, deberiamos ver en nuestra terminal algo similar a lo siguiente:
![base de datos creada.](img_docs/docker_script_populate.png)

¡Listo! Ya tenemos nuestro entorno levantado y listo para usarlo. Considera que los cambios que realices, para poder verlos reflejados será necesario que detengas los contenedores y vuelvas a ejecutar: `docker compose build --up`

Nota al margen. Las tablas que crea el script son las siguientes:
```sql

CREATE TABLE brands (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL
);


CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(70) UNIQUE NOT NULL,
    average_price DECIMAL(10,2),
    brand_id INTEGER,
    CONSTRAINT fk_brand FOREIGN KEY (brand_id) REFERENCES brands(id)
);
```
# ¿Cómo consumir los endpoints?

El entorno tiene seis endpoints:
- GET - **{{BASE_URL}}/health-check**
  Ideal para saber que la API esta andando y la conexión con la bd se ha realizado.
- GET - **{{BASE_URL}}/v1/brands**
  Listado de las marcas y su precio promedio.
- GET - **{{BASE_URL}}/v1/brands/:brand_name/models**
  Listado de todos los modelos relacionado a una marca.
- POST - **{{BASE_URL}}/v1/brands**
  Creación de nuevas marcas en la base de datos.
- POST - **{{BASE_URL}}/v1/brands/:brand_name/models**
  Creación de nuevos modelos relacionados a una marca.
- PUT - **{{BASE_URL}}/v1/models/:model_name**
  Actualización del average_price de un modelo.
- GET - **{{BASE_URL}}/v1/models?greater=400000&lower=380000**
  Listado de modelos con filtros por average_price

> **{{BASE_URL}}** = localhost:8000

> **:model_name, :brand_name** son variables (Path Variables). En Postman se usan de esa manera.

## GET: health-check
- URL: localhost:8000/health-check
- Body: N/A

## GET: brands
## GET: brands by models
## POST: brands
## POST: models by brand
## PUT: models
## GET: models



## Modo Local (Solo si tienes Python3.11)
Si quieres ejecutar este proyecto de manera local, para realizar pruebas o modificaciones. Hay preparativos que se deben realizar antes. Sigue los siguientes pasos en orden y al final tendrás el proyecto listo para probar de manera local.

### 1: Base de datos
Este proyecto hace uso de PostgreSQL y de su interfaz gráfica PGAdmin.
Si bien podemos manejar la base de datos desde la terminal. Es más comodo manejar los datos
mediante la IG.

1. **Instalación y configuración de PostgreSQL Y PGAdmin.**

Creamos el directorio postgres-docker para guardar nuestro archivo docker-compose.

```bash
# Creación del directorio y del archivo docker-compose.yml
mkdir postgres-docker
cd postgres-docker
touch docker-compose.yml
```

Una vez creado, lo llenamos con los siguientes servicios:
```bash
version: "3.8"
services:
  db:
    image: postgres
    container_name: local_pgdb
    restart: always
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: toor
      POSTGRES_PASSWORD: toor
    volumes:
      - local_pgdata:/var/lib/postgresql/data
  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin4_container
    restart: always
    ports:
      - "8888:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: nexus@email.com
      PGADMIN_DEFAULT_PASSWORD: nexus
    volumes:
      - pgadmin-data:/var/lib/pgadmin

volumes:
  local_pgdata:
  pgadmin-data:
```
Una vez que el archivo tiene el contenido, podemos ejecutar el archivo mediante el comando:
```bash
# Executar el archivo
docker compose up -d

# En otras versiones puede ser
docker-compose up -d
```
Si todo salio bien. Ahora nos dirigimos a nuestro navegador y accedemos a la ruta: http://localhost:8888/ y accedemos con las credenciales que hemos puesto en nuestro archivo.
![Login de pgadmin.](img_docs/pgadmin_1_login.png)

**username:** nexus@email
**password:** nexus

2. **Creación de la base de datos.**

Una vez que hemos logrado acceder a PGAdmin, procedemos a crear la base de datos de la siguiente manera. Nos dirigimos a register server (click derecho sobre Servers -> Register -> Server) y registramos un nuevo servidor llamado: **_LOCAL_nexus_db_**

![Registro de nuevo server.](img_docs/pgadmin_2_creaciondb.jpg)

Posteriormente, en la pestaña de **Connection**, llenamos los datos con los que hemos especificado en el **docker compose** para realizar la conexión.

Los datos útilizados del docker compose son: Username y Password (ambos son **toor**, referencia a tor browser).
![Registro de conexión.](img_docs/pgadmin_3_registerdb.jpg)

Si todo ha salidos bien, debemos de ser capaces de de ver la base de datos **toor** entre las bases de datos.
![base de datos creada.](img_docs/pgadmin_4_db.jpg)

> La URL de las bases de datos en PostgreSQL se compone de la siguiente manera:
> **"postgresql://USERNAME:PASSWORD@localhost:5432/NAME_DB"**

Ahora, procedemos a crear las tablas en la base de datos.

3. Creación y llenado de las tablas en la base de datos.

Pra ello vamos a ejecutar el script: **populate_script.py** que viene en el proyecto. El script se encargara de crear las tablas y llenarlas a partir del archivo **models.json**

```bash
# ejecutar script
python3 populate_script.py
```
Si todo salio bien, deberiamos ver en nuestra terminal mensajes similares a los de la siguiente imagen:
![base de datos creada.](img_docs/docker_script_populate.png)

Y también deberiamos de ser capaces de ver los datos en nuestra base de datos.
![Tablas creadas.](img_docs/pgadmin_7_tablascreadas.png)

> NOTA: Es posible que cuando revise los datos, se de cuenta que la cantidad no cuadra con la del archivo .json. Esto se debe a que hay datos duplicados que fueron omitidos. Ya que entraban en conflicto con algunas reglas de la prueba técnica, por ejemplo, que el nombre del modelo sea único.

Se adjunta un script con el que se pueden observar los duplicados y se adjunta una imagen con los modelos que se dúplican.

Script para revisar duplicados
```python

import json
from collections import Counter

# Cargar el JSON
with open("models.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Contar cuántas veces aparece cada name
name_counts = Counter(item["name"] for item in data)

# Mostrar solo los que están duplicados
duplicates = {name: count for name, count in name_counts.items() if count > 1}

print("🚨 Modelos duplicados por name:")
for name, count in duplicates.items():
    print(f"- {name} (aparece {count} veces)")
```
Modelos duplicados
![Script de dúplicados ejecutado con éxito.](img_docs/script_duplicados.jpg)


### 2: Descarga e instalación de dependencias del proyecto
En lo personal recomiendo usar un entorno virtual de python con la herramienta **Pyenv** ya que tienes acceso a versiones de python especificas (esteproyecto usa python3.11) pero también es posible usar los entornos virtuales que ya vienen por defecto con Python3.11

> Si vas a usar los entornos virtuales que vienen por defecto con python. Es imperativo que tengas python3.11 instalado en la computadora.


Hacer uso de un etorno virtual nos permitirá llevar mejor control de las librerias utilizadas en el proyecto y evitaremos instalar todas esas librerias en nuestro equipo.

Ejecute los comandos en el siguiente orden
```Python
# Creacion de una carpeta para trabajo
mkdir Work
cd Work
# Descarga del proyecto
git clone <URL DEL PROYECTO>
cd API_nxs

# Creamos nuestro entorno
python3 -m venv nombre_del_entorno
# Linux/Mac
source nombre_del_entorno/bin/activate
# Windows
nombre_del_entorno\Scripts\activate.bat
```
La consola deberá mostrar algo similar cuando el entorno este acrivo
```
(nombre_del_entorno) $
```
![Entorno creado.](img_docs/entorno.png)

Una vez que tenemos nuestro entorno, procedemos a instalar las dependencias del proyecto.
```python
pip install poetry

# Instalar dependencias
poetry install

export PYTHONPATH=src

# Correr el proyecto
uvicorn src.main:app --reload

# Otros comandos útiles
# (ejecutar cuando no este ejecutando uvicorn src.main:app --reload)

# Para correr ejecutar test
poetry run pytest

# Para ejecutar coverage
poetry run pytest --cov=src

# Para revisar el linting
pre-commit run --all-files
```
