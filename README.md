# Nexus API technical test

# Overview
Lorem Ipsumn

# How to run this project?

## Local Mode
If you want to execute this project locally, to test or modify, there are some consideration before.

### Consideration 1: Database
To settup your database locally please follow the next steps:
> We going to use PostgreSQL for this API.
1. PostgresQL and pgadmin config

We can manage our database just by a terminal but we going to connect with a UX to manage our data better. To perfom the connection we going to leverage from docker compose.

```bash
# Create a directory and docker-compose.yml file within the directory
mkdir postgres-docker
cd postgres-docker
touch docker-compose.yml
```

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
```bash
# Execute the project
docker compose up -d
```
Now the use PGAdmin tool, open the browser and access http://localhost:8888/. Enter the username and password for PGAdmin.

pip install poetry

poetry init

export PYTHONPATH=src

Creación de la base de datos
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


> poetry run pytest

> poetry run pytest --cov=src
pre-commit run --all-files
