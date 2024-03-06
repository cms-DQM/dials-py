from typing import Optional

from pydantic import AnyUrl, AwareDatetime, BaseModel, Field

from ...utils.base_model import OBaseModel


class Run(BaseModel):
    run_number: int
    run_date: AwareDatetime | None
    year: int | None
    period: str | None = Field(..., max_length=1)
    date: AwareDatetime
    oms_fill: int | None
    oms_lumisections: int | None
    oms_initial_lumi: float | None
    oms_end_lumi: float | None


class PaginatedRunList(BaseModel):
    count: int | None
    next: AnyUrl | None
    previous: AnyUrl | None
    results: list[Run] | None


class RunFilters(OBaseModel):
    max_run_number: Optional[int] = None
    min_run_number: Optional[int] = None
    page: Optional[str] = None
