from ...utils.api_client import BaseAuthorizedAPIClient
from .models import PaginatedRunList, Run, RunFilters


class RunClient(BaseAuthorizedAPIClient):
    data_model = Run
    pagination_model = RunFilters
    filter_class = PaginatedRunList
    lookup_url = "run/"
