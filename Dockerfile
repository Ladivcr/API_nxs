FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema y herramientas para el entorno virtual
RUN apt-get update && apt-get install -y \
    python3-venv \
    && pip install -U poetry gunicorn uvicorn[standard]

WORKDIR /app

# Crear un entorno virtual en la carpeta de la aplicación
RUN python3 -m venv /app/venv

# Activar el entorno virtual y usarlo para instalar las dependencias
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copiar archivos de configuración de poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/

# Versión 1.7.0 que es compatible con poetry 1.8.x
RUN poetry self add "poetry-plugin-export==1.7.0"

# Exportar las dependencias a requirements.txt y luego instalar
RUN cd /tmp && poetry export -f requirements.txt --output /app/requirements.txt --without-hashes --with dev \
    && pip install --no-warn-script-location --disable-pip-version-check --no-cache-dir -r /app/requirements.txt

# Copiar el código fuente de la aplicación
COPY ./src /app

# Exponer el puerto 9000 para el contenedor
EXPOSE 8000

# Usar uvicorn dentro del entorno virtual para ejecutar la app FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]