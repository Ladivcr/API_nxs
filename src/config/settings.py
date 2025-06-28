import sys
from typing import List, Optional

from dotenv import dotenv_values
from loguru import logger  # NOQA
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


env_file = dotenv_values("src/config/.env")


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
