from fastapi import APIRouter

router = APIRouter(prefix="/models")


# PUT /models/:id
@router.put("/{item_id}")
async def update_model(item_id: str):
    """Update a model in db."""
    return None


@router.get("")
async def get_models():
    """Get all modelsfrom db."""
    return None
