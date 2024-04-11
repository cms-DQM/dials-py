from typing import Optional

from pydantic import AnyUrl, BaseModel

from ...utils.base_model import OBaseModel


class Lumisection(BaseModel):
    ls_id: int
    ls_number: int
    th1_count: int
    th2_count: int


class PaginatedLumisectionList(BaseModel):
    count: int
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: list[Lumisection]


class LumisectionFilters(OBaseModel):
    page: Optional[str] = None
    run_number: Optional[int] = None
    ls_number: Optional[int] = None
    min_ls_number: Optional[int] = None
    max_ls_number: Optional[int] = None
    min_run_number: Optional[int] = None
    max_run_number: Optional[int] = None
