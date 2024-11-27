from typing import Optional

from pydantic import AnyUrl, BaseModel, Field

from ...utils.base_model import OBaseModel, PaginatedBaseModel


class Lumisection(BaseModel):
    dataset_id: int
    dataset: str = Field(..., max_length=255)
    run_number: int
    ls_number: int
    th1_count: int
    th2_count: int


class PaginatedLumisectionList(PaginatedBaseModel):
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: list[Lumisection]


class LumisectionFilters(OBaseModel):
    next_token: Optional[str] = None
    page_size: Optional[int] = None
    dataset_id: Optional[int] = None
    run_number: Optional[int] = None
    run_number__lte: Optional[int] = None
    run_number__gte: Optional[int] = None
    ls_number: Optional[int] = None
    ls_number__lte: Optional[int] = None
    ls_number__gte: Optional[int] = None
    dataset: Optional[str] = None
    dataset__regex: Optional[str] = None
