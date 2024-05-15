from pydantic import BaseModel, Field

from ...utils.base_model import OBaseModel


class MonitoringElement(BaseModel):
    me_id: int
    me: str = Field(..., max_length=255)
    count: int
    dim: int


class MEFilters(OBaseModel):
    me: str | None = None
    me__regex: str | None = None
    dim: int | None = None
