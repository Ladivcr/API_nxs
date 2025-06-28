from typing import Dict

from fastapi import APIRouter

from config.settings import logger
from managers.database_operations import general_operations_db
from schemas.health import HealthSchema

router = APIRouter()


@router.get("/health-check", response_model=HealthSchema)
def health_check() -> Dict:
    """Endpoint to check status API."""
    logger.info("Checking connection in progress... - STATUS: UNKNOWN")
    result = general_operations_db.ping_db()
    if result:
        logger.success("Checking connection in progress... - STATUS: OK")
        return {"status": "Establish connection - OK"}
    else:
        logger.error("Checking connection in progress... - STATUS: FAIL")
        return {"status": "Bad response - Connection Fail"}
