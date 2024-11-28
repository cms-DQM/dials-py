from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel, Field

from ...utils.base_model import OBaseModel, PaginatedBaseModel


class DatasetIndex(BaseModel):
    dataset_id: int
    dataset: str = Field(..., max_length=255)
    era: str = Field(..., max_length=255)
    data_tier: str = Field(..., max_length=255)
    primary_ds_name: str = Field(..., max_length=255)
    processed_ds_name: str = Field(..., max_length=255)
    processing_version: int
    last_modification_date: datetime


class PaginatedDatasetIndexList(PaginatedBaseModel):
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: list[DatasetIndex]


class DatasetIndexFilters(OBaseModel):
    next_token: Optional[str] = None
    page_size: Optional[int] = None
    dataset: Optional[str] = None
    dataset__regex: Optional[str] = None
