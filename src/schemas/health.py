from pydantic import BaseModel


class HealthSchema(BaseModel):
    """Schema for health."""

    status: str = "ok"
