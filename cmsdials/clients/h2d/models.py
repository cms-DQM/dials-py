from typing import Optional

from pydantic import AnyUrl, AwareDatetime, BaseModel, Field

from ...utils.base_model import OBaseModel


class LumisectionHistogram2D(BaseModel):
    id: int
    ls_number: int
    run_number: int
    date: AwareDatetime
    title: str = Field(..., max_length=220)
    entries: int
    data: list[list[float]]
    x_min: float
    x_max: float
    x_bin: int
    y_max: float
    y_min: float
    y_bin: int
    source_data_file: int = Field(
        ...,
        description="Source data file that the specific Histogram was read from, if any",
    )
    lumisection: int


class PaginatedLumisectionHistogram2DList(BaseModel):
    count: int
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: list[LumisectionHistogram2D]


class LumisectionHistogram2DFilters(OBaseModel):
    ls_number: Optional[int] = None
    lumisection_id: Optional[int] = None
    max_ls_number: Optional[int] = None
    max_run_number: Optional[int] = None
    min_entries: Optional[int] = None
    min_ls_number: Optional[int] = None
    min_run_number: Optional[int] = None
    page: Optional[str] = None
    run_number: Optional[int] = None
    title: Optional[str] = None
    title_contains: Optional[str] = None
