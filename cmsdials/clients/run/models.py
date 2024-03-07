from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel, Field

from ...utils.base_model import OBaseModel


class Run(BaseModel):
    run_number: int
    run_date: Optional[datetime]
    year: Optional[int]
    period: Optional[str] = Field(..., max_length=1)
    date: datetime
    oms_fill: Optional[int]
    oms_lumisections: Optional[int]
    oms_initial_lumi: Optional[float]
    oms_end_lumi: Optional[float]


class PaginatedRunList(BaseModel):
    count: int
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: list[Run]


class RunFilters(OBaseModel):
    max_run_number: Optional[int] = None
    min_run_number: Optional[int] = None
    page: Optional[str] = None
