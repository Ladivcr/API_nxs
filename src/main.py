from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.urls import api_router, api_router_unversioned
from config.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1}/openapi.json")


if settings.ENVIRONMENT in ["PRODUCTION"]:
    app.docs_url = ""
    app.redoc_url = ""
    app.openapi_url = ""

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1)
app.include_router(api_router_unversioned)
