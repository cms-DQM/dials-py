from typing import List, Optional

from pydantic import AnyUrl, AwareDatetime, BaseModel, Field

from ...utils.base_model import OBaseModel


class FileIndex(BaseModel):
    id: int
    file_uuid: str = Field(..., description="ROOT TFile UUID", max_length=36)
    file_path: str = Field(..., description="Path where the file is stored", max_length=255)
    data_era: str = Field(..., description="The era that the data refers to (e.g. 2018A)", max_length=7)
    n_entries: int = Field(
        ...,
        description="Total number of entries contained in this histogram file",
    )
    n_entries_ingested: int = Field(
        ...,
        description="Number of histogram entries that have been extracted from the file",
    )
    st_size: float = Field(..., description="The data file's size in bytes")
    st_ctime: AwareDatetime = Field(..., description="Time of files's last status change in filesystem")
    st_itime: AwareDatetime = Field(..., description="Time when file was indexed in database")
    status: str = Field(
        ...,
        description="Indicate the processing status of run-histogram within the file",
        max_length=9,
    )


class PaginatedFileIndexList(BaseModel):
    count: int
    next: Optional[AnyUrl]
    previous: Optional[AnyUrl]
    results: List[FileIndex]


class FileIndexFilters(OBaseModel):
    era: Optional[str] = None
    min_size: Optional[float] = None
    page: Optional[str] = None
    path_contains: Optional[str] = None
    status: Optional[str] = None
