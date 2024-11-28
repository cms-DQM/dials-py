from typing import Optional

from pydantic import AnyUrl, BaseModel

from ...utils.base_model import OBaseModel, PaginatedBaseModel


class MLModelsIndex(BaseModel):
    model_id: int
    filename: str
    target_me: str
    active: bool


class PaginatedMLModelsIndexList(PaginatedBaseModel):
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: list[MLModelsIndex]


class MLModelsIndexFilters(OBaseModel):
    next_token: Optional[str] = None
    page_size: Optional[int] = None
    model_id: Optional[int] = None
    model_id__in: Optional[list[int]] = None
    filename: Optional[str] = None
    filename__regex: Optional[str] = None
    target_me: Optional[str] = None
    target_me__regex: Optional[str] = None
    active: Optional[bool] = None
