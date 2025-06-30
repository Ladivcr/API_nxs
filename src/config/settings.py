import sys
from typing import List, Optional

from dotenv import dotenv_values
from loguru import logger  # NOQA
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
import os


LOCAL_ENV_PATH = "src/config/.env"
DOCKER_ENV_PATH = "config/.env"

env_path = LOCAL_ENV_PATH if os.path.exists(LOCAL_ENV_PATH) else DOCKER_ENV_PATH
env_file = dotenv_values(env_path)


class BaseConfig(BaseSettings):
    """Global configurations."""

    PROJECT_NAME: Optional[str] = "Nexus-API"
    API_V1: Optional[str] = "/v1"
    BACKEND_CORS_ORIGINS: Optional[List[AnyHttpUrl]] = []
    ENVIRONMENT: str = env_file["ENVIRONMENT"]
    DATABASE_URL: str = env_file[f"{ENVIRONMENT}_DATABASE_URL"]


logger.remove()  # Elimina cualquier configuración previa por defecto
logger.add(sys.stderr, level="DEBUG")  # Imprime logs en consola
settings = BaseConfig()
