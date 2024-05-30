import pandas as pd

from cmsdials.clients.h1d.models import LumisectionHistogram1D, PaginatedLumisectionHistogram1DList
from cmsdials.filters import LumisectionHistogram1DFilters

from .utils import setup_dials_object


def test_get_h1d() -> None:
    dials = setup_dials_object()
    data = dials.h1d.get(dataset_id=14677060, run_number=367112, ls_number=10, me_id=1)
    assert isinstance(data, LumisectionHistogram1D)


def test_list_h1d() -> None:
    dials = setup_dials_object()
    data = dials.h1d.list()
    assert isinstance(data, PaginatedLumisectionHistogram1DList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_list_all_h1d() -> None:
    dials = setup_dials_object()
    data = dials.h1d.list_all(LumisectionHistogram1DFilters(), max_pages=5)
    assert isinstance(data, PaginatedLumisectionHistogram1DList)
    assert isinstance(data.to_pandas(), pd.DataFrame)
