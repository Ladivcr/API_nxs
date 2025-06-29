from fastapi import APIRouter

from config.settings import logger
from services.brands import brand_service
router = APIRouter(prefix="/brands")


# GET    /brands
@router.get(
    "",
)
async def get_brands():
    """List all brands from database"""
    logger.info("Getting brands in progress... - STATUS: STARTED")
    response = brand_service.list_brands()
    logger.success("Getting brands finished - STATUS: OK")
    return response


# GET    /brands/:id/models
@router.get(
    "/{brand}/models",
)
async def get_models_brand(brand: str):
    """Get model of brand from database
    
    Args: 
        brand (str): brand name.
    
    """
    logger.info("Getting brand in progress... - STATUS: STARTED")
    response = brand_service.list_brands(brand_name=brand)
    logger.success("Getting brand finished - STATUS: OK")
    return response
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
