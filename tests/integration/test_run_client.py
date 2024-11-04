import pandas as pd
from urllib3.util import Retry

from cmsdials.clients.run.models import PaginatedRunList, Run
from cmsdials.filters import RunFilters

from .utils import DEFAULT_TEST_WORKSPACE, setup_dials_object


def test_get_run() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.run.get(dataset_id=14677060, run_number=367112)
    assert isinstance(data, Run)


def test_list_run() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.run.list()
    assert isinstance(data, PaginatedRunList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_list_all_run() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.run.list_all(RunFilters(), max_pages=5)
    assert isinstance(data, PaginatedRunList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_get_run_with_retries() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.run.get(dataset_id=14677060, run_number=367112, retries=Retry(total=3, backoff_factor=0.1))
    assert isinstance(data, Run)


def test_list_run_with_retries() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.run.list(retries=Retry(total=3, backoff_factor=0.1))
    assert isinstance(data, PaginatedRunList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_list_all_run_with_retries() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.run.list_all(RunFilters(), max_pages=5, retries=Retry(total=3, backoff_factor=0.1))
    assert isinstance(data, PaginatedRunList)
    assert isinstance(data.to_pandas(), pd.DataFrame)
