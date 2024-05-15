from cmsdials.clients.mes.models import MonitoringElement
from cmsdials.filters import MEFilters

from .utils import setup_dials_object


def test_get_mes() -> None:
    dials = setup_dials_object()
    data = dials.mes.get(id=1)
    assert isinstance(data, MonitoringElement)


def test_list_mes() -> None:
    dials = setup_dials_object()
    data = dials.mes.list()
    for me in data:
        assert isinstance(me, MonitoringElement)


def test_list_all_mes() -> None:
    dials = setup_dials_object()
    data = dials.mes.list_all(MEFilters())
    for me in data:
        assert isinstance(me, MonitoringElement)
