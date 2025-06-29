from pydantic import BaseModel


class BrandCreateSchema(BaseModel):
    name: str


class BrandSchema(BaseModel):
    id: int
    name: str
