from pydantic import BaseModel
from typing import Optional


class ModelSchema(BaseModel):
    id: int
    name: str
    average_price: float
    brand_id: int
    brand: Optional[dict] = None


class CreateModelSchema(BaseModel):
    name: str
    average_price: Optional[float] = None
    brand_id: Optional[int] = None


class UpdateModelSchema(BaseModel):
    average_price: float
    name: Optional[str] = None
