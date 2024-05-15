from datetime import datetime
from typing import Optional

from pydantic import AnyUrl, BaseModel, Field

from ...utils.base_model import OBaseModel


class FileIndex(BaseModel):
    dataset_id: int
    dataset: str = Field(..., max_length=255)
    file_id: int
    file_size: int
    creation_date: datetime
    last_modification_date: datetime
    logical_file_name: str
    status: str = Field(..., max_length=15)
    err_trace: Optional[str] = Field(..., max_length=5000)


class PaginatedFileIndexList(BaseModel):
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: list[FileIndex]


class FileIndexFilters(OBaseModel):
    next_token: Optional[str] = None
    dataset_id: Optional[int] = None
    logical_file_name: Optional[str] = None
    logical_file_name__regex: Optional[str] = None
    status: Optional[str] = None
    min_size: Optional[int] = None
    dataset: Optional[str] = None
    dataset__regex: Optional[str] = None
