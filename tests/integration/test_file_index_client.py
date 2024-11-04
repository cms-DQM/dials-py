import pandas as pd
from urllib3.util import Retry

from cmsdials.clients.file_index.models import FileIndex, PaginatedFileIndexList
from cmsdials.filters import FileIndexFilters

from .utils import DEFAULT_TEST_WORKSPACE, setup_dials_object


def test_get_file_index() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.file_index.get(dataset_id=14677060, file_id=3393809397)
    assert isinstance(data, FileIndex)


def test_list_file_index() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.file_index.list()
    assert isinstance(data, PaginatedFileIndexList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_list_all_file_index() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.file_index.list_all(FileIndexFilters(), max_pages=5)
    assert isinstance(data, PaginatedFileIndexList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_get_file_index_with_retries() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.file_index.get(dataset_id=14677060, file_id=3393809397, retries=Retry(total=3, backoff_factor=0.1))
    assert isinstance(data, FileIndex)


def test_list_file_index_with_retries() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.file_index.list(retries=Retry(total=3, backoff_factor=0.1))
    assert isinstance(data, PaginatedFileIndexList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_list_all_file_index_with_retries() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.file_index.list_all(FileIndexFilters(), max_pages=5, retries=Retry(total=3, backoff_factor=0.1))
    assert isinstance(data, PaginatedFileIndexList)
    assert isinstance(data.to_pandas(), pd.DataFrame)
