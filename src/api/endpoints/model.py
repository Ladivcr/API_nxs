from fastapi import APIRouter, Query
from schemas.models import UpdateModelSchema
from fastapi.responses import JSONResponse
from services.models import model_service
from config.settings import logger
from typing import Optional

router = APIRouter(prefix="/models")


# PUT /models/:id
@router.put("/{model_name}")
async def update_model(model_name: str, update_data: UpdateModelSchema):
    """Update a model in db.

    Args:
        model_name(str): name of the model in db
    """
    logger.info("Updating model in progress... - STATUS: STARTED")

    if update_data.average_price < 100000:
        return JSONResponse(
            status_code=400,
            content={"error": "average price can't be less than 100,000!"},
        )

    update_data.name = model_name
    response = model_service.update_model(data=update_data)
    logger.success("Updating model finished - STATUS: FINISHED")

    return response


@router.get("")
async def get_models(
    greater: Optional[float] = Query(None), lower: Optional[float] = Query(None)
):
    """Get all modelsfrom db."""
    logger.info("Getting models by filter in progress... - STATUS: STARTED")
    if (lower is not None and greater is not None) and lower > greater:
        return JSONResponse(
            status_code=400,
            content={"error": "lower parameter can't be greater than greater parameter!"},
        )
    response = model_service.list_models(min_avg_price=lower, max_avg_price=greater)
    logger.success("Getting models by filter finished - STATUS: FINISHED")
    return response
