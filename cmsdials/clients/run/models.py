from typing import Optional

from pydantic import AnyUrl, BaseModel

from ...utils.base_model import OBaseModel


class Run(BaseModel):
    run_number: int
    ls_count: int


class PaginatedRunList(BaseModel):
    count: int
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: list[Run]


class RunFilters(OBaseModel):
    page: Optional[str] = None
    max_run_number: Optional[int] = None
    min_run_number: Optional[int] = None
