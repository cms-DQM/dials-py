from typing import Optional

from pydantic import AnyUrl, BaseModel, Field

from ...utils.base_model import OBaseModel


class LumisectionHistogram2D(BaseModel):
    hist_id: int
    file_id: int
    run_number: int
    ls_id: int
    title: str = Field(..., max_length=220)
    x_min: float
    x_max: float
    x_bin: float
    y_min: float
    y_max: float
    y_bin: float
    entries: int
    data: list[float]


class PaginatedLumisectionHistogram2DList(BaseModel):
    count: int
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: list[LumisectionHistogram2D]


class LumisectionHistogram2DFilters(OBaseModel):
    page: Optional[str] = None
    run_number: Optional[int] = None
    ls_number: Optional[int] = None
    ls_id: Optional[int] = None
    title: Optional[str] = None
    min_run_number: Optional[int] = None
    max_run_number: Optional[int] = None
    min_ls_number: Optional[int] = None
    max_ls_number: Optional[int] = None
    title_contains: Optional[str] = None
    min_entries: Optional[int] = None
    era: Optional[str] = None
    campaign: Optional[str] = None
    dataset: Optional[str] = None
    file_id: Optional[int] = None
