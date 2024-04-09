from datetime import datetime
from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field

from ...utils.base_model import OBaseModel


class FileIndex(BaseModel):
    file_id: int
    file_size: int
    era: str = Field(..., max_length=5)
    campaign: str = Field(..., max_length=15)
    dataset: str = Field(..., max_length=50)
    creation_date: datetime
    last_modification_date: datetime
    logical_file_name: str
    status: str = Field(..., max_length=15)
    err_trace: Optional[str] = Field(..., max_length=5000)


class PaginatedFileIndexList(BaseModel):
    count: int
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: List[FileIndex]


class FileIndexFilters(OBaseModel):
    page: Optional[str] = None
    min_size: Optional[int] = None
    era: Optional[str] = None
    campaign: Optional[str] = None
    dataset: Optional[str] = None
    logical_file_name: Optional[str] = None
    status: Optional[str] = None
