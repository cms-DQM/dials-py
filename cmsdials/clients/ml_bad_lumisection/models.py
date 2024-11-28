from typing import Optional

from pydantic import AnyUrl, BaseModel

from ...utils.base_model import OBaseModel, PaginatedBaseModel


class MLBadLumisection(BaseModel):
    model_id: int
    dataset_id: int
    file_id: int
    run_number: int
    ls_number: int
    me_id: int
    mse: float


class PaginatedMLBadLumisectionList(PaginatedBaseModel):
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: list[MLBadLumisection]


class MLBadLumisectionFilters(OBaseModel):
    next_token: Optional[str] = None
    page_size: Optional[int] = None
    model_id: Optional[int] = None
    model_id__in: Optional[list[int]] = None
    dataset_id: Optional[int] = None
    dataset_id__in: Optional[list[int]] = None
    dataset: Optional[str] = None
    dataset__regex: Optional[str] = None
    me_id: Optional[int] = None
    me: Optional[str] = None
    me__regex: Optional[str] = None
    run_number: Optional[int] = None
    run_number__in: Optional[list[int]] = None
    ls_number: Optional[int] = None
