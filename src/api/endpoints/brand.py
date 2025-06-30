from fastapi import APIRouter

from config.settings import logger
from services.brands import brand_service
from services.models import model_service
from schemas.brands import BrandCreateSchema
from schemas.models import CreateModelSchema
import json
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/brands")


# GET    /brands [OK]
@router.get(
    "",
)
async def get_brands():
    """List all brands from database"""
    logger.info("Getting brands in progress... - STATUS: STARTED")
    response = brand_service.list_brands()
    logger.success("Getting brands finished - STATUS: OK")
    return response


# GET    /brands/:id/models [OK]
@router.get(
    "/{brand}/models",
)
async def get_models_brand(brand: str):
    """Get model of brand from database

    Args:
        brand (str): brand name.

    """
    logger.info("Getting brands by model in progress... - STATUS: STARTED")
    normalized_name = brand.title()
    response_brands = brand_service.list_brands(
        brand_name=normalized_name, struct_response=False
    )
    if len(json.loads(response_brands.body)) > 0:
        response_model = model_service.list_models(
            brand_id=json.loads(response_brands.body)[0]["id"]
        )
    else:
        logger.success("Getting brands model finished - STATUS: OK")
        return JSONResponse(
            status_code=404,
            content={"brand": f"´{normalized_name}´ not found in db."},
        )
    logger.success("Getting brands model finished - STATUS: OK")
    return response_model


# POST /brands
@router.post("")
async def add_brand(brand: BrandCreateSchema):
    """Add a new brand to db."""
    logger.info("Create a new brand in progress... - STATUS: STARTED")
    normalized_name = brand.name.title()
    response_brand = brand_service.create_new_brand(brand_name=normalized_name)
    logger.success("Create a new brand finished - STATUS: OK")
    return response_brand


# POST /brands/:id/models
@router.post("/{brand}/models")
async def add_model_brand(brand: str, model: CreateModelSchema):
    """Add a new model linked to a brand.
    Args:
        brand (str): brand name linked to the model.
    """
    logger.info("Create a new model in progress... - STATUS: STARTED")
    if model.average_price is not None and model.average_price < 100000:
        return JSONResponse(
            status_code=400,
            content={"error": "average price can't be less than 100,000!"},
        )

    normalized_name = brand.title()
    response_brands = brand_service.list_brands(
        brand_name=normalized_name, struct_response=False
    )
    if len(json.loads(response_brands.body)) == 0:
        return JSONResponse(
            status_code=404,
            content={"error": f"brand '{normalized_name}' does not exist in database!"},
        )

    brand_id = json.loads(response_brands.body)[0]["id"]
    response_model = model_service.create_new_model(data_model=model, brand_id=brand_id)
    logger.success("Create a new model finished - STATUS: OK")
    return response_model
