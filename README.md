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
