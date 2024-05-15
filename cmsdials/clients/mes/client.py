from ...utils.api_client import BaseAuthorizedAPIClient
from .models import MEFilters, MonitoringElement


class MonitoringElementClient(BaseAuthorizedAPIClient):
    data_model = MonitoringElement
    filter_class = MEFilters
    lookup_url = "mes/"
