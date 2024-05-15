import pandas as pd

from cmsdials.clients.lumisection.models import Lumisection, PaginatedLumisectionList
from cmsdials.filters import LumisectionFilters

from .utils import setup_dials_object


def test_get_lumisection() -> None:
    dials = setup_dials_object()
    data = dials.lumi.get(dataset_id=14677060, run_number=367094, ls_number=1)
    assert isinstance(data, Lumisection)


def test_list_lumisection() -> None:
    dials = setup_dials_object()
    data = dials.lumi.list()
    assert isinstance(data, PaginatedLumisectionList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_list_all_lumisection() -> None:
    dials = setup_dials_object()
    data = dials.lumi.list_all(LumisectionFilters(), max_pages=5)
    assert isinstance(data, PaginatedLumisectionList)
    assert isinstance(data.to_pandas(), pd.DataFrame)
