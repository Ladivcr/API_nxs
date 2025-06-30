# Nexus API - Prueba Técnica

## Índice

- Vista General
- ¿Cómo correr este proyecto?
- - Modo Local (Ideal para nuevos miembros)
- - - 1. Base de datos
- - - 2. Populación de la base de datos
- - - 3. Descarga e instalación de dependencias del proyecto


# Vista General
Proyecto realizado para llevar a cabo la prueba técnica de Nexus. Aquí encontrará el proceso para llevar a cabo el levantamiento del proyecto para validar su función. Así como observaciones, mejoras y decisiones técnicas tomadas durante el desarrollo.

# ¿Cómo correr este proyecto?

## Modo Local
Para poder llevar a cabo los siguientes pasos, es necesario contar con las siguientes herramientas instaladas en el sistema:
- Docker
- Python 3.x

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

2. **Creación y llenado de la base de datos.**

Una vez que hemos logrado acceder a PGAdmin, procedemos a crear la base de datos de la siguiente manera. Nos dirigimos a register server y registramos un nuevo servidor llamado: **_Local_nexus_db_**
![Registro de nuevo server.](img_docs/pgadmin_2_creaciondb.jpg)

Posteriormente, en la pestaña de **Connection**, llenamos los datos con los que hemos especificado en el **docker compose** para realizar la conexión.

Los datos útilizados del docker compose son: Username y Password (ambos son **toor**, referencia a tor browser).
![Registro de conexión.](img_docs/pgadmin_3_registerdb.jpg)

Si todo ha salidos bien, debemos de ser capaces de de ver la base de datos **toor** entre las bases de datos.
![base de datos creada.](img_docs/pgadmin_4_db.jpg)

> La URL de las bases de datos en PostgreSQL se compone de la siguiente manera:
> "postgresql://USERNAME:PASSWORD@localhost:5432/NAME_DB"

Ahora, procedemos a crear las tablas en la base de datos. Para ello nos dirigimos al esquema público, presionamos click derecho y seleccionamos "Query Tool". Estos nos abrira un apartado para introducir las instrucciones para el creado de las tablas.

![Creación de tablas.](img_docs/pgadmin_6_queriesdb.png)

Ahí introducimos las siguientes instrucciones:

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
Si todo salio bien. Deberiamos de poder ver las tablas en su apartado correspondiente.
![Tablas creadas.](img_docs/pgadmin_7_tablascreadas.png)

### 2: Populación de la base de datos
Para realizar el llenado de la base de datos es necesario ejecutar el script: **populate_script.py** que a su vez, hace uso del archivo **models.json**

Antes de proceder a correr el script, es necesario actualizar la variable: **DB_URL**
Con la URL de la base de datos en el formato anteriormente expuesto: **"postgresql://USERNAME:PASSWORD@localhost:5432/DATABASE"**

El valor de la variable debe coincidir con el de tu archivo **.env** en **src/config/.env**

> El archivo se ha añadido por cuestiones de facilitación a la persona que revise. Pero en un entorno de producción y profesional, no se recomienda añadir el archivo de las variables de entorno al proyecto.

Una vez actualizada la variable, ejecutamos el script de la siguiente forma.
> Python3 populate_script.py

Si todo salio bien deberíamos poder ver un mensaje de confirmación.
![Script ejecutado con éxito.](img_docs/script_population.png)

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


### 3: Descarga e instalación de dependencias del proyecto
En lo personal recomiendo usar un entorno virtual de python con la herramienta **Pyenv** ya que tienes acceso a versiones de python especificas (esteproyecto usa python3.11) pero también es posible usar los entornos virtuales que ya vienen por defecto con Python3.x

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
python -m venv nombre_del_entorno
# Linux/Mac
source nombre_del_entorno/bin/activate
# Windows
nombre_del_entorno\Scripts\activate.bat
```
La consola deberá mostrar algo similar cuando el entorno este acrivo
```
(nombre_del_entorno) $
```

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
