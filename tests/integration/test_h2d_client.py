import pandas as pd
from urllib3.util import Retry

from cmsdials.clients.h2d.models import LumisectionHistogram2D, PaginatedLumisectionHistogram2DList
from cmsdials.filters import LumisectionHistogram2DFilters

from .utils import setup_dials_object


def test_get_h2d() -> None:
    dials = setup_dials_object()
    data = dials.h2d.get(dataset_id=14677060, run_number=367112, ls_number=10, me_id=133)
    assert isinstance(data, LumisectionHistogram2D)


def test_list_h2d() -> None:
    dials = setup_dials_object()
    data = dials.h2d.list(retries=Retry(total=3, backoff_factor=0.1))
    assert isinstance(data, PaginatedLumisectionHistogram2DList)
    assert isinstance(data.to_pandas(), pd.DataFrame)


def test_list_all_h2d() -> None:
    dials = setup_dials_object()
    data = dials.h2d.list_all(LumisectionHistogram2DFilters(), max_pages=5, retries=Retry(total=5, backoff_factor=0.1))
    assert isinstance(data, PaginatedLumisectionHistogram2DList)
    assert isinstance(data.to_pandas(), pd.DataFrame)
