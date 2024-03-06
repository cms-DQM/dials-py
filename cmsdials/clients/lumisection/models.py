from typing import List, Optional

from pydantic import AnyUrl, AwareDatetime, BaseModel

from ...utils.base_model import OBaseModel


class Lumisection(BaseModel):
    id: int
    ls_number: int
    date: AwareDatetime
    oms_zerobias_rate: float | None
    run: int


class PaginatedLumisectionList(BaseModel):
    count: int | None
    next: AnyUrl | None
    previous: AnyUrl | None
    results: list[Lumisection] | None


class LumisectionFilters(OBaseModel):
    ls_number: Optional[int] = None
    max_ls_number: Optional[int] = None
    max_run_number: Optional[int] = None
    min_ls_number: Optional[int] = None
    min_run_number: Optional[int] = None
    page: Optional[str] = None
    run_number: Optional[int] = None


class ConfiguredMEs(BaseModel):
    mes: List[str]
