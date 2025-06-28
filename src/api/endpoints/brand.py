from fastapi import APIRouter

from config.settings import logger

router = APIRouter(prefix="/brands")


# GET    /brands
@router.get(
    "",
)
async def get_brands():
    """Get brands from database"""
    logger.info("Getting brands in progress... - STATUS: STARTED")
    return None


# GET    /brands/:id/models
@router.get(
    "/{item_id}/models",
)
async def get_models_brand(item_id: str):
    """Get model of brand from database"""
    logger.info("Getting brand in progress... - STATUS: STARTED")
    return None


# POST /brands
@router.post("")
async def add_brand():
    """Add a new brand to db."""
    return None


# POST /brands/:id/models
@router.post("/{item_id}/models")
async def add_model_brand(item_id: str):
    """Add a new model of brand to db."""
    return None
