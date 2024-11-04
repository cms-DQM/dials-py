from ...utils.api_client import BaseAuthorizedAPIClient
from .models import MEFilters, MonitoringElement


class MonitoringElementClient(BaseAuthorizedAPIClient):
    data_model = MonitoringElement
    filter_class = MEFilters
    lookup_url = "mes/"

    def get(self, id: int, **kwargs):  # noqa: A002
        edp = f"{id}/"
        return super().get(edp, **kwargs)
