from fastapi import APIRouter

from .endpoints import brand, health, model

api_router = APIRouter()
api_router.include_router(brand.router, tags=["brands_crud"])
api_router.include_router(model.router, tags=["models_crud"])


api_router_unversioned = APIRouter()
api_router_unversioned.include_router(health.router, tags=["health_check"])
