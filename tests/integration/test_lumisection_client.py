import pandas as pd
from urllib3.util import Retry

from cmsdials.clients.lumisection.models import Lumisection, PaginatedLumisectionList
from cmsdials.filters import LumisectionFilters

from .utils import DEFAULT_TEST_WORKSPACE, setup_dials_object


def test_get_lumisection() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.lumi.get(dataset_id=14677060, run_number=367112, ls_number=10)
    assert isinstance(data, Lumisection)


def test_list_lumisection() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.lumi.list()
    assert isinstance(data, PaginatedLumisectionList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_list_all_lumisection() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.lumi.list_all(LumisectionFilters(), max_pages=5)
    assert isinstance(data, PaginatedLumisectionList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_get_lumisection_with_retries() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.lumi.get(
        dataset_id=14677060, run_number=367112, ls_number=10, retries=Retry(total=3, backoff_factor=0.1)
    )
    assert isinstance(data, Lumisection)


def test_list_lumisection_with_retries() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.lumi.list(retries=Retry(total=3, backoff_factor=0.1))
    assert isinstance(data, PaginatedLumisectionList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_list_all_lumisection_with_retries() -> None:
    dials = setup_dials_object(workspace=DEFAULT_TEST_WORKSPACE)
    data = dials.lumi.list_all(LumisectionFilters(), max_pages=5, retries=Retry(total=3, backoff_factor=0.1))
    assert isinstance(data, PaginatedLumisectionList)
    assert isinstance(data.to_pandas(), pd.DataFrame)
