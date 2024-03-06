from typing import Optional

from pydantic import AnyUrl, AwareDatetime, BaseModel, Field

from ...utils.base_model import OBaseModel


class LumisectionHistogram2D(BaseModel):
    id: int
    ls_number: int
    run_number: int
    date: AwareDatetime
    title: str = Field(..., max_length=220)
    entries: int | None
    data: list[list[float]] | None
    x_min: float | None
    x_max: float | None
    x_bin: int | None
    y_max: float | None
    y_min: float | None
    y_bin: int | None
    source_data_file: int | None = Field(
        ...,
        description="Source data file that the specific Histogram was read from, if any",
    )
    lumisection: int


class PaginatedLumisectionHistogram2DList(BaseModel):
    count: int | None
    next: AnyUrl | None
    previous: AnyUrl | None
    results: list[LumisectionHistogram2D] | None


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
