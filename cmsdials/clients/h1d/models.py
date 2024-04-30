from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field

from ...utils.base_model import OBaseModel


class LumisectionHistogram1D(BaseModel):
    hist_id: int
    dataset: str = Field(..., max_length=255)
    me: str = Field(..., max_length=255)
    dataset_id: int
    file_id: int
    run_number: int
    ls_number: int
    me_id: int
    ls_id: int
    x_min: float
    x_max: float
    x_bin: float
    entries: int
    data: list[float]


class PaginatedLumisectionHistogram1DList(BaseModel):
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: List[LumisectionHistogram1D]


class LumisectionHistogram1DFilters(OBaseModel):
    next_token: Optional[str] = None
    dataset_id: Optional[int] = None
    file_id: Optional[int] = None
    run_number: Optional[int] = None
    run_number__lte: Optional[int] = None
    run_number__gte: Optional[int] = None
    ls_number: Optional[int] = None
    ls_numbet__lte: Optional[int] = None
    ls_number__gte: Optional[int] = None
    me_id: Optional[int] = None
    ls_id: Optional[int] = None
    entries__gte: Optional[int] = None
    dataset: Optional[str] = None
    dataset__regex: Optional[str] = None
    logical_file_name: Optional[str] = None
    logical_file_name__regex: Optional[str] = None
    me: Optional[str] = None
    me__regex: Optional[str] = None
