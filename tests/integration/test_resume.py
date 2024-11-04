from cmsdials.filters import LumisectionHistogram2DFilters

from .utils import setup_dials_object


def test_resume() -> None:
    dials = setup_dials_object(workspace="tracker")
    data = dials.h2d.list_all(
        LumisectionHistogram2DFilters(me__regex="PXBarrel", ls_number=78, entries__gte=100),
        max_pages=10,
        keep_failed=True,
    )
    assert len(data.results) == 100
    data = dials.h2d.list_all(
        LumisectionHistogram2DFilters(me__regex="PXBarrel", ls_number=78, entries__gte=100),
        max_pages=10,
        keep_failed=True,
        resume_from=data,
    )
    assert len(data.results) == 200
    assert data.results[0].run_number != data.results[100].run_number
    assert data.results[100].run_number != data.results[199].run_number
