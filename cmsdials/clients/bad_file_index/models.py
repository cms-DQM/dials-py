from datetime import datetime
from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field

from ...utils.base_model import OBaseModel


class BadFileIndex(BaseModel):
    id: int
    file_path: str = Field(..., description="Path where the file is stored", max_length=255)
    data_era: str = Field(..., description="The era that the data refers to (e.g. 2018A)", max_length=7)
    st_size: float = Field(..., description="The data file's size in bytes")
    st_ctime: datetime = Field(..., description="Time of files's last status change in filesystem")
    st_itime: datetime = Field(..., description="Time when file was indexed in database")
    err: str = Field(..., description="Error message", max_length=255)


class PaginatedBadFileIndexList(BaseModel):
    count: int
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: List[BadFileIndex]


class BadFileIndexFilters(OBaseModel):
    era: Optional[str] = None
    min_size: Optional[float] = None
    page: Optional[str] = None
    path_contains: Optional[str] = None
