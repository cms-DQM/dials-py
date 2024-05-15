import pandas as pd

from cmsdials.clients.file_index.models import FileIndex, PaginatedFileIndexList
from cmsdials.filters import FileIndexFilters

from .utils import setup_dials_object


def test_get_file_index() -> None:
    dials = setup_dials_object()
    data = dials.file_index.get(id=3386119397)
    assert isinstance(data, FileIndex)


def test_list_file_index() -> None:
    dials = setup_dials_object()
    data = dials.file_index.list()
    assert isinstance(data, PaginatedFileIndexList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_list_all_file_index() -> None:
    dials = setup_dials_object()
    data = dials.file_index.list_all(FileIndexFilters(), max_pages=5)
    assert isinstance(data, PaginatedFileIndexList)
    assert isinstance(data.to_pandas(), pd.DataFrame)
