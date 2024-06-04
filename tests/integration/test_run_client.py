import pandas as pd

from cmsdials.clients.run.models import PaginatedRunList, Run
from cmsdials.filters import RunFilters

from .utils import setup_dials_object


def test_get_run() -> None:
    dials = setup_dials_object()
    data = dials.run.get(dataset_id=14677060, run_number=367112)
    assert isinstance(data, Run)


def test_list_run() -> None:
    dials = setup_dials_object()
    data = dials.run.list()
    assert isinstance(data, PaginatedRunList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_list_all_run() -> None:
    dials = setup_dials_object()
    data = dials.run.list_all(RunFilters(), max_pages=5)
    assert isinstance(data, PaginatedRunList)
    assert isinstance(data.to_pandas(), pd.DataFrame)
